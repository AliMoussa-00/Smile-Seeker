"""Appointment module"""

from sqlalchemy import Column, DateTime, ForeignKey, String
from datetime import datetime
from models import storage_type
from models.base_model import Base, BaseModel


class Appointments(BaseModel, Base):
    """Defining the Appointment class"""

    if storage_type == "db":
        __tablename__ = "appointments"

        user_id = Column(String(128), ForeignKey("users.id"), nullable=False)
        doctor_id = Column(String(128), ForeignKey("doctors.id"), nullable=False)
        appointment_date = Column(DateTime, default=datetime.utcnow)
        status = Column(String(28), default='scheduled')

    else:
        user_id = ""
        doctor_id = ""
        appointment_date = datetime.utcnow
        status = "scheduled"

    def __init__(self, *args, **kwargs):
        """Initializing the appointment instance"""
        super().__init__(*args, **kwargs)
