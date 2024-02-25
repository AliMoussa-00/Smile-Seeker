"""defining the location module"""
from sqlalchemy import Column, Float, ForeignKey, String

from models import storage_type
from models.base_model import Base, BaseModel


class Location(BaseModel, Base):
    """Defining the Location class"""

    if storage_type == "db":
        __tablename__ = "location"
        doctor_id = Column(String(128), ForeignKey("doctors.id"), nullable=False)
        address = Column(String(128), nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

    else:
        doctor_id = ""
        address = ""
        latitude = 0.0
        longitude = 0.0

    def __init__(self, *args, **kwargs):
        """Initializing the location instance"""
        super().__init__(*args, **kwargs)
