from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

from app.db.base_class import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=True)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    # 🔑 برای Auth
    hashed_password = Column(String, nullable=False)  # پسورد هش‌شده

    otp_code = Column(String, nullable=True)
    otp_expiry = Column(Integer,nullable=True)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)  # وضعیت کاربر (فعال/غیرفعال)
    role = Column(String, default="user")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    subscription_plan = Column(String, nullable=False, default="free")
