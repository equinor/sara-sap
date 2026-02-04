from typing import List

from fastapi import Depends, File, UploadFile
from fastapi_azure_auth.user import User

from sara_sap.maintenance_api.activity_report.api import ActivityReportService
from sara_sap.maintenance_api.activity_report.models import (
    ActivityReportCreated,
    UploadedFile,
)
from sara_sap.maintenance_api.documents.api import DocumentsService
from sara_sap.maintenance_api.documents.models import DocumentCreated
from sara_sap.maintenance_api.maintenance_plan.models import (
    MaintenancePlan,
    MaintenancePlanItem,
    WorkOrderCall,
)
from sara_sap.maintenance_api.work_orders.api import WorkOrderService
from sara_sap.maintenance_api.work_orders.models import PreventiveWorkOrder
from sara_sap.authentication import (
    azure_scheme,
    get_on_behalf_of_token_for_maintenance_api,
)
from sara_sap.maintenance_api.maintenance_plan.api import MaintenancePlanService
from sara_sap.settings import settings


class InsightsUploaderController:
    def __init__(
        self,
        maintenance_plan_service: MaintenancePlanService,
        work_order_service: WorkOrderService,
        activity_report_service: ActivityReportService,
        documents_service: DocumentsService,
    ):
        self.maintenance_plan_service: MaintenancePlanService = maintenance_plan_service
        self.work_order_service: WorkOrderService = work_order_service
        self.activity_report_service: ActivityReportService = activity_report_service
        self.documents_service: DocumentsService = documents_service

    def upload_co2_report_to_sap_next_in_line_work_order(
        self,
        files: List[UploadFile] = File(...),
        user: User = Depends(azure_scheme),
    ) -> List[UploadedFile]:
        access_token: str = get_on_behalf_of_token_for_maintenance_api(
            access_token=user.access_token
        )

        preventive_work_order_id: str = self._get_work_order_id_for_insights_upload(
            access_token
        )
        work_order: PreventiveWorkOrder = (
            self.work_order_service.get_preventive_work_order_by_id(
                work_order_id=preventive_work_order_id, access_token=access_token
            )
        )

        source_id: str = (
            self.work_order_service.get_next_object_list_id_from_preventive_work_order(
                preventive_work_order=work_order
            )
        )

        activity_report: ActivityReportCreated = (
            self.activity_report_service.post_activity_report_to_work_order(
                work_order_id=preventive_work_order_id,
                source_id=source_id,
                work_center_id=work_order.work_center_id,
                work_center_plant_id=work_order.work_center_plant_id,
                access_token=access_token,
            )
        )

        document: DocumentCreated = self.documents_service.create_document(
            document_title="Robot automated CO2 measurements",
            document_description="This document contains files which give an overview of CO2 measurements performed by "
            "the robot for the given time period. Please note that the .html file must be opened in the Windows SAP "
            "client. For any questions please contact the robot team at fg_robots@equinor.com.",
            access_token=access_token,
        )

        self.documents_service.add_document_relationship_to_maintenance_record(
            document_id=document.document_id,
            maintenance_record_id=activity_report.record_id,
            access_token=access_token,
        )

        return self.activity_report_service.upload_attachments_to_activity_report(
            maintenance_record_id=activity_report.record_id,
            document_id=document.document_id,
            files=files,
            access_token=access_token,
        )

    def get_next_work_order_for_c02_maintenance_plan(
        self, user: User = Depends(azure_scheme)
    ) -> PreventiveWorkOrder:
        access_token: str = get_on_behalf_of_token_for_maintenance_api(
            access_token=user.access_token
        )
        preventive_work_order_id: str = self._get_work_order_id_for_insights_upload(
            access_token
        )
        work_order: PreventiveWorkOrder = (
            self.work_order_service.get_preventive_work_order_by_id(
                work_order_id=preventive_work_order_id, access_token=access_token
            )
        )

        return work_order

    def _get_work_order_id_for_insights_upload(self, access_token: str) -> str:
        maintenance_plan: MaintenancePlan = (
            self.maintenance_plan_service.get_maintenance_plan_by_id(
                maintenance_plan_id=settings.MAINTENANCE_PLAN_ID,
                access_token=access_token,
            )
        )

        maintenance_plan_item: MaintenancePlanItem = (
            self.maintenance_plan_service.find_maintenance_item_by_id(
                maintenance_plan=maintenance_plan,
                item_id=settings.MAINTENANCE_PLAN_ITEM_ID,
            )
        )

        work_order_call: WorkOrderCall = (
            self.maintenance_plan_service.select_next_called_work_order(
                maintenance_plan_item=maintenance_plan_item
            )
        )

        return work_order_call.preventive_work_order_id
