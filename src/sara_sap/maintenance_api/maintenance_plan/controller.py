from fastapi import Depends
from fastapi_azure_auth.user import User

from sara_sap.authentication import (
    azure_scheme,
    get_on_behalf_of_token_for_maintenance_api,
)
from sara_sap.maintenance_api.maintenance_plan.service import MaintenancePlanService
from sara_sap.maintenance_api.models import Dummy


class MaintenancePlanController:
    def __init__(self) -> None:
        self.maintenance_plan_service: MaintenancePlanService = MaintenancePlanService()

    def get_maintenance_plan(
        self, maintenance_plan_id: str, user: User = Depends(azure_scheme)
    ) -> None:
        access_token: str = get_on_behalf_of_token_for_maintenance_api(
            user.access_token
        )
        return self.maintenance_plan_service.get_maintenance_plan(
            maintenance_plan_id=maintenance_plan_id, access_token=access_token
        )
