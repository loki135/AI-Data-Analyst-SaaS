"""Dataset management routes."""

from typing import Any

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.exceptions import NotFoundError
from app.core.response import ok, paginated
from app.models.dataset import Dataset
from app.models.user import User
from app.services.dataset_service import (
    extract_metadata,
    get_preview,
    read_dataframe,
    validate_file_extension,
)
from app.utils.pagination import PaginationParams, get_pagination

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.get("")
async def list_datasets(
    pagination: PaginationParams = Depends(get_pagination),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """List the current user's datasets with pagination."""
    query = select(Dataset).where(Dataset.owner_id == user.id)

    total_result = await db.execute(
        select(func.count()).select_from(query.subquery())
    )
    total = total_result.scalar() or 0

    result = await db.execute(
        query.offset(pagination.offset).limit(pagination.limit)
    )
    datasets = result.scalars().all()
    return paginated(
        items=[
            {"id": d.id, "name": d.name, "row_count": d.row_count}
            for d in datasets
        ],
        page=pagination.page,
        per_page=pagination.per_page,
        total=total,
    )


@router.post("")
async def upload_dataset(
    file: UploadFile,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Upload and process a new dataset."""
    filename = file.filename or "unknown"
    validate_file_extension(filename)

    # Save file (simplified — use object storage in production)
    import os

    file_path = f"/tmp/datasets/{user.id}/{filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    df = read_dataframe(file_path)
    metadata = extract_metadata(df)

    dataset = Dataset(
        name=filename,
        file_path=file_path,
        file_size_bytes=len(content),
        row_count=metadata["row_count"],
        column_count=metadata["column_count"],
        owner_id=user.id,
    )
    db.add(dataset)
    await db.flush()

    return ok({"id": dataset.id, "metadata": metadata})


@router.get("/{dataset_id}")
async def get_dataset(
    dataset_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Get dataset details and metadata."""
    result = await db.execute(
        select(Dataset).where(Dataset.id == dataset_id, Dataset.owner_id == user.id)
    )
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise NotFoundError("Dataset", dataset_id)

    df = read_dataframe(dataset.file_path)
    metadata = extract_metadata(df)
    preview = get_preview(df)

    return ok({
        "id": dataset.id,
        "name": dataset.name,
        "metadata": metadata,
        "preview": preview,
    })
