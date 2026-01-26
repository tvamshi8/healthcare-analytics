from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class AlertType(str, Enum):
    VITALS = "vitals"
    RISK = "risk"
    DETERIORATION = "deterioration"
    DISCHARGE = "discharge"


class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertResponse(BaseModel):
    id: str
    type: AlertType
    severity: AlertSeverity
    patient_id: str
    patient_name: str
    title: str
    message: str
    acknowledged: bool
    acknowledged_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
