from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from ..database import get_db
from ..models.patient import Patient
from ..models.risk import RiskAssessment, RiskFactor, Recommendation, RecommendationType, RecommendationPriority
from ..models.user import User
from .auth import get_current_user
from ..ml.readmission_model import predict_readmission

router = APIRouter()


@router.post("/readmission")
async def predict_patient_readmission(
    request: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    patient_id = request.get("patientId")

    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Get prediction from ML model
    prediction = predict_readmission(patient, db)

    # Create risk assessment record
    assessment = RiskAssessment(
        id=str(uuid.uuid4()),
        patient_id=patient_id,
        risk_score=prediction["risk_score"],
        risk_level=prediction["risk_level"],
        readmission_probability=prediction["probability"],
        confidence=prediction["confidence"],
        assessed_at=datetime.utcnow()
    )
    db.add(assessment)

    # Add risk factors
    for rf in prediction["risk_factors"]:
        risk_factor = RiskFactor(
            id=str(uuid.uuid4()),
            assessment_id=assessment.id,
            factor=rf["factor"],
            description=rf["description"],
            contribution=rf["contribution"],
            severity=rf["severity"]
        )
        db.add(risk_factor)

    # Add recommendations
    for rec in prediction["recommendations"]:
        recommendation = Recommendation(
            id=str(uuid.uuid4()),
            assessment_id=assessment.id,
            type=RecommendationType(rec["type"]),
            title=rec["title"],
            description=rec["description"],
            priority=RecommendationPriority(rec["priority"])
        )
        db.add(recommendation)

    # Update patient risk score
    patient.risk_score = prediction["risk_score"]
    patient.risk_level = prediction["risk_level"]

    db.commit()

    return {
        "data": {
            "id": assessment.id,
            "patientId": patient_id,
            "riskScore": prediction["risk_score"],
            "riskLevel": prediction["risk_level"],
            "readmissionProbability": prediction["probability"],
            "confidence": prediction["confidence"],
            "riskFactors": prediction["risk_factors"],
            "recommendations": prediction["recommendations"],
            "assessedAt": assessment.assessed_at
        }
    }


@router.get("/explain/{patient_id}")
async def explain_prediction(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Get latest assessment
    assessment = db.query(RiskAssessment).filter(
        RiskAssessment.patient_id == patient_id
    ).order_by(RiskAssessment.assessed_at.desc()).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="No risk assessment found")

    # In production, use SHAP values for model explainability
    feature_importance = {}
    for rf in assessment.risk_factors:
        feature_importance[rf.factor] = rf.contribution

    summary = generate_explanation_summary(patient, assessment)

    return {
        "data": {
            "features": feature_importance,
            "summary": summary
        }
    }


def generate_explanation_summary(patient: Patient, assessment: RiskAssessment) -> str:
    """Generate a human-readable explanation of the risk prediction."""
    factors = sorted(assessment.risk_factors, key=lambda x: x.contribution, reverse=True)

    if not factors:
        return f"Patient has a {assessment.risk_level} risk level with a {assessment.risk_score}% risk score."

    top_factors = [f.factor for f in factors[:3]]

    summary = f"Patient {patient.last_name}, {patient.first_name} has a {assessment.risk_level} risk level "
    summary += f"with a {assessment.risk_score}% probability of 30-day readmission. "
    summary += f"The primary contributing factors are: {', '.join(top_factors)}. "

    if assessment.risk_level in ["high", "critical"]:
        summary += "Proactive intervention is recommended to reduce readmission risk."

    return summary
