"""Analysis domain model."""

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Analysis(BaseModel):
    __tablename__ = "analyses"

    title: Mapped[str] = mapped_column(String(255))
    query: Mapped[str] = mapped_column(Text)
    result_summary: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(50), default="pending")
    dataset_id: Mapped[int] = mapped_column(ForeignKey("datasets.id"))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
