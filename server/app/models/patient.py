from sqlalchemy import Column, String, Integer, Float, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class PatientStatus(str, enum.Enum):
    ADMITTED = "admitted"
    DISCHARGED = "discharged"
    TRANSFERRED = "transferred"
    DECEASED = "deceased"


class ClinicalStatus(str, enum.Enum):
    STABLE = "stable"
    WATCH = "watch"
    CRITICAL = "critical"


class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Patient(Base):
    __tablename__ = "patients"

    id = Column(String(36), primary_key=True)
    mrn = Column(String(20), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(Enum(Gender), nullable=False)

    admission_date = Column(DateTime, nullable=False)
    discharge_date = Column(DateTime, nullable=True)
    department = Column(String(100), nullable=False)
    room = Column(String(20), nullable=False)
    bed = Column(String(10), nullable=False)
    attending_physician = Column(String(100), nullable=False)

    primary_diagnosis = Column(String(255), nullable=False)
    risk_score = Column(Integer, default=0)
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.LOW)
    clinical_status = Column(Enum(ClinicalStatus), default=ClinicalStatus.STABLE)
    status = Column(Enum(PatientStatus), default=PatientStatus.ADMITTED)

    insurance_provider = Column(String(100), nullable=True)
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_relationship = Column(String(50), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    diagnoses = relationship("Diagnosis", back_populates="patient", cascade="all, delete-orphan")
    vital_signs = relationship("VitalSign", back_populates="patient", cascade="all, delete-orphan")
    lab_results = relationship("LabResult", back_populates="patient", cascade="all, delete-orphan")
    risk_assessments = relationship("RiskAssessment", back_populates="patient", cascade="all, delete-orphan")


class DiagnosisType(str, enum.Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    COMORBIDITY = "comorbidity"


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(String(36), primary_key=True)
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=False)
    code = Column(String(20), nullable=False)  # ICD-10 code
    description = Column(String(255), nullable=False)
    type = Column(Enum(DiagnosisType), default=DiagnosisType.SECONDARY)
    diagnosed_at = Column(DateTime, server_default=func.now())

    patient = relationship("Patient", back_populates="diagnoses")


class VitalSign(Base):
    __tablename__ = "vital_signs"

    id = Column(String(36), primary_key=True)
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)

    heart_rate = Column(Integer, nullable=False)
    blood_pressure_systolic = Column(Integer, nullable=False)
    blood_pressure_diastolic = Column(Integer, nullable=False)
    temperature = Column(Float, nullable=False)
    respiratory_rate = Column(Integer, nullable=False)
    oxygen_saturation = Column(Float, nullable=False)
    pain_level = Column(Integer, nullable=True)

    patient = relationship("Patient", back_populates="vital_signs")


class LabResultStatus(str, enum.Enum):
    NORMAL = "normal"
    LOW = "low"
    HIGH = "high"
    CRITICAL = "critical"


class LabResult(Base):
    __tablename__ = "lab_results"

    id = Column(String(36), primary_key=True)
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=False, index=True)
    test_name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    normal_min = Column(Float, nullable=False)
    normal_max = Column(Float, nullable=False)
    status = Column(Enum(LabResultStatus), default=LabResultStatus.NORMAL)
    timestamp = Column(DateTime, server_default=func.now())
    notes = Column(Text, nullable=True)

    patient = relationship("Patient", back_populates="lab_results")
