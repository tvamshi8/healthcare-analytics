from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from datetime import datetime

from ..database import get_db
from ..models.patient import Patient, VitalSign, LabResult
from ..models.user import User
from ..schemas.patient import PatientResponse, VitalSignResponse, LabResultResponse, EmergencyContact
from .auth import get_current_user

router = APIRouter()


def calculate_age(dob: datetime) -> int:
    today = datetime.now()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


@router.get("/", response_model=dict)
async def list_patients(
    department: Optional[str] = None,
    risk_level: Optional[str] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Patient)

    if department:
        query = query.filter(Patient.department == department)
    if risk_level:
        query = query.filter(Patient.risk_level == risk_level)
    if status:
        query = query.filter(Patient.status == status)

    total = query.count()
    patients = query.order_by(Patient.risk_score.desc()).offset((page - 1) * limit).limit(limit).all()

    result = []
    for p in patients:
        emergency_contact = None
        if p.emergency_contact_name:
            emergency_contact = EmergencyContact(
                name=p.emergency_contact_name,
                relationship=p.emergency_contact_relationship,
                phone=p.emergency_contact_phone
            )

        result.append({
            "id": p.id,
            "mrn": p.mrn,
            "first_name": p.first_name,
            "last_name": p.last_name,
            "date_of_birth": p.date_of_birth,
            "gender": p.gender.value,
            "age": calculate_age(p.date_of_birth),
            "admission_date": p.admission_date,
            "discharge_date": p.discharge_date,
            "department": p.department,
            "room": p.room,
            "bed": p.bed,
            "attending_physician": p.attending_physician,
            "primary_diagnosis": p.primary_diagnosis,
            "risk_score": p.risk_score,
            "risk_level": p.risk_level.value,
            "clinical_status": p.clinical_status.value,
            "status": p.status.value,
            "insurance_provider": p.insurance_provider,
            "emergency_contact": emergency_contact,
            "diagnoses": [
                {
                    "id": d.id,
                    "code": d.code,
                    "description": d.description,
                    "type": d.type.value,
                    "diagnosed_at": d.diagnosed_at
                }
                for d in p.diagnoses
            ]
        })

    return {
        "data": result,
        "total": total,
        "page": page,
        "totalPages": (total + limit - 1) // limit
    }


@router.get("/{patient_id}")
async def get_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    emergency_contact = None
    if patient.emergency_contact_name:
        emergency_contact = {
            "name": patient.emergency_contact_name,
            "relationship": patient.emergency_contact_relationship,
            "phone": patient.emergency_contact_phone
        }

    return {
        "data": {
            "id": patient.id,
            "mrn": patient.mrn,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "date_of_birth": patient.date_of_birth,
            "gender": patient.gender.value,
            "age": calculate_age(patient.date_of_birth),
            "admission_date": patient.admission_date,
            "discharge_date": patient.discharge_date,
            "department": patient.department,
            "room": patient.room,
            "bed": patient.bed,
            "attending_physician": patient.attending_physician,
            "primary_diagnosis": patient.primary_diagnosis,
            "risk_score": patient.risk_score,
            "risk_level": patient.risk_level.value,
            "clinical_status": patient.clinical_status.value,
            "status": patient.status.value,
            "insurance_provider": patient.insurance_provider,
            "emergency_contact": emergency_contact,
            "diagnoses": [
                {
                    "id": d.id,
                    "code": d.code,
                    "description": d.description,
                    "type": d.type.value,
                    "diagnosed_at": d.diagnosed_at
                }
                for d in patient.diagnoses
            ]
        }
    }


@router.get("/{patient_id}/vitals", response_model=dict)
async def get_patient_vitals(
    patient_id: str,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(VitalSign).filter(VitalSign.patient_id == patient_id)

    if start:
        query = query.filter(VitalSign.timestamp >= start)
    if end:
        query = query.filter(VitalSign.timestamp <= end)

    vitals = query.order_by(VitalSign.timestamp.desc()).limit(100).all()

    return {
        "data": [
            {
                "id": v.id,
                "patient_id": v.patient_id,
                "timestamp": v.timestamp,
                "heart_rate": v.heart_rate,
                "blood_pressure_systolic": v.blood_pressure_systolic,
                "blood_pressure_diastolic": v.blood_pressure_diastolic,
                "temperature": v.temperature,
                "respiratory_rate": v.respiratory_rate,
                "oxygen_saturation": v.oxygen_saturation,
                "pain_level": v.pain_level
            }
            for v in vitals
        ]
    }


@router.get("/{patient_id}/labs", response_model=dict)
async def get_patient_labs(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    labs = db.query(LabResult).filter(
        LabResult.patient_id == patient_id
    ).order_by(LabResult.timestamp.desc()).limit(50).all()

    return {
        "data": [
            {
                "id": l.id,
                "patient_id": l.patient_id,
                "test_name": l.test_name,
                "value": l.value,
                "unit": l.unit,
                "normal_min": l.normal_min,
                "normal_max": l.normal_max,
                "status": l.status.value,
                "timestamp": l.timestamp,
                "notes": l.notes
            }
            for l in labs
        ]
    }


@router.get("/{patient_id}/risk")
async def get_patient_risk(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Get latest risk assessment
    assessment = patient.risk_assessments[-1] if patient.risk_assessments else None

    if not assessment:
        # Return basic risk info if no assessment exists
        return {
            "data": {
                "patient_id": patient_id,
                "risk_score": patient.risk_score,
                "risk_level": patient.risk_level.value,
                "readmission_probability": patient.risk_score / 100,
                "confidence": 0.75,
                "risk_factors": [],
                "recommendations": [],
                "assessed_at": datetime.utcnow()
            }
        }

    return {
        "data": {
            "id": assessment.id,
            "patient_id": assessment.patient_id,
            "risk_score": assessment.risk_score,
            "risk_level": assessment.risk_level,
            "readmission_probability": assessment.readmission_probability,
            "confidence": assessment.confidence,
            "assessed_at": assessment.assessed_at,
            "risk_factors": [
                {
                    "id": rf.id,
                    "factor": rf.factor,
                    "description": rf.description,
                    "contribution": rf.contribution,
                    "severity": rf.severity
                }
                for rf in assessment.risk_factors
            ],
            "recommendations": [
                {
                    "id": r.id,
                    "type": r.type.value,
                    "title": r.title,
                    "description": r.description,
                    "priority": r.priority.value,
                    "status": r.status.value,
                    "created_at": r.created_at,
                    "completed_at": r.completed_at
                }
                for r in assessment.recommendations
            ]
        }
    }
