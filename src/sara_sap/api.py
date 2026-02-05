from http import HTTPStatus
from typing import List, Union

from fastapi import APIRouter, FastAPI, Security
from pydantic import AnyHttpUrl
from starlette.middleware.cors import CORSMiddleware

from sara_sap.authentication import Authenticator
from sara_sap.maintenance_api.maintenance_plan.controller import (
    MaintenancePlanController,
)
from sara_sap.maintenance_api.models import MaintenancePlan
from sara_sap.settings import settings


class API:
    def __init__(self):
        self.authenticator: Authenticator = Authenticator()
        self.host: str = settings.API_HOST_IP
        self.port: int = settings.PORT

        self.maintenance_plan_controller = MaintenancePlanController()

    def setup_fastapi(self) -> FastAPI:
        app: FastAPI = FastAPI(
            on_startup=[
                self.authenticator.load_config,
                self._log_startup_message,
            ],
            swagger_ui_oauth2_redirect_url="/oauth2-redirect",
            swagger_ui_init_oauth={
                "usePkceWithAuthorizationCodeGrant": True,
                "clientId": settings.AZURE_CLIENT_ID,
            },
        )

        if self.authenticator.should_authenticate():
            backend_cors_origins: List[Union[str, AnyHttpUrl]] = [
                f"http://{self.host}:{self.port}"
            ]

            app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in backend_cors_origins],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        app.include_router(router=self._create_maintenance_plan_router())

        return app

    def _create_maintenance_plan_router(self) -> APIRouter:
        router: APIRouter = APIRouter(tags=["Maintenance Plan"])

        authentication_dependency: Security = Security(self.authenticator.get_scheme())

        router.add_api_route(
            path="/maintenance-plan",
            endpoint=self.maintenance_plan_controller.get_maintenance_plan,
            methods=["GET"],
            dependencies=[authentication_dependency],
            summary="Get the maintenance plan for a given maintenance plan ID",
            responses={
                HTTPStatus.OK.value: {
                    "description": "Successfully retrieved maintenance plan",
                    "model": MaintenancePlan,
                },
                HTTPStatus.BAD_REQUEST.value: {
                    "description": "Bad request",
                },
                HTTPStatus.NOT_FOUND.value: {
                    "description": "The maintenance plan with the provided ID was not found in SAP",
                },
            },
        )

        return router

    def _log_startup_message(self) -> None:
        print("API is starting up...")


api: API = API()
app = api.setup_fastapi()
