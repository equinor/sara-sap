from pydantic import BaseModel, Field, ConfigDict


class ActivityReportCreated(BaseModel):
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
    created_date_time: str | None = Field(alias="createdDateTime")


class UploadedFile(BaseModel):
    maintenance_record_id: str = Field(...)
    document_id: str = Field(...)
    file_name: str = Field(...)
