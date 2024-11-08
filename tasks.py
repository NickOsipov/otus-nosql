"""
Script: tasks.py
Description: Invoke tasks for managing services.
"""

import os
from typing import Dict, Callable
from functools import lru_cache
from invoke import task
from invoke.context import Context
from dotenv import load_dotenv

load_dotenv()

INFRA_DIR = "infrastructure"
SERVICES = ["minio", "clickhouse", "mongodb"]


def create_service_action(service_name: str) -> Dict[str, Callable]:
    """Create service actions for a given service name."""
    service_path = os.path.join(INFRA_DIR, service_name)
    return {
        "up": lambda ctx: ctx.run(f"cd {service_path} && docker-compose up -d"),
        "down": lambda ctx: ctx.run(f"cd {service_path} && docker-compose down"),
    }


@lru_cache(maxsize=None)
def get_service_actions() -> Dict[str, Dict[str, Callable]]:
    """Get cached service actions dictionary."""
    return {service: create_service_action(service) for service in SERVICES}


def get_services_list(services: str) -> list:
    """Convert services string to list and validate."""
    if not services:
        return []

    services_list = [s.strip().lower() for s in services.split(",")]
    valid_services = SERVICES + ["all"]

    invalid_services = [s for s in services_list if s not in valid_services]
    if invalid_services:
        raise ValueError(
            f"Invalid service(s): {', '.join(invalid_services)}. "
            f"Valid options are: {', '.join(valid_services)}"
        )

    if "all" in services_list:
        return SERVICES

    return services_list


@task(
    help={
        "services": f'List of services to start: "all", {", ".join(f"{s}" for s in SERVICES)}'
    }
)
def up(ctx: Context, services: str = "all") -> None:
    """Start the specified services."""
    services_list = get_services_list(services)

    if not services_list:
        print("No services specified")
        return

    service_actions = get_service_actions()
    print(f"Starting services: {', '.join(services_list)}")
    for service in services_list:
        print(f"Starting {service}...")
        service_actions[service]["up"](ctx)


@task(
    help={
        "services": f'List of services to stop: "all", {", ".join(f"{s}" for s in SERVICES)}'
    }
)
def down(ctx: Context, services: str = "all") -> None:
    """Stop the specified services."""
    services_list = get_services_list(services)

    if not services_list:
        print("No services specified")
        return

    service_actions = get_service_actions()
    print(f"Stopping services: {', '.join(services_list)}")
    for service in services_list:
        print(f"Stopping {service}...")
        service_actions[service]["down"](ctx)
