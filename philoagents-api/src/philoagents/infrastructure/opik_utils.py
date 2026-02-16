import os

import opik
from loguru import logger
from opik.configurator.configure import OpikConfigurator
from opik.rest_api.core.api_error import ApiError

from philoagents.config import settings


def configure() -> None:
    if not settings.COMET_API_KEY:
        logger.warning(
            "COMET_API_KEY is not set. Set it to enable prompt monitoring with Opik (powered by Comet ML)."
        )
        return

    # Use COMET_WORKSPACE from env when set, else try to fetch default
    workspace = settings.COMET_WORKSPACE
    if workspace is None:
        try:
            client = OpikConfigurator(api_key=settings.COMET_API_KEY)
            workspace = client._get_default_workspace()
        except Exception:
            logger.warning(
                "Default workspace not found. Set COMET_WORKSPACE in .env (e.g. vishnu-pratap)."
            )
            workspace = None

    os.environ["OPIK_API_KEY"] = settings.COMET_API_KEY
    os.environ["OPIK_PROJECT_NAME"] = settings.COMET_PROJECT
    if workspace:
        os.environ["OPIK_WORKSPACE"] = workspace

    try:
        opik.configure(
            api_key=settings.COMET_API_KEY,
            workspace=workspace,
            use_local=False,
            force=True,
        )
        logger.info(
            f"Opik configured successfully (project: {settings.COMET_PROJECT}, workspace: {workspace})"
        )
    except Exception:
        logger.warning(
            "Couldn't configure Opik. Check COMET_API_KEY, COMET_PROJECT, and COMET_WORKSPACE."
        )



def get_dataset(name: str) -> opik.Dataset:
    client = opik.Opik()
    try:
        dataset = client.get_dataset(name=name)
    except Exception:
        logger.warning(f"Dataset {name} not found.")
        return None
    return dataset


def create_dataset(name: str, description: str, items: list[dict]) -> opik.Dataset:

    client = opik.Opik()
    try:
        client.delete_dataset(name=name)
    except ApiError as e:
        if e.status_code != 404:
            raise
    dataset = client.create_dataset(name=name, description=description)
    dataset.insert(items)
    return dataset