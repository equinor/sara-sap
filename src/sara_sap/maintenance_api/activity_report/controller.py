from http import HTTPStatus
from typing import List

from fastapi import Depends, UploadFile, File
from fastapi import Response as FastAPIResponse
from fastapi_azure_auth.user import User

from sara_sap.authentication import (
    azure_scheme,
    get_on_behalf_of_token_for_maintenance_api,
)
from sara_sap.maintenance_api.activity_report.api import ActivityReportService
from sara_sap.maintenance_api.activity_report.enums import ActivityReportStatus
from sara_sap.maintenance_api.activity_report.models import (
    ActivityReportCreated,
    UploadedFile,
)
from sara_sap.maintenance_api.maintenance_plan.models import MaintenanceRecord
from sara_sap.maintenance_api.work_orders.api import WorkOrderService
from sara_sap.maintenance_api.work_orders.models import PreventiveWorkOrder


class ActivityReportController:
    def __init__(
        self,
        activity_report_service: ActivityReportService,
        work_order_service: WorkOrderService,
    ) -> None:
        self.activity_report_service: ActivityReportService = activity_report_service
        self.work_order_service: WorkOrderService = work_order_service

    def get_activity_report_by_record_id(
        self, activity_report_record_id: str, user: User = Depends(azure_scheme)
    ) -> MaintenanceRecord:
        access_token: str = get_on_behalf_of_token_for_maintenance_api(
            access_token=user.access_token
        )

        return self.activity_report_service.get_activity_report_by_record_id(
            activity_report_record_id=activity_report_record_id,
            access_token=access_token,
        )

    def update_status_of_activity_report(
        self,
        activity_report_record_id: str,
        new_status: ActivityReportStatus,
        user: User = Depends(azure_scheme),
    ) -> FastAPIResponse:
        access_token: str = get_on_behalf_of_token_for_maintenance_api(
            access_token=user.access_token
        )

        self.activity_report_service.update_status_of_activity_report(
            activity_report_record_id=activity_report_record_id,
            new_status=new_status,
            access_token=access_token,
        )

        return FastAPIResponse(status_code=HTTPStatus.CREATED)

    def post_activity_report_to_work_order(
        self, work_order_id: str, user: User = Depends(azure_scheme)
    ) -> ActivityReportCreated:
        access_token: str = get_on_behalf_of_token_for_maintenance_api(
            access_token=user.access_token
        )

        work_order: PreventiveWorkOrder = (
            self.work_order_service.get_preventive_work_order_by_id(
                work_order_id=work_order_id, access_token=access_token
            )
        )

        source_id: str = (
            self.work_order_service.get_next_object_list_id_from_preventive_work_order(
                preventive_work_order=work_order
            )
        )

        return self.activity_report_service.post_activity_report_to_work_order(
            work_order_id=work_order_id,
            source_id=source_id,
            work_center_id=work_order.work_center_id,
            work_center_plant_id=work_order.work_center_plant_id,
            access_token=access_token,
        )

    def upload_attachment_to_activity_report(
        self,
        maintenance_record_id: str,
        document_id: str,
        files: List[UploadFile] = File(...),
        user: User = Depends(azure_scheme),
    ) -> List[UploadedFile]:
        access_token: str = get_on_behalf_of_token_for_maintenance_api(
            access_token=user.access_token
        )
        return self.activity_report_service.upload_attachments_to_activity_report(
            maintenance_record_id=maintenance_record_id,
            document_id=document_id,
            files=files,
            access_token=access_token,
        )

    def download_attachment_from_activity_report(
        self,
        maintenance_record_id: str,
        attachment_id: str,
        user: User = Depends(azure_scheme),
    ) -> None:
        access_token: str = get_on_behalf_of_token_for_maintenance_api(
            access_token=user.access_token
        )

        self.activity_report_service.download_attachment_from_activity_report(
            maintenance_record_id=maintenance_record_id,
            attachment_id=attachment_id,
            access_token=access_token,
        )

        return
