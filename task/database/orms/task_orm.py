from sqlalchemy import String, Column, Boolean, DateTime, ForeignKey
from task.root.utils.abstract_base import AbstractBase
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy.orm import relationship


class Task(AbstractBase):
    __tablename__ = "Tasks"
    task_uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_uid = Column(UUID(as_uuid=True), ForeignKey("users.user_uid"), default=uuid4)
    title = Column(String, nullable=False)
    detail = Column(String, nullable=True)
    is_completed = Column(Boolean, nullable=False)
    status = Column(String, nullable=False)
    completed_date_utc = Column(DateTime(), nullable=True)
    owner = relationship("User")
