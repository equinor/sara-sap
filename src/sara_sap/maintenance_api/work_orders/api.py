import traceback

from fastapi import HTTPException
from loguru import logger
from requests import Response, RequestException

from sara_sap.maintenance_api.work_orders.models import PreventiveWorkOrder
from sara_sap.utilities.request_handler import get
from sara_sap.utilities.parse_response import parse_response_into_model


class WorkOrderService:
    @staticmethod
    def get_preventive_work_order_by_id(
        work_order_id: str, access_token: str
    ) -> PreventiveWorkOrder:
        url: str = (
            f"https://api-test.gateway.equinor.com/maintenance-api/work-orders/preventive-work-orders/{work_order_id}"
        )
        try:
            response: Response = get(
                url=url,
                headers={"Authorization": f"Bearer {access_token}"},
                params={
                    "api-version": "v1",
                    "include-maintenance-records": "true",
                    "include-attachments": "true",
                    "include-tag-details": "true",
                    "include-related-tags": "true",
                },
            )
        except RequestException, Exception:
            error_description: str = (
                f"Failed to get preventive work order by id: {work_order_id}"
            )
            logger.exception(error_description)
            raise HTTPException(status_code=500, detail=error_description)

        preventive_work_order: PreventiveWorkOrder = parse_response_into_model(
            response=response, model_type=PreventiveWorkOrder
        )
        return preventive_work_order

    @staticmethod
    def get_next_object_list_id_from_preventive_work_order(
        preventive_work_order: PreventiveWorkOrder,
    ) -> str:
        object_list_id: str = (
            WorkOrderService.find_object_list_id_from_preventive_work_order(
                preventive_work_order=preventive_work_order
            )
        )
        next_counter_in_object_list: int = (
            WorkOrderService.get_next_row_counter_from_preventive_work_order(
                preventive_work_order=preventive_work_order
            )
        )
        # Should be in format "OL-1234567-1"
        source_id: str = f"OL-{object_list_id}-{next_counter_in_object_list}"

        return source_id

    @staticmethod
    def find_object_list_id_from_preventive_work_order(
        preventive_work_order: PreventiveWorkOrder,
    ) -> str:
        if not preventive_work_order.maintenance_records:
            if not preventive_work_order.tags_related:
                raise HTTPException(
                    status_code=404,
                    detail="There were no existing maintenance records or a default tags related item in the object list",
                )
            return _extract_object_id_from_source_id(
                preventive_work_order.tags_related[0].source_id
            )

        return _extract_object_id_from_source_id(
            preventive_work_order.maintenance_records[0].source_id
        )

    @staticmethod
    def get_next_row_counter_from_preventive_work_order(
        preventive_work_order: PreventiveWorkOrder,
    ) -> int:
        if (
            not preventive_work_order.maintenance_records
            and not preventive_work_order.tags_related
        ):
            raise HTTPException(
                status_code=404,
                detail="There were no existing maintenance records or a default tags related item in the object list",
            )

        highest_counter: int | None = None

        for items in (
            getattr(preventive_work_order, "tags_related", None),
            getattr(preventive_work_order, "maintenance_records", None),
        ):
            for item in items or []:
                if getattr(item, "source", None) != "ObjectList":
                    continue

                source_id: str = getattr(item, "source_id", None)
                if not source_id:
                    continue

                number: int = _extract_counter_from_source_id(source_id=source_id)
                if highest_counter is None or highest_counter < number:
                    highest_counter = number

        if highest_counter is None:
            raise HTTPException(
                status_code=500,
                detail="No existing value for counter found in work order",
            )

        return highest_counter + 1


def _extract_object_id_from_source_id(source_id: str) -> str:
    # Expected input of format "OL-1234567-1" and the output should be "1234567"
    return source_id.split("-")[1]


def _extract_counter_from_source_id(source_id: str) -> int:
    # Expected input of format "OL-1234567-1" and the output should be 1
    return int(source_id.split("-")[2])
