import time
from http import HTTPStatus
from typing import List, Union

import uvicorn
from fastapi import APIRouter, FastAPI, Security
from loguru import logger
from pydantic import AnyHttpUrl
from starlette.middleware.cors import CORSMiddleware

from sara_sap.maintenance_api.activity_report.controller import ActivityReportController
from sara_sap.maintenance_api.activity_report.models import (
    ActivityReportCreated,
    UploadedFile,
)
from sara_sap.maintenance_api.documents.controller import DocumentsController
from sara_sap.maintenance_api.documents.models import Document, DocumentCreated
from sara_sap.maintenance_api.insights_uploader.controller import (
    InsightsUploaderController,
)
from sara_sap.maintenance_api.maintenance_plan.models import (
    MaintenanceRecord,
    MaintenancePlan,
)
from sara_sap.maintenance_api.work_orders.controller import WorkOrderController
from sara_sap.maintenance_api.work_orders.models import PreventiveWorkOrder
from sara_sap.authentication import Authenticator
from sara_sap.maintenance_api.maintenance_plan.controller import (
    MaintenancePlanController,
)
from sara_sap.settings import settings


class API:
    def __init__(
        self,
        authenticator: Authenticator,
        maintenance_plan_controller: MaintenancePlanController,
        activity_report_controller: ActivityReportController,
        work_order_controller: WorkOrderController,
        documents_controller: DocumentsController,
        insights_uploader_controller: InsightsUploaderController,
    ):
        self.host: str = settings.API_HOST_IP
        self.port: int = settings.PORT

        self.authenticator: Authenticator = authenticator
        self.maintenance_plan_controller: MaintenancePlanController = (
            maintenance_plan_controller
        )
        self.activity_report_controller: ActivityReportController = (
            activity_report_controller
        )
        self.work_order_controller: WorkOrderController = work_order_controller
        self.documents_controller: DocumentsController = documents_controller
        self.insights_uploader_controller: InsightsUploaderController = (
            insights_uploader_controller
        )

        self.app: FastApi = self._create_app()
        self.server: uvicorn.Server = self._setup_server()

    def get_app(self) -> FastAPI:
        return self.app

    def _setup_server(self) -> uvicorn.Server:
        config = uvicorn.Config(
            app=self.app,
            port=self.port,
            host=self.host,
            reload=False,
            log_config=None,
        )
        return uvicorn.Server(config)

    def wait_for_api_server_ready(self) -> None:
        while not self.server.started:
            time.sleep(0.01)
        logger.info("Uvicorn server has been started")
        self._log_startup_message()

    def _create_app(self) -> FastAPI:
        app: FastAPI = FastAPI(
            openapi_tags=[
                {
                    "name": "Maintenance Plan",
                    "description": "Endpoints which allow for interaction with maintenance plans through "
                    "Maintenance API.",
                },
                {
                    "name": "Activity Report",
                    "description": "Endpoints which allow for interaction with activity reports (maintenance records) "
                    "through Maintenance API.",
                },
                {
                    "name": "Work Order",
                    "description": "Endpoints which allow for interaction with work orders through Maintenance API.",
                },
                {
                    "name": "Documents",
                    "description": "Endpoints which allow for interaction with documents through Maintenance API.",
                },
                {
                    "name": "Insights Uploader",
                    "description": "Endpoints used to post data to SAP through the Maintenance API for specific "
                    "use cases.",
                },
            ],
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
        app.include_router(router=self._create_activity_report_router())
        app.include_router(router=self._create_work_order_router())
        app.include_router(router=self._create_insights_uploader_router())
        app.include_router(router=self._create_documents_router())

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

    def _create_activity_report_router(self) -> APIRouter:
        router: APIRouter = APIRouter(tags=["Activity Report"])
        authentication_dependency: Security = Security(self.authenticator.get_scheme())

        router.add_api_route(
            path="/activity-report",
            endpoint=self.activity_report_controller.get_activity_report_by_record_id,
            methods=["GET"],
            dependencies=[authentication_dependency],
            summary="Get the activity report (maintenance record) for a given activity report record ID",
            responses={
                HTTPStatus.OK.value: {
                    "description": "Successfully retrieved activity report",
                    "model": MaintenanceRecord,
                },
                HTTPStatus.BAD_REQUEST.value: {
                    "description": "Bad request",
                },
                HTTPStatus.NOT_FOUND.value: {
                    "description": "The activity report with the provided ID was not found in SAP",
                },
            },
        )

        router.add_api_route(
            path="/activity-report/update-status",
            endpoint=self.activity_report_controller.update_status_of_activity_report,
            methods=["PATCH"],
            dependencies=[authentication_dependency],
            summary="Update status of the activity report for a given activity report record ID",
            responses={
                HTTPStatus.NO_CONTENT.value: {
                    "description": "Successfully updated activity report status",
                },
                HTTPStatus.BAD_REQUEST.value: {
                    "description": "Bad request",
                },
                HTTPStatus.NOT_FOUND.value: {
                    "description": "The activity report with the provided ID was not found in SAP",
                },
            },
        )

        router.add_api_route(
            path="/activity-report/create",
            endpoint=self.activity_report_controller.post_activity_report_to_work_order,
            methods=["POST"],
            dependencies=[authentication_dependency],
            summary="Add a new activity report to an existing work order",
            responses={
                HTTPStatus.CREATED.value: {
                    "description": "Successfully created activity report",
                    "model": ActivityReportCreated,
                },
                HTTPStatus.BAD_REQUEST.value: {
                    "description": "Bad request",
                },
            },
        )

        router.add_api_route(
            path="/activity-report/upload-attachment",
            endpoint=self.activity_report_controller.upload_attachment_to_activity_report,
            methods=["POST"],
            dependencies=[authentication_dependency],
            summary="Upload an attachment to the activity report with corresponding maintenance order ID "
            "and pre-defined document ID",
            responses={
                HTTPStatus.OK.value: {
                    "description": "Successfully uploaded attachment",
                },
                HTTPStatus.BAD_REQUEST.value: {
                    "description": "Bad request",
                },
            },
        )

        router.add_api_route(
            path="/activity-report/download-attachment",
            endpoint=self.activity_report_controller.download_attachment_from_activity_report,
            methods=["POST"],
            dependencies=[authentication_dependency],
            summary="Download an attachment from the activity report with corresponding maintenance order ID "
            "and pre-defined document ID",
            responses={
                HTTPStatus.OK.value: {
                    "description": "Successfully downloaded attachment",
                },
                HTTPStatus.BAD_REQUEST.value: {
                    "description": "Bad request",
                },
            },
        )

        return router

    def _create_work_order_router(self) -> APIRouter:
        router: APIRouter = APIRouter(tags=["Work Order"])
        authentication_dependency: Security = Security(self.authenticator.get_scheme())

        router.add_api_route(
            path="/preventive-work-order",
            endpoint=self.work_order_controller.get_preventive_work_order_by_id,
            methods=["GET"],
            dependencies=[authentication_dependency],
            summary="Get the preventive work order for a given work order ID",
            responses={
                HTTPStatus.OK.value: {
                    "description": "Successfully retrieved preventive work order",
                    "model": PreventiveWorkOrder,
                },
                HTTPStatus.BAD_REQUEST.value: {
                    "description": "Bad request",
                },
            },
        )

        return router

    def _create_insights_uploader_router(self) -> APIRouter:
        router: APIRouter = APIRouter(tags=["Insights Uploader"])
        authentication_dependency: Security = Security(self.authenticator.get_scheme())

        router.add_api_route(
            path="/insights-uploader",
            endpoint=self.insights_uploader_controller.upload_co2_report_to_sap_next_in_line_work_order,
            methods=["POST"],
            dependencies=[authentication_dependency],
            summary="Upload a CO2 report to the next upcoming SAP work order for the fugitive gas monitoring "
            "preventive maintenance plan",
            responses={
                HTTPStatus.OK.value: {
                    "description": "Successfully uploaded CO2 report to SAP work order",
                    "model": List[UploadedFile],
                },
                HTTPStatus.BAD_REQUEST.value: {
                    "description": "Bad request",
                },
            },
        )

        router.add_api_route(
            path="/insights-uploader/next-co2-work-order",
            endpoint=self.insights_uploader_controller.get_next_work_order_for_c02_maintenance_plan,
            methods=["GET"],
            dependencies=[authentication_dependency],
            summary="Retrieve the next work order in line for uploading CO2 reports to. This is the closest work order "
            "in time which is already called and set as on hold. ",
            responses={
                HTTPStatus.OK.value: {
                    "description": "Successfully retrieved next work order.",
                    "model": PreventiveWorkOrder,
                },
                HTTPStatus.BAD_REQUEST.value: {
                    "description": "Bad request",
                },
            },
        )

        return router

    def _create_documents_router(self) -> APIRouter:
        router: APIRouter = APIRouter(tags=["Documents"])
        authentication_dependency: Security = Security(self.authenticator.get_scheme())

        router.add_api_route(
            path="/documents/create",
            endpoint=self.documents_controller.create_document,
            methods=["POST"],
            dependencies=[authentication_dependency],
            summary="Create a new document reference in SAP",
            responses={
                HTTPStatus.OK.value: {
                    "description": "Successfully created a new document reference in SAP",
                    "model": DocumentCreated,
                },
                HTTPStatus.BAD_REQUEST.value: {
                    "description": "Bad request",
                },
            },
        )

        router.add_api_route(
            path="/documents/add-document-relationship-to-maintenance-record",
            endpoint=self.documents_controller.add_document_relationship_to_maintenance_record,
            methods=["POST"],
            dependencies=[authentication_dependency],
            summary="Add a relationship between a maintenance record and a document",
            responses={
                HTTPStatus.CREATED.value: {
                    "description": "Successfully added relationship between maintenance record and a document",
                },
                HTTPStatus.BAD_REQUEST.value: {
                    "description": "Bad request",
                },
            },
        )

        router.add_api_route(
            path="/documents/maintenance-record-relationships",
            endpoint=self.documents_controller.get_document_maintenance_record_relationships,
            methods=["GET"],
            dependencies=[authentication_dependency],
            summary="Retrieve the maintenance record relationships for a maintenance record (activity report)",
            responses={
                HTTPStatus.OK.value: {
                    "description": "Successfully retrieved maintenance record relationships",
                    "model": List[Document],
                },
                HTTPStatus.BAD_REQUEST.value: {
                    "description": "Bad request",
                },
            },
        )

        return router

    @staticmethod
    def _log_startup_message() -> None:
        print("API is starting up...")
