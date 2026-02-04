from typing import List

from pydantic import BaseModel, Field, ConfigDict

from sara_sap.maintenance_api.maintenance_plan.models import Attachment


class Document(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    document_id: str = Field(alias="documentId")
    document_number: str = Field(alias="documentNumber")
    document_type: str = Field(alias="documentType")
    document_part: str | None = Field(alias="documentPart")
    document_version: str | None = Field(alias="documentVersion")
    document_title: str = Field(alias="documentTitle")
    attachments: List[Attachment] | None = Field(
        alias="attachments", default_factory=list
    )
    characteristics: List[str] | None = Field(
        alias="characteristics", default_factory=list
    )
    document_created_date: str | None = Field(alias="documentCreatedDate")


class DocumentCreated(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    document_id: str = Field(alias="documentId")
    document_title: str | None = Field(alias="documentTitle")
    document_number: str = Field(alias="documentNumber")
    document_type: str = Field(alias="documentType")
    document_part: str | None = Field(alias="documentPart")
    document_created_date: str | None = Field(alias="documentCreatedDate")
    text: str = Field(alias="text")
    status_id: str = Field(alias="statusId")
    status_text: str = Field(alias="statusText")
