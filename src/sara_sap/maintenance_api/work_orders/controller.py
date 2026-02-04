from fastapi import Depends
from fastapi_azure_auth.user import User

from sara_sap.authentication import (
    azure_scheme,
    get_on_behalf_of_token_for_maintenance_api,
)
from sara_sap.maintenance_api.work_orders.api import WorkOrderService
from sara_sap.maintenance_api.work_orders.models import PreventiveWorkOrder


class WorkOrderController:
    def __init__(self, work_order_service: WorkOrderService) -> None:
        self.work_order_service: WorkOrderService = work_order_service

    def get_preventive_work_order_by_id(
        self, work_order_id: str, user: User = Depends(azure_scheme)
    ) -> PreventiveWorkOrder:
        access_token: str = get_on_behalf_of_token_for_maintenance_api(
            access_token=user.access_token
        )
        return self.work_order_service.get_preventive_work_order_by_id(
            work_order_id=work_order_id, access_token=access_token
        )
