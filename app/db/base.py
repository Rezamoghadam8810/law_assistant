from app.db.base_class import Base  # 👈 فقط Base از اینجا



# 👇 همه مدل‌ها اینجا ایمپورت میشن تا Alembic بتونه ببینه‌شون
from app.models.user import User  # noqa
# از این به بعد هر مدل جدیدی ساختی (مثلاً Role, Case, Document و …)
# همینجا ایمپورت کن
from app.models.client import Client
from app.models.case import Case
