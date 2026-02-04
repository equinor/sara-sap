from datetime import datetime, timezone

from fastapi import HTTPException
from requests import Response, get

from sara_sap.maintenance_api.maintenance_plan.models import (
    MaintenancePlan,
    MaintenancePlanItem,
    WorkOrderCall,
)
from sara_sap.utilities.parse_response import parse_response_into_model


class MaintenancePlanService:
    @staticmethod
    def get_maintenance_plan_by_id(
        maintenance_plan_id: str, access_token: str
    ) -> MaintenancePlan:
        url: str = (
            f"https://api-test.gateway.equinor.com/maintenance-api/maintenance-plans/"
            f"{maintenance_plan_id}"
        )
        response: Response = get(
            url=url,
            headers={"Authorization": f"Bearer {access_token}"},
            params={"api-version": "v1"},
        )

        maintenance_plan: MaintenancePlan = parse_response_into_model(
            response=response, model_type=MaintenancePlan
        )
        return maintenance_plan

    @staticmethod
    def find_maintenance_item_by_id(
        maintenance_plan: MaintenancePlan, item_id: str
    ) -> MaintenancePlanItem:
        for item in maintenance_plan.items:
            if item.maintenance_plan_item_id == item_id:
                return item
        raise HTTPException(status_code=404, detail="Maintenance plan item not found")

    @staticmethod
    def select_next_called_work_order(
        maintenance_plan_item: MaintenancePlanItem,
    ) -> WorkOrderCall:
        today: datetime = datetime.now(timezone.utc)

        candidates: list[tuple[datetime, WorkOrderCall]] = []
        for call in maintenance_plan_item.calls:
            if _normalize_status(call.scheduling_type_status) != "Scheduled Called":
                continue
            planned_time: datetime = _parse_planned_datetime(call.planned_date)
            if planned_time < today:
                continue
            candidates.append((planned_time, call))

        if not candidates:
            raise HTTPException(
                status_code=404, detail="No scheduled calls found in the future"
            )

        candidates.sort(key=lambda x: x[0])
        return candidates[0][1]


def _normalize_status(value: str | None) -> str:
    return " ".join((value or "").split())


def _parse_planned_datetime(value: str) -> datetime:
    if not value:
        raise HTTPException(status_code=500, detail="Value cannot be empty")
    try:
        text = value.strip()

        if len(text) == 10 and text[4] == "-" and text[7] == "-":
            return datetime.fromisoformat(text).replace(tzinfo=timezone.utc)

        if text.endswith("Z"):
            text = text[:-1] + "+00:00"

        dt: datetime = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        raise HTTPException(status_code=500, detail=f"Invalid datetime format: {value}")
