from typing import List

from pydantic import BaseModel, ConfigDict, Field

from sara_sap.maintenance_api.activity_report.enums import WorkOrderRelationship


class MaintenanceRecordActivity(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    activity_id: str = Field(alias="activityId")
    title: str = Field(alias="title")
    text: str | None = Field(alias="text")
    is_readonly_text: bool = Field(alias="isReadonlyText")
    activity_code_id: str = Field(alias="activityCodeId")
    activity_code: str = Field(alias="activityCode")
    activity_code_group_id: str = Field(alias="activityCodeGroupId")
    activity_code_group: str = Field(alias="activityCodeGroup")
    start_date_time: str | None = Field(alias="startDateTime")
    end_date_time: str | None = Field(alias="endDateTime")


class Link(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    enclosure: str = Field(alias="enclosure")
    documentEnclosure: str = Field(alias="documentEnclosure", default="")


class Attachment(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    attachment_id: str = Field(alias="attachmentId")
    file_name: str = Field(alias="fileName")
    file_size: str = Field(alias="fileSize")
    mime_type: str = Field(alias="mimeType")
    created_date_time: str | None = Field(alias="createdDateTime")
    changed_date_time: str | None = Field(alias="changedDateTime")
    document_title: str | None = Field(alias="documentTitle")
    document_type: str | None = Field(alias="documentType")
    document_number: str | None = Field(alias="documentNumber")
    document_created_date: str | None = Field(alias="documentCreatedDate")
    links: Link = Field(alias="_links")


class Status(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    status_id: str = Field(alias="statusId")
    status: str = Field(alias="status")
    status_order: int | None = Field(alias="statusOrder")
    is_active: bool = Field(alias="isActive")
    activated_date_time: str | None = Field(alias="activatedDateTime")


class Measurement(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    measurement_id: str = Field(alias="measurementId")
    maintenance_record_id: str | None = Field(alias="maintenanceRecordId")
    measuring_point_id: str = Field(alias="measuringPointId")
    measurement_date_time: str = Field(alias="measurementDateTime")
    measurement_title: str = Field(alias="measurementTitle")
    quantitative_reading: float = Field(alias="quantitativeReading")
    quantitative_reading_unit_id: str = Field(alias="quantitativeReadingUnitId")
    qualitative_code_group_id: str = Field(alias="qualitativeCodeGroupId")
    qualitative_code_id: str = Field(alias="qualitativeCodeId")
    processing_status_id: str = Field(alias="processingStatusId")
    work_order_id: str | None = Field(alias="workOrderId")


class UrlReference(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    url_reference_id: str = Field(alias="urlReferenceId")
    url: str = Field(alias="url")
    title: str = Field(alias="title")
    document_title: str = Field(alias="documentTitle")
    document_type: str = Field(alias="documentType")
    document_number: str = Field(alias="documentNumber")
    document_created_date: str | None = Field(alias="documentCreatedDate")


class MaintenanceRecord(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    record_id: str = Field(alias="recordId")
    tag_id: str | None = Field(alias="tagId")
    tag_plant_id: str = Field(alias="tagPlantId")
    equipment_id: str = Field(alias="equipmentId")
    title: str = Field(alias="title")
    text: str = Field(alias="text")
    is_open: bool = Field(alias="isOpen")
    work_center_id: str = Field(alias="workCenterId")
    work_center_plant_id: str = Field(alias="workCenterPlantId")
    active_status_ids: str = Field(alias="activeStatusIds")
    maintenance_record_type_id: str = Field(alias="maintenanceRecordTypeId")
    created_by_id: str = Field(alias="createdById")
    created_by: str | None = Field(alias="createdBy")
    created_by_email: str | None = Field(alias="createdByEmail")
    activities: List[MaintenanceRecordActivity] = Field(
        alias="activities", default_factory=list
    )
    attachments: List[Attachment] = Field(alias="attachments", default_factory=list)
    url_references: List[UrlReference] = Field(
        alias="urlReferences", default_factory=list
    )
    statuses: List[Status] = Field(alias="statuses", default_factory=list)
    measurements: List[Measurement] = Field(alias="measurements", default_factory=list)
    created_date_time: str | None = Field(alias="createdDateTime")


class MaintenanceRecordActivityCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(alias="title")
    text: str = Field(alias="text")
    activity_code_id: str = Field(alias="activityCodeId")
    activity_code_group_id: str = Field(alias="activityCodeGroupId")
    start_date_time: str | None = Field(alias="startDateTime")
    end_date_time: str | None = Field(alias="endDateTime")


class TechnicalFeedbackParameters(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    status_id: str = Field(alias="statusId")
    reason_id: str | None = Field(alias="reasonId")


class RelatedWorkOrderRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    work_order_id: str = Field(alias="workOrderId")
    source: WorkOrderRelationship = Field(alias="source")
    source_id: str = Field(alias="sourceId")
    technical_feedback_parameters: TechnicalFeedbackParameters = Field(
        alias="technicalFeedbackParameters"
    )


class CharacteristicsAddActivityReport(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    characteristics_id: str = Field(alias="characteristicsId")
    value_id: str = Field(alias="valueId")


class Characteristics(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    class_id: str = Field(alias="classId")
    characteristics: List[CharacteristicsAddActivityReport] = Field(
        alias="characteristics"
    )


class CreateActivityReportRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(alias="title")
    text: str | None = Field(alias="text")
    tag_id: str | None = Field(alias="tagId")
    tag_plant_id: str = Field(alias="tagPlantId")
    equipment_id: str = Field(alias="equipmentId")
    work_center_id: str = Field(alias="workCenterId")
    work_center_plant_id: str = Field(alias="workCenterPlantId")
    is_open: bool = Field(alias="isOpen")
    created_date_time: str | None = Field(alias="createdDateTime")
    activities: List[MaintenanceRecordActivity] = Field(alias="activities")
    related_work_order: RelatedWorkOrderRequest = Field(alias="relatedWorkOrder")
    characteristics: Characteristics = Field(alias="characteristics")


class ActivityReportStatusUpdateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    op: str = Field(alias="op", default="replace")
    path: str = Field(alias="path", default="/isActive")
    value: str | bool = Field(
        alias="value", default=True
    )  # If it is an "activation" or "deactivation" status


class WorkOrderCall(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    call_nr: int = Field(alias="callNr")
    planned_date: str | None = Field(alias="plannedDate", default=None)
    is_executed: bool = Field(alias="isExecuted")
    preventive_work_order_id: str = Field(alias="preventiveWorkOrderId")
    due_packages: str = Field(alias="duePackages")
    scheduling_type_status: str = Field(alias="schedulingTypeStatus")
    call_date: str | None = Field(alias="callDate")
    completion_date: str | None = Field(alias="completionDate")


class MaintenancePlanItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    maintenance_strategy_id: str = Field(alias="maintenanceStrategyId")
    maintenance_strategy: str = Field(alias="maintenanceStrategy")
    status: str = Field(alias="status")
    calls: List[WorkOrderCall] = Field(alias="calls")
    maintenance_activity_type_id: str = Field(alias="maintenanceActivityTypeId")
    maintenance_activity_type: str = Field(alias="maintenanceActivityType")
    priority_id: str | None = Field(alias="priorityId")
    maintenance_plan_item_id: str = Field(alias="maintenancePlanItemId")
    maintenance_plan_item: str = Field(alias="maintenancePlanItem")
    maintenance_plan_id: str = Field(alias="maintenancePlanId")
    planning_plant_id: str = Field(alias="planningPlantId")
    main_tag_id: str | None = Field(alias="mainTagId")
    main_tag_plant_id: str = Field(alias="mainTagPlantId")
    changed_date_time: str | None = Field(alias="changedDateTime")


class MaintenancePlan(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    maintenance_plan_id: str = Field(alias="maintenancePlanId")
    maintenance_plan: str = Field(alias="maintenancePlan")
    is_active: bool = Field(alias="isActive")
    items: List[MaintenancePlanItem] = Field(alias="items")
