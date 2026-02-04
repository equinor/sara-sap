from datetime import datetime
from http import HTTPStatus
from pathlib import Path
from typing import Dict, List, Tuple, BinaryIO

from fastapi import HTTPException, UploadFile
from loguru import logger
from requests import RequestException, Response
from fastapi.responses import Response as FastAPIResponse

from sara_sap.maintenance_api.activity_report.enums import ActivityReportStatus
from sara_sap.maintenance_api.activity_report.models import (
    ActivityReportCreated,
    UploadedFile,
)
from sara_sap.maintenance_api.maintenance_plan.models import (
    ActivityReportStatusUpdateRequest,
    MaintenanceRecord,
)
from sara_sap.utilities.parse_response import parse_response_into_model
from sara_sap.utilities.request_handler import get, post, patch


class ActivityReportService:
    @staticmethod
    def get_activity_report_by_record_id(
        activity_report_record_id: str, access_token: str
    ) -> MaintenanceRecord:
        url: str = (
            f"https://api-test.gateway.equinor.com/maintenance-api/maintenance-records/activity-reports/"
            f"{activity_report_record_id}"
        )
        try:
            response: Response = get(
                url=url,
                headers={"Authorization": f"Bearer {access_token}"},
                params={"api-version": "v1"},
            )

            maintenance_record: MaintenanceRecord = parse_response_into_model(
                response=response, model_type=MaintenanceRecord
            )

            return maintenance_record

        except RequestException, Exception:
            error_description: str = (
                f"Failed to get activity report for record id {activity_report_record_id}"
            )
            logger.exception(error_description)
            raise HTTPException(status_code=500, detail=error_description)

    @staticmethod
    def update_status_of_activity_report(
        new_status: ActivityReportStatus,
        activity_report_record_id: str,
        access_token: str,
    ) -> FastAPIResponse:
        url: str = (
            f"https://api-test.gateway.equinor.com/maintenance-api/maintenance-records/activity-reports/"
            f"{activity_report_record_id}/statuses/{new_status.value}"
        )

        body: List[ActivityReportStatusUpdateRequest] = [
            ActivityReportStatusUpdateRequest(
                op="replace", path="/isActive", value=True
            )
        ]

        try:
            _ = patch(
                url=url,
                headers={"Authorization": f"Bearer {access_token}"},
                params={"api-version": "v1"},
                json_body=body,
            )
            return FastAPIResponse(status_code=HTTPStatus.NO_CONTENT)

        except RequestException:
            error_description: str = (
                f"Failed to upload activity report status to {new_status.value} "
                f"on activity report {activity_report_record_id}"
            )
            logger.exception(error_description)
            raise HTTPException(status_code=500, detail=error_description)

    @staticmethod
    def post_activity_report_to_work_order(
        work_order_id: str,
        source_id: str,
        work_center_id: str,
        work_center_plant_id: str,
        access_token: str,
    ) -> ActivityReportCreated:
        url: str = (
            "https://api-test.gateway.equinor.com/maintenance-api/maintenance-records/activity-reports"
        )

        current_month: str = datetime.now().strftime("%B")
        request_body: Dict = {
            "title": f"CO2 measurements from robot for {current_month}",
            "text": f"Spot measurements of CO2 performed by autonomous robot for the month of {current_month}",
            "tagPlantId": "1875",
            "isOpen": True,
            "workCenterId": work_center_id,
            "workCenterPlantId": work_center_plant_id,
            "relatedWorkOrder": {
                "workOrderId": work_order_id,
                "source": "ObjectList",
                "sourceId": source_id,
            },
        }

        try:
            response: Response = post(
                url=url,
                headers={"Authorization": f"Bearer {access_token}"},
                params={"api-version": "v1"},
                json_body=request_body,
            )
            return parse_response_into_model(
                response=response, model_type=ActivityReportCreated
            )

        except RequestException, Exception:
            error_description: str = (
                f"Failed to post activity report to work order {work_order_id} in SAP"
            )
            logger.exception(error_description)
            raise HTTPException(status_code=500, detail=error_description)

    @staticmethod
    def upload_attachments_to_activity_report(
        maintenance_record_id: str,
        document_id: str,
        files: List[UploadFile],
        access_token: str,
    ) -> List[UploadedFile]:
        url: str = (
            f"https://api-test.gateway.equinor.com/maintenance-api/maintenance-records/activity-reports/"
            f"{maintenance_record_id}/attachments"
        )

        files_to_upload: List[Tuple[str, Tuple[str, BinaryIO, str]]] = [
            ("files", (f.filename, f.file, f.content_type)) for f in files
        ]

        try:
            _ = post(
                url=url,
                headers={"Authorization": f"Bearer {access_token}"},
                params={"document-id": document_id, "api-version": "v1"},
                files=files_to_upload,
            )

            return [
                UploadedFile(
                    maintenance_record_id=maintenance_record_id,
                    document_id=document_id,
                    file_name=f.filename,
                )
                for f in files
            ]

        except RequestException, Exception:
            error_description: str = (
                f"Failed to upload attachments to activity report {maintenance_record_id} "
                f"and document {document_id}"
            )
            logger.exception(error_description)
            raise HTTPException(status_code=500, detail=error_description)

    @staticmethod
    def download_attachment_from_activity_report(
        maintenance_record_id: str, attachment_id: str, access_token: str
    ) -> None:
        url: str = (
            f"https://api-test.gateway.equinor.com/maintenance-api/maintenance-records/activity-reports/"
            f"{maintenance_record_id}/attachments/{attachment_id}"
        )

        response: Response = get(
            url=url,
            headers={"Authorization": f"Bearer {access_token}"},
            params={"api-version": "v1"},
        )

        path: Path = Path("./test.html")
        path.write_bytes(response.content)
        return
