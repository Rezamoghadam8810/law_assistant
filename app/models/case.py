from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum


class CaseStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


class Case(Base):
    __tablename__ = "case"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("client.id", ondelete="CASCADE"), nullable=False, index=True)

    title = Column(String(255), nullable=False)         # عنوان پرونده
    description = Column(Text, nullable=True)           # توضیحات کامل
    status = Column(Enum(CaseStatus), default=CaseStatus.OPEN, nullable=False)

    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # رابطه: هر پرونده به یک موکل تعلق داره
    client = relationship("Client", backref="cases", passive_deletes=True)
