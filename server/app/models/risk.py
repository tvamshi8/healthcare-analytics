from sqlalchemy import Column, String, Integer, Float, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base


class RecommendationType(str, enum.Enum):
    INTERVENTION = "intervention"
    FOLLOW_UP = "follow-up"
    REFERRAL = "referral"
    EDUCATION = "education"


class RecommendationPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class RecommendationStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    DECLINED = "declined"


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(String(36), primary_key=True)
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=False, index=True)
    risk_score = Column(Integer, nullable=False)
    risk_level = Column(String(20), nullable=False)
    readmission_probability = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    assessed_at = Column(DateTime, server_default=func.now())

    patient = relationship("Patient", back_populates="risk_assessments")
    risk_factors = relationship("RiskFactor", back_populates="assessment", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="assessment", cascade="all, delete-orphan")


class RiskFactor(Base):
    __tablename__ = "risk_factors"

    id = Column(String(36), primary_key=True)
    assessment_id = Column(String(36), ForeignKey("risk_assessments.id"), nullable=False)
    factor = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    contribution = Column(Float, nullable=False)  # SHAP value or percentage
    severity = Column(String(20), nullable=False)

    assessment = relationship("RiskAssessment", back_populates="risk_factors")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String(36), primary_key=True)
    assessment_id = Column(String(36), ForeignKey("risk_assessments.id"), nullable=False)
    type = Column(Enum(RecommendationType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(Enum(RecommendationPriority), default=RecommendationPriority.MEDIUM)
    status = Column(Enum(RecommendationStatus), default=RecommendationStatus.PENDING)

    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
    completed_by = Column(String(36), nullable=True)

    assessment = relationship("RiskAssessment", back_populates="recommendations")
