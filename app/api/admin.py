from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.schemas.document import DocumentResponse
from app.services.knowledge_base_service import KnowledgeBaseService
from uuid import UUID
from fastapi import status

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.post(
    "/documents",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Upload and index a knowledge base document.
    """

    knowledge_base_service = KnowledgeBaseService(db)

    return knowledge_base_service.upload_document(
        file=file,
        uploaded_by=current_user.id,
    )


@router.get(
    "/documents",
    response_model=list[DocumentResponse],
)
def list_documents(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieve all indexed documents.
    """

    knowledge_base_service = KnowledgeBaseService(db)

    return knowledge_base_service.list_documents()



@router.delete(
    "/documents/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document(
    document_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete an indexed document.
    """

    knowledge_base_service = KnowledgeBaseService(db)

    knowledge_base_service.delete_document(document_id)