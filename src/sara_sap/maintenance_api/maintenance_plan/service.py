import requests
from requests import Response

from sara_sap.maintenance_api.models import MaintenancePlan


class MaintenancePlanService:
    def __init__(self):
        pass

    def get_maintenance_plan(
        self, maintenance_plan_id: str, access_token: str
    ) -> MaintenancePlan:
        url: str = (
            f"https://api-test.gateway.equinor.com/maintenance-api/maintenance-plans/"
            f"{maintenance_plan_id}"
        )
        response: Response = requests.get(
            url,
            params={"api-version": "v1"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        return response.json()
