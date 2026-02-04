from fastapi import Depends
from fastapi_azure_auth.user import User

from sara_sap.authentication import (
    azure_scheme,
    get_on_behalf_of_token_for_maintenance_api,
)
from sara_sap.maintenance_api.maintenance_plan.api import MaintenancePlanService
from sara_sap.maintenance_api.maintenance_plan.models import MaintenancePlan


class MaintenancePlanController:
    def __init__(self, maintenance_plan_service: MaintenancePlanService) -> None:
        self.maintenance_plan_service: MaintenancePlanService = maintenance_plan_service

    def get_maintenance_plan(
        self, maintenance_plan_id: str, user: User = Depends(azure_scheme)
    ) -> MaintenancePlan:
        access_token: str = get_on_behalf_of_token_for_maintenance_api(
            access_token=user.access_token
        )
        return self.maintenance_plan_service.get_maintenance_plan_by_id(
            maintenance_plan_id=maintenance_plan_id, access_token=access_token
        )
