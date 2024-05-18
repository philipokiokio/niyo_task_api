from sqlalchemy import String, Column
from task.root.utils.abstract_base import AbstractBase
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy.orm import relationship


class User(AbstractBase):
    __tablename__ = "users"
    user_uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    tasks = relationship("Task", back_populates="owner")


2
