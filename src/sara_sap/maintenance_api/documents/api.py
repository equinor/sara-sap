from http import HTTPStatus
from typing import List, Dict

from fastapi import HTTPException
from fastapi import Response as FastAPIResponse
from loguru import logger
from requests import Response, RequestException

from sara_sap.maintenance_api.documents.enums import RelationshipType
from sara_sap.maintenance_api.documents.models import Document, DocumentCreated
from sara_sap.utilities.parse_response import parse_response_into_model
from sara_sap.utilities.request_handler import get, post


class DocumentsService:
    @staticmethod
    def create_document(
        document_title: str,
        document_description: str,
        access_token: str,
        status_id: str = "CV",
        document_type: str = "B30",
    ) -> DocumentCreated:
        url: str = "https://api-test.gateway.equinor.com/maintenance-api/documents"

        request_body: dict = {
            "documentTitle": document_title,
            "documentType": document_type,
            "statusId": status_id,
            "text": document_description,
        }

        try:
            response: Response = post(
                url=url,
                headers={"Authorization": f"Bearer {access_token}"},
                params={"api-version": "v1"},
                json_body=request_body,
            )
            return parse_response_into_model(
                response=response, model_type=DocumentCreated
            )
        except RequestException, Exception:
            error_description: str = "Failed to create new document"
            logger.exception(error_description)
            raise HTTPException(status_code=500, detail=error_description)

    @staticmethod
    def add_document_relationship_to_maintenance_record(
        document_id: str, maintenance_record_id: str, access_token: str
    ) -> FastAPIResponse:
        url: str = (
            f"https://api-test.gateway.equinor.com/maintenance-api/document-relationships/"
            f"{RelationshipType.MAINTENANCE_RECORDS.value}/{maintenance_record_id}"
        )
        request_body: List[Dict] = [{"documentId": document_id}]

        try:
            _ = post(
                url=url,
                headers={"Authorization": f"Bearer {access_token}"},
                params={"api-version": "v1"},
                json_body=request_body,
            )
            return FastAPIResponse(status_code=HTTPStatus.CREATED)
        except RequestException, Exception:
            error_description: str = (
                f"Failed to add document relationship between maintenance record id {maintenance_record_id} "
                f"and document {document_id}"
            )
            logger.exception(error_description)
            raise HTTPException(status_code=500, detail=error_description)

    @staticmethod
    def get_document_relationships(
        relationship_type: RelationshipType, source_id: str, access_token: str
    ) -> List[Document]:
        url: str = (
            f"https://api-test.gateway.equinor.com/maintenance-api/document-relationships/"
            f"{relationship_type.value}/{source_id}"
        )

        try:
            response: Response = get(
                url=url,
                headers={"Authorization": f"Bearer {access_token}"},
                params={"include-attachments": True, "api-version": "v1"},
            )
            return parse_response_into_model(
                response=response, model_type=List[Document]
            )
        except RequestException, Exception:
            error_description: str = (
                f"Failed to get document relationships for relationship type {relationship_type} "
                f"and source_id {source_id}"
            )
            logger.exception(error_description)
            raise HTTPException(status_code=500, detail=error_description)
