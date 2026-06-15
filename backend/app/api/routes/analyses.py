"""Analysis routes."""

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.exceptions import NotFoundError
from app.core.response import ok, paginated
from app.models.analysis import Analysis
from app.models.dataset import Dataset
from app.models.user import User
from app.services.ai_service import generate_analysis, summarize_data
from app.services.dataset_service import get_preview, read_dataframe
from app.utils.pagination import PaginationParams, get_pagination

router = APIRouter(prefix="/analyses", tags=["analyses"])


class CreateAnalysisRequest(BaseModel):
    dataset_id: int
    query: str
    title: str = ""


@router.get("")
async def list_analyses(
    pagination: PaginationParams = Depends(get_pagination),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """List the current user's analyses with pagination."""
    query = select(Analysis).where(Analysis.owner_id == user.id)

    total_result = await db.execute(
        select(func.count()).select_from(query.subquery())
    )
    total = total_result.scalar() or 0

    result = await db.execute(
        query.offset(pagination.offset).limit(pagination.limit)
    )
    analyses = result.scalars().all()
    return paginated(
        items=[
            {
                "id": a.id,
                "title": a.title,
                "status": a.status,
                "created_at": str(a.created_at),
            }
            for a in analyses
        ],
        page=pagination.page,
        per_page=pagination.per_page,
        total=total,
    )


@router.post("")
async def create_analysis(
    body: CreateAnalysisRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Create a new AI-powered analysis on a dataset."""
    # Verify dataset ownership
    ds_result = await db.execute(
        select(Dataset).where(
            Dataset.id == body.dataset_id,
            Dataset.owner_id == user.id,
        )
    )
    dataset = ds_result.scalar_one_or_none()
    if not dataset:
        raise NotFoundError("Dataset", body.dataset_id)

    # Read data and generate analysis
    df = read_dataframe(dataset.file_path)
    data_sample = str(get_preview(df, rows=20))

    result_text = await generate_analysis(
        prompt=body.query,
        context=f"You are analyzing a dataset named '{dataset.name}'. "
        f"Here is a sample of the data:\n{data_sample}",
    )

    analysis = Analysis(
        title=body.title or body.query[:100],
        query=body.query,
        result_summary=result_text,
        status="completed",
        dataset_id=dataset.id,
        owner_id=user.id,
    )
    db.add(analysis)
    await db.flush()

    return ok({"id": analysis.id, "result": result_text})


@router.get("/{analysis_id}")
async def get_analysis(
    analysis_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Get a specific analysis result."""
    result = await db.execute(
        select(Analysis).where(Analysis.id == analysis_id, Analysis.owner_id == user.id)
    )
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise NotFoundError("Analysis", analysis_id)

    return ok({
        "id": analysis.id,
        "title": analysis.title,
        "query": analysis.query,
        "result_summary": analysis.result_summary,
        "status": analysis.status,
        "dataset_id": analysis.dataset_id,
    })


@router.post("/{analysis_id}/summarize")
async def summarize_analysis(
    analysis_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Generate a summary for an existing analysis's dataset."""
    result = await db.execute(
        select(Analysis).where(Analysis.id == analysis_id, Analysis.owner_id == user.id)
    )
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise NotFoundError("Analysis", analysis_id)

    ds_result = await db.execute(
        select(Dataset).where(Dataset.id == analysis.dataset_id)
    )
    dataset = ds_result.scalar_one_or_none()
    if not dataset:
        raise NotFoundError("Dataset", analysis.dataset_id)

    df = read_dataframe(dataset.file_path)
    data_sample = str(get_preview(df, rows=20))
    summary = await summarize_data(data_sample)

    return ok({"analysis_id": analysis.id, "summary": summary})
