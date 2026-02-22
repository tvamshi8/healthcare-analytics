from sqlalchemy import Column, String, DateTime, Enum, Boolean, ForeignKey, Text
from sqlalchemy.sql import func
import enum
from ..database import Base


class AlertType(str, enum.Enum):
    VITALS = "vitals"
    RISK = "risk"
    DETERIORATION = "deterioration"
    DISCHARGE = "discharge"


class AlertSeverity(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String(36), primary_key=True)
    type = Column(Enum(AlertType), nullable=False)
    severity = Column(Enum(AlertSeverity), nullable=False)
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=False, index=True)
    patient_name = Column(String(200), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)

    acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime, nullable=True)
    acknowledged_by = Column(String(36), ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, server_default=func.now(), index=True)
