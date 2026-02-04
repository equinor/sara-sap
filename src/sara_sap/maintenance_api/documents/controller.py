from http import HTTPStatus
from typing import List

from fastapi import Depends
from fastapi import Response as FastAPIResponse
from fastapi_azure_auth.user import User

from sara_sap.authentication import (
    get_on_behalf_of_token_for_maintenance_api,
    azure_scheme,
)
from sara_sap.maintenance_api.documents.api import DocumentsService
from sara_sap.maintenance_api.documents.enums import RelationshipType
from sara_sap.maintenance_api.documents.models import Document, DocumentCreated


class DocumentsController:
    def __init__(self, documents_service: DocumentsService) -> None:
        self.documents_service: DocumentsService = documents_service

    def create_document(
        self,
        document_title: str,
        document_description: str,
        user: User = Depends(azure_scheme),
    ) -> DocumentCreated:
        access_token: str = get_on_behalf_of_token_for_maintenance_api(
            access_token=user.access_token
        )
        return self.documents_service.create_document(
            document_title=document_title,
            document_description=document_description,
            access_token=access_token,
        )

    def add_document_relationship_to_maintenance_record(
        self,
        document_id: str,
        maintenance_record_id: str,
        user: User = Depends(azure_scheme),
    ) -> FastAPIResponse:
        access_token: str = get_on_behalf_of_token_for_maintenance_api(
            access_token=user.access_token
        )

        self.documents_service.add_document_relationship_to_maintenance_record(
            document_id=document_id,
            maintenance_record_id=maintenance_record_id,
            access_token=access_token,
        )

        return FastAPIResponse(
            status_code=HTTPStatus.NO_CONTENT,
        )

    def get_document_maintenance_record_relationships(
        self,
        maintenance_record_id: str,
        user: User = Depends(azure_scheme),
    ) -> List[Document]:
        access_token: str = get_on_behalf_of_token_for_maintenance_api(
            access_token=user.access_token
        )
        relationships: List[Document] = (
            self.documents_service.get_document_relationships(
                relationship_type=RelationshipType.MAINTENANCE_RECORDS,
                source_id=maintenance_record_id,
                access_token=access_token,
            )
        )
        return relationships
