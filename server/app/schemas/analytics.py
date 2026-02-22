from pydantic import BaseModel


class DashboardMetrics(BaseModel):
    total_patients: int
    patients_change: float
    high_risk_patients: int
    high_risk_change: float
    readmission_rate: float
    readmission_rate_change: float
    avg_length_of_stay: float
    los_change: float
    interventions_today: int
    discharges_pending: int


class RiskDistribution(BaseModel):
    low: int
    medium: int
    high: int
    critical: int


class DepartmentStats(BaseModel):
    department: str
    total_patients: int
    high_risk: int
    avg_risk_score: float
    readmission_rate: float


class ReadmissionTrend(BaseModel):
    date: str
    predicted: int
    actual: int
    interventions: int
