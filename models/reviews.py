"""the reviews module"""

from sqlalchemy import Column, ForeignKey, INT, String

from models import storage_type
from models.base_model import Base, BaseModel


class Reviews(BaseModel, Base):
    """Defining the reviews class"""

    if storage_type == "db":
        __tablename__ = "reviews"

        user_id = Column(String(128), ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
        doctor_id = Column(String(128), ForeignKey("doctors.id", ondelete='CASCADE'), nullable=False)
        comment = Column(String(500), nullable=False)
        rating = Column(INT, nullable=False)
    else:
        user_id = ""
        doctor_id = ""
        comment = ""
        rating = 0

    def __init__(self, *args, **kwargs):
        """Initializing the reviews instance"""
        super().__init__(*args, **kwargs)
