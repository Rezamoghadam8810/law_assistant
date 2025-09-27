from sqlalchemy.orm import declarative_base

# پایه‌ی تمام مدل‌ها
Base = declarative_base()

# 👇 همه مدل‌ها اینجا ایمپورت میشن تا Alembic بتونه ببینه‌شون
from app.models.user import User  # noqa
# از این به بعد هر مدل جدیدی ساختی (مثلاً Role, Case, Document و …)
# همینجا ایمپورت کن
