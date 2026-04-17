from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class PatientStatus(str, Enum):
    ADMITTED = "admitted"
    DISCHARGED = "discharged"
    TRANSFERRED = "transferred"
    DECEASED = "deceased"


class ClinicalStatus(str, Enum):
    STABLE = "stable"
    WATCH = "watch"
    CRITICAL = "critical"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DiagnosisType(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    COMORBIDITY = "comorbidity"


class DiagnosisResponse(BaseModel):
    id: str
    code: str
    description: str
    type: DiagnosisType
    diagnosed_at: datetime

    class Config:
        from_attributes = True


class VitalSignResponse(BaseModel):
    id: str
    patient_id: str
    timestamp: datetime
    heart_rate: int
    blood_pressure_systolic: int
    blood_pressure_diastolic: int
    temperature: float
    respiratory_rate: int
    oxygen_saturation: float
    pain_level: Optional[int] = None

    class Config:
        from_attributes = True


class LabResultStatus(str, Enum):
    NORMAL = "normal"
    LOW = "low"
    HIGH = "high"
    CRITICAL = "critical"


class LabResultResponse(BaseModel):
    id: str
    patient_id: str
    test_name: str
    value: float
    unit: str
    normal_min: float
    normal_max: float
    status: LabResultStatus
    timestamp: datetime
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class EmergencyContact(BaseModel):
    name: Optional[str] = None
    relationship: Optional[str] = None
    phone: Optional[str] = None


class PatientBase(BaseModel):
    mrn: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    gender: Gender
    department: str
    room: str
    bed: str
    attending_physician: str
    primary_diagnosis: str


class PatientCreate(PatientBase):
    pass


class PatientResponse(PatientBase):
    id: str
    age: int
    admission_date: datetime
    discharge_date: Optional[datetime] = None
    risk_score: int
    risk_level: RiskLevel
    clinical_status: ClinicalStatus
    status: PatientStatus
    insurance_provider: Optional[str] = None
    emergency_contact: Optional[EmergencyContact] = None
    diagnoses: List[DiagnosisResponse] = []

    class Config:
        from_attributes = True
