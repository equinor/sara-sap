from typing import Dict, List

from pydantic import BaseModel, ConfigDict, Field

from sara_sap.maintenance_api.activity_report.enums import WorkOrderRelationship
from sara_sap.maintenance_api.work_orders.enums import PriorityId


class TagRelatedToWorkOrder(BaseModel):
    source: WorkOrderRelationship = Field(alias="source")
    source_id: str = Field(alias="sourceId")
    equipment_id: str = Field(alias="equipmentId")
    equipment: str = Field(alias="equipment")
    tag_id: str | None = Field(alias="tagId", default="")
    tag_plant_id: str = Field(alias="tagPlantId")
    location_id: str = Field(alias="locationId")
    location: str = Field(alias="location")
    related_operations: List[str] = Field(
        alias="relatedOperations", default_factory=list
    )


class MaintenanceRecordMinimalWithActiveStatusIds(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    record_id: str = Field(alias="recordId")
    record_resource: str = Field(alias="recordResource")
    tag_id: str | None = Field(alias="tagId")
    tag_plant_id: str = Field(alias="tagPlantId")
    tag: str = Field(alias="tag")
    title: str = Field(alias="title")
    source: WorkOrderRelationship = Field(alias="source")
    source_id: str = Field(alias="sourceId")
    active_status_ids: str = Field(alias="activeStatusIds")
    related_operations: List[str] = Field(
        alias="relatedOperations", default_factory=list
    )
    location_id: str = Field(alias="locationId")
    location: str = Field(alias="location")
    equipment_id: str = Field(alias="equipmentId")
    equipment: str = Field(alias="equipment")


class PreventiveWorkOrder(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    cost_wbs_id: str = Field(alias="costWBSId")
    cost_wbs: str = Field(alias="costWBS")
    additional_cost_wbs_id: str = Field(alias="additionalCostWBSId")
    additional_cost_wbs: str = Field(alias="additionalCostWBS")
    text: str = Field(alias="text")
    work_order_type_id: str = Field(alias="workOrderTypeId")
    work_center: str = Field(alias="workCenter")
    work_order_id: str = Field(alias="workOrderId")
    tag_id: str | None = Field(alias="tagId")
    tag_plant_id: str = Field(alias="tagPlantId")
    tag: str = Field(alias="tag")
    title: str = Field(alias="title")
    work_center_id: str = Field(alias="workCenterId")
    work_center_plant_id: str = Field(alias="workCenterPlantId")
    location_id: str = Field(alias="locationId")
    plant_id: str = Field(alias="plantId")
    planning_plant_id: str = Field(alias="planningPlantId")
    planner_group_id: str = Field(alias="plannerGroupId")
    active_status_ids: str = Field(alias="activeStatusIds")
    maintenance_type_id: str = Field(alias="maintenanceTypeId")
    maintenance_type: str = Field(alias="maintenanceType")
    planned_date: str | None = Field(alias="plannedDate", default=None)
    priority_id: PriorityId | None = Field(alias="priorityId")
    revision_id: str = Field(alias="revisionId")
    revision: str = Field(alias="revision")
    basic_start_date_time: str | None = Field(alias="basicStartDateTime")
    basic_end_date_time: str | None = Field(alias="basicEndDateTime")
    created_date_time: str | None = Field(alias="createdDateTime")
    changed_date_time: str | None = Field(alias="changedDateTime")
    sort_field: str = Field(alias="sortField")
    costs: float | None = Field(alias="costs")
    costs_currency: str = Field(alias="costsCurrency")
    is_open: bool = Field(alias="isOpen")
    operations: List[Dict] | None = Field(alias="operations", default_factory=list)
    service_operations: List[Dict] | None = Field(alias="serviceOperations")
    statuses: List[Dict] | None = Field(alias="statuses", default_factory=list)
    tags_related: List[TagRelatedToWorkOrder] | None = Field(
        alias="tagsRelated", default_factory=list
    )
    maintenance_records: List[MaintenanceRecordMinimalWithActiveStatusIds] = Field(
        alias="maintenanceRecords", default_factory=list
    )
    maintenance_plan: Dict | None = Field(alias="maintenancePlan", default_factory=dict)
    tag_details: Dict | None = Field(alias="tagDetails", default_factory=dict)
    attachments: List[Dict] | None = Field(alias="attachments", default_factory=list)
    measurements: List[Dict] | None = Field(alias="measurements", default_factory=list)
    estimated_costs: List[Dict] | None = Field(
        alias="estimatedCosts", default_factory=list
    )
    due_date: str | None = Field(alias="dueDate", default=None)
    is_production_critical: str = Field(alias="isProductionCritical")
    is_hse_critical: str = Field(alias="isHSECritical")
    planner_group: str = Field(alias="plannerGroup")
    person_responsible_id: str | None = Field(alias="personResponsibleId", default="")
    person_responsible_email: str | None = Field(
        alias="personResponsibleEmail", default=""
    )
