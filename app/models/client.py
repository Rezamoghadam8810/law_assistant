from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, UniqueConstraint, Index
from app.db.base_class import Base

class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    lawyer_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)

    name = Column(String(200), nullable=False)
    email = Column(String(320), nullable=True)
    phone = Column(String(50),  nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("lawyer_id", "email", name="uq_client_email_per_lawyer"),
        Index("ix_client_lawyer_id_name", "lawyer_id", "name"),
    )
