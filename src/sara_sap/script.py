import uvicorn
from fastapi import FastAPI

from sara_sap.api import API
from sara_sap.container import ApplicationContainer, get_injector
from sara_sap.settings import settings


def start() -> None:
    injector: ApplicationContainer = get_injector()

    api: API = injector.api()
    api.server.run()


if __name__ == "__main__":
    start()
