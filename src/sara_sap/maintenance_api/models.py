from typing import List

from pydantic import BaseModel, Field


class WorkOrderCall(BaseModel):
    call_nr: int = Field(alias="callNr")
    planned_date: str = Field(alias="plannedDate")
    is_executed: bool = Field(alias="isExecuted")
    preventive_work_order_id: str = Field(alias="preventiveWorkOrderId")
    due_packages: str = Field(alias="duePackages")
    scheduling_type_status: str = Field(alias="schedulingTypeStatus")
    call_date: str = Field(alias="callDate")
    completion_date: str = Field(alias="completionDate")


class MaintenanceItem(BaseModel):
    maintenance_strategy_id: str = Field(alias="maintenanceStrategyId")
    maintenance_strategy: str = Field(alias="maintenanceStrategy")
    status: str = Field(alias="status")
    calls: List[WorkOrderCall] = Field(alias="calls")
    maintenance_activity_type_id: str = Field(alias="maintenanceActivityTypeId")
    maintenance_activity_type: str = Field(alias="maintenanceActivityType")
    priority_id: str = Field(alias="priorityId")
    maintenance_plan_item_id: str = Field(alias="maintenancePlanItemId")
    maintenance_plan_item: str = Field(alias="maintenancePlanItem")
    maintenance_plan_id: str = Field(alias="maintenancePlanId")
    planning_plant_id: str = Field(alias="planningPlantId")
    main_tag_id: str = Field(alias="mainTagId")
    main_tag_plant_id: str = Field(alias="mainTagPlantId")
    changed_date_time: str = Field(alias="changedDateTime")


class MaintenancePlan(BaseModel):
    maintenance_plan_id: str = Field(alias="maintenancePlanId")
    maintenance_plan: str = Field(alias="maintenancePlan")
    is_active: bool = Field(alias="isActive")
    items: List[MaintenanceItem] = Field(alias="items")
