from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List

from ..database import get_db
from ..models.patient import Patient, RiskLevel, PatientStatus
from ..models.user import User
from ..models.alert import Alert
from ..schemas.analytics import DashboardMetrics, RiskDistribution, DepartmentStats, ReadmissionTrend
from .auth import get_current_user

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    now = datetime.utcnow()
    thirty_days_ago = now - timedelta(days=30)
    sixty_days_ago = now - timedelta(days=60)

    # Current period
    current_patients = db.query(Patient).filter(
        Patient.status == PatientStatus.ADMITTED
    ).count()

    high_risk_current = db.query(Patient).filter(
        Patient.status == PatientStatus.ADMITTED,
        Patient.risk_level.in_([RiskLevel.HIGH, RiskLevel.CRITICAL])
    ).count()

    # Previous period for comparison
    # In production, these would be calculated from historical snapshots
    previous_patients = int(current_patients * 0.95)
    previous_high_risk = int(high_risk_current * 1.12)

    # Calculate changes
    patients_change = ((current_patients - previous_patients) / max(previous_patients, 1)) * 100
    high_risk_change = ((high_risk_current - previous_high_risk) / max(previous_high_risk, 1)) * 100

    # Readmission rate (simulated - in production, track actual readmissions)
    readmission_rate = 22.5
    readmission_target = 30.0
    readmission_change = ((readmission_target - readmission_rate) / readmission_target) * -100

    # Average length of stay (simulated)
    avg_los = 4.6
    los_change = -11.5

    # Today's interventions
    today_start = datetime(now.year, now.month, now.day)
    interventions_today = 18  # In production, count from recommendations table

    # Pending discharges
    discharges_pending = db.query(Patient).filter(
        Patient.status == PatientStatus.ADMITTED,
        Patient.clinical_status == 'stable'
    ).limit(20).count()

    return {
        "data": {
            "totalPatients": current_patients,
            "patientsChange": round(patients_change, 1),
            "highRiskPatients": high_risk_current,
            "highRiskChange": round(high_risk_change, 1),
            "readmissionRate": readmission_rate,
            "readmissionRateChange": round(readmission_change, 1),
            "avgLengthOfStay": avg_los,
            "losChange": los_change,
            "interventionsToday": interventions_today,
            "dischargesPending": discharges_pending
        }
    }


@router.get("/risk-distribution")
async def get_risk_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    distribution = db.query(
        Patient.risk_level,
        func.count(Patient.id).label('count')
    ).filter(
        Patient.status == PatientStatus.ADMITTED
    ).group_by(Patient.risk_level).all()

    result = {"low": 0, "medium": 0, "high": 0, "critical": 0}

    for level, count in distribution:
        result[level.value] = count

    return {"data": result}


@router.get("/departments")
async def get_department_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    departments = db.query(
        Patient.department,
        func.count(Patient.id).label('total'),
        func.avg(Patient.risk_score).label('avg_risk')
    ).filter(
        Patient.status == PatientStatus.ADMITTED
    ).group_by(Patient.department).all()

    result = []
    for dept, total, avg_risk in departments:
        high_risk = db.query(Patient).filter(
            Patient.department == dept,
            Patient.status == PatientStatus.ADMITTED,
            Patient.risk_level.in_([RiskLevel.HIGH, RiskLevel.CRITICAL])
        ).count()

        result.append({
            "department": dept,
            "totalPatients": total,
            "highRisk": high_risk,
            "avgRiskScore": round(avg_risk or 0, 1),
            "readmissionRate": round(20 + (high_risk / max(total, 1)) * 30, 1)  # Simulated
        })

    return {"data": result}


@router.get("/readmission-trends")
async def get_readmission_trends(
    days: int = Query(30, ge=7, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # In production, this would come from actual readmission tracking
    # For demo, generate synthetic trend data
    import random

    result = []
    for i in range(days):
        date = datetime.utcnow() - timedelta(days=(days - 1 - i))
        result.append({
            "date": date.strftime("%Y-%m-%d"),
            "predicted": random.randint(18, 28),
            "actual": random.randint(16, 26),
            "interventions": random.randint(5, 15)
        })

    return {"data": result}


@router.get("/population")
async def get_population_health(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Population health statistics
    total = db.query(Patient).filter(Patient.status == PatientStatus.ADMITTED).count()

    # Age distribution
    age_groups = {
        "0-17": 0,
        "18-44": 0,
        "45-64": 0,
        "65-74": 0,
        "75+": 0
    }

    # Common diagnoses
    diagnoses_count = {}

    # In production, calculate actual distributions
    # For demo, return simulated data
    return {
        "data": {
            "totalPatients": total,
            "ageDistribution": {
                "0-17": 12,
                "18-44": 45,
                "45-64": 78,
                "65-74": 68,
                "75+": 44
            },
            "genderDistribution": {
                "male": 124,
                "female": 118,
                "other": 5
            },
            "topDiagnoses": [
                {"diagnosis": "Heart Failure", "count": 34},
                {"diagnosis": "COPD", "count": 28},
                {"diagnosis": "Diabetes", "count": 42},
                {"diagnosis": "Pneumonia", "count": 22},
                {"diagnosis": "Sepsis", "count": 18}
            ],
            "avgRiskScore": 38.5,
            "readmissionRate30Day": 22.5,
            "avgLengthOfStay": 4.6
        }
    }
