from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from sara_sap.api import API
from sara_sap.authentication import Authenticator
from sara_sap.maintenance_api.activity_report.api import ActivityReportService
from sara_sap.maintenance_api.activity_report.controller import ActivityReportController
from sara_sap.maintenance_api.documents.api import DocumentsService
from sara_sap.maintenance_api.documents.controller import DocumentsController
from sara_sap.maintenance_api.insights_uploader.controller import (
    InsightsUploaderController,
)
from sara_sap.maintenance_api.maintenance_plan.api import MaintenancePlanService
from sara_sap.maintenance_api.maintenance_plan.controller import (
    MaintenancePlanController,
)
from sara_sap.maintenance_api.work_orders.api import WorkOrderService
from sara_sap.maintenance_api.work_orders.controller import WorkOrderController
from sara_sap.settings import settings


class ApplicationContainer(DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[settings])

    authenticator: Authenticator = providers.Singleton(Authenticator)

    maintenance_plan_service: MaintenancePlanService = providers.Singleton(
        MaintenancePlanService
    )
    activity_report_service: ActivityReportService = providers.Singleton(
        ActivityReportService
    )
    work_order_service: WorkOrderService = providers.Singleton(WorkOrderService)
    documents_service: DocumentsService = providers.Singleton(DocumentsService)

    activity_report_controller: ActivityReportController = providers.Singleton(
        ActivityReportController,
        activity_report_service=activity_report_service,
        work_order_service=work_order_service,
    )
    maintenance_plan_controller: MaintenancePlanController = providers.Singleton(
        MaintenancePlanController, maintenance_plan_service=maintenance_plan_service
    )
    work_order_controller: WorkOrderController = providers.Singleton(
        WorkOrderController, work_order_service=work_order_service
    )
    documents_controller: DocumentsController = providers.Singleton(
        DocumentsController, documents_service=documents_service
    )
    insights_uploader_controller: InsightsUploaderController = providers.Singleton(
        InsightsUploaderController,
        maintenance_plan_service=maintenance_plan_service,
        work_order_service=work_order_service,
        activity_report_service=activity_report_service,
        documents_service=documents_service,
    )

    api: API = providers.Singleton(
        API,
        authenticator=authenticator,
        maintenance_plan_controller=maintenance_plan_controller,
        activity_report_controller=activity_report_controller,
        work_order_controller=work_order_controller,
        documents_controller=documents_controller,
        insights_uploader_controller=insights_uploader_controller,
    )


def get_injector() -> ApplicationContainer:
    container: ApplicationContainer = ApplicationContainer()
    container.init_resources()
    container.wire(modules=[__name__])

    print("Loaded the following module configurations:")
    for provider_name, provider in container.providers.items():
        provider_repr = repr(provider)
        simplified_provider = provider_repr.split(".")[-1].split(">")[0]
        print(f"    {provider_name:<20}: {simplified_provider}")

    return container
