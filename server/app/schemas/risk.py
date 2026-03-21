from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from enum import Enum


class RecommendationType(str, Enum):
    INTERVENTION = "intervention"
    FOLLOW_UP = "follow-up"
    REFERRAL = "referral"
    EDUCATION = "education"


class RecommendationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class RecommendationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    DECLINED = "declined"


class RiskFactorResponse(BaseModel):
    id: str
    factor: str
    description: str
    contribution: float
    severity: str

    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    id: str
    type: RecommendationType
    title: str
    description: str
    priority: RecommendationPriority
    status: RecommendationStatus
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RiskAssessmentResponse(BaseModel):
    id: str
    patient_id: str
    risk_score: int
    risk_level: str
    readmission_probability: float
    confidence: float
    assessed_at: datetime
    risk_factors: List[RiskFactorResponse] = []
    recommendations: List[RecommendationResponse] = []

    class Config:
        from_attributes = True
