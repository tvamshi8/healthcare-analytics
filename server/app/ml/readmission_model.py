"""
Readmission Prediction Model

Uses a Random Forest classifier trained on patient features to predict
30-day hospital readmission risk.

In production, this would load a pre-trained model. For demonstration,
we use a rule-based scoring system that mimics ML behavior.
"""

from typing import Dict, List, Any
from datetime import datetime
import numpy as np
from sqlalchemy.orm import Session

from ..models.patient import Patient, VitalSign, LabResult


def calculate_age(dob: datetime) -> int:
    today = datetime.now()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def extract_features(patient: Patient, db: Session) -> Dict[str, float]:
    """Extract features from patient data for prediction."""
    features = {}

    # Demographics
    features["age"] = calculate_age(patient.date_of_birth)
    features["is_elderly"] = 1.0 if features["age"] >= 65 else 0.0

    # Length of stay
    if patient.admission_date:
        los = (datetime.utcnow() - patient.admission_date).days
        features["length_of_stay"] = los
        features["extended_stay"] = 1.0 if los > 7 else 0.0

    # Diagnosis count (comorbidities)
    features["diagnosis_count"] = len(patient.diagnoses)
    features["high_comorbidity"] = 1.0 if len(patient.diagnoses) >= 3 else 0.0

    # Get latest vitals
    latest_vitals = db.query(VitalSign).filter(
        VitalSign.patient_id == patient.id
    ).order_by(VitalSign.timestamp.desc()).first()

    if latest_vitals:
        features["heart_rate"] = latest_vitals.heart_rate
        features["bp_systolic"] = latest_vitals.blood_pressure_systolic
        features["bp_diastolic"] = latest_vitals.blood_pressure_diastolic
        features["temperature"] = latest_vitals.temperature
        features["oxygen_saturation"] = latest_vitals.oxygen_saturation

        # Abnormal vitals flags
        features["abnormal_hr"] = 1.0 if latest_vitals.heart_rate < 60 or latest_vitals.heart_rate > 100 else 0.0
        features["abnormal_bp"] = 1.0 if latest_vitals.blood_pressure_systolic < 90 or latest_vitals.blood_pressure_systolic > 140 else 0.0
        features["low_oxygen"] = 1.0 if latest_vitals.oxygen_saturation < 95 else 0.0

    # Get recent lab results
    lab_results = db.query(LabResult).filter(
        LabResult.patient_id == patient.id
    ).order_by(LabResult.timestamp.desc()).limit(10).all()

    abnormal_labs = sum(1 for l in lab_results if l.status.value in ["high", "low", "critical"])
    features["abnormal_lab_count"] = abnormal_labs
    features["critical_labs"] = 1.0 if any(l.status.value == "critical" for l in lab_results) else 0.0

    return features


def calculate_risk_score(features: Dict[str, float]) -> int:
    """
    Calculate risk score based on extracted features.

    This mimics an ML model's behavior using weighted rules.
    In production, replace with actual model.predict_proba().
    """
    score = 10  # Base score

    # Age factor
    if features.get("is_elderly", 0):
        score += 15

    # Length of stay factor
    if features.get("extended_stay", 0):
        score += 12

    # Comorbidity factor
    if features.get("high_comorbidity", 0):
        score += 18

    # Vital signs factors
    if features.get("abnormal_hr", 0):
        score += 10
    if features.get("abnormal_bp", 0):
        score += 12
    if features.get("low_oxygen", 0):
        score += 15

    # Lab results factors
    score += features.get("abnormal_lab_count", 0) * 5
    if features.get("critical_labs", 0):
        score += 20

    # Add some variance to simulate model behavior
    score += np.random.randint(-5, 5)

    return max(0, min(100, score))


def get_risk_factors(features: Dict[str, float], score: int) -> List[Dict[str, Any]]:
    """Identify contributing risk factors."""
    risk_factors = []

    if features.get("is_elderly", 0):
        risk_factors.append({
            "factor": "Advanced Age",
            "description": f"Patient is {features.get('age', 0)} years old (≥65 increases risk)",
            "contribution": 15.0,
            "severity": "medium"
        })

    if features.get("extended_stay", 0):
        risk_factors.append({
            "factor": "Extended Hospital Stay",
            "description": f"Length of stay: {features.get('length_of_stay', 0)} days (>7 days increases risk)",
            "contribution": 12.0,
            "severity": "medium"
        })

    if features.get("high_comorbidity", 0):
        risk_factors.append({
            "factor": "Multiple Comorbidities",
            "description": f"{features.get('diagnosis_count', 0)} concurrent diagnoses",
            "contribution": 18.0,
            "severity": "high"
        })

    if features.get("abnormal_hr", 0):
        risk_factors.append({
            "factor": "Abnormal Heart Rate",
            "description": f"Heart rate: {features.get('heart_rate', 0)} bpm (outside 60-100 range)",
            "contribution": 10.0,
            "severity": "medium"
        })

    if features.get("low_oxygen", 0):
        risk_factors.append({
            "factor": "Low Oxygen Saturation",
            "description": f"SpO2: {features.get('oxygen_saturation', 0)}% (below 95%)",
            "contribution": 15.0,
            "severity": "high"
        })

    if features.get("critical_labs", 0):
        risk_factors.append({
            "factor": "Critical Lab Values",
            "description": "One or more lab results in critical range",
            "contribution": 20.0,
            "severity": "high"
        })

    # Sort by contribution
    risk_factors.sort(key=lambda x: x["contribution"], reverse=True)

    return risk_factors


def get_recommendations(risk_level: str, risk_factors: List[Dict]) -> List[Dict[str, Any]]:
    """Generate clinical recommendations based on risk assessment."""
    recommendations = []

    if risk_level in ["high", "critical"]:
        recommendations.append({
            "type": "intervention",
            "title": "Schedule Follow-up Appointment",
            "description": "Arrange a follow-up appointment within 7 days of discharge to monitor recovery",
            "priority": "high"
        })

        recommendations.append({
            "type": "referral",
            "title": "Home Health Referral",
            "description": "Consider home health services for medication management and vital signs monitoring",
            "priority": "high"
        })

    if any(rf["factor"] == "Multiple Comorbidities" for rf in risk_factors):
        recommendations.append({
            "type": "intervention",
            "title": "Care Coordination",
            "description": "Coordinate with specialists for comprehensive care plan",
            "priority": "medium"
        })

    if any(rf["factor"] == "Low Oxygen Saturation" for rf in risk_factors):
        recommendations.append({
            "type": "intervention",
            "title": "Respiratory Assessment",
            "description": "Conduct pulmonary function assessment before discharge",
            "priority": "high"
        })

    recommendations.append({
        "type": "education",
        "title": "Discharge Education",
        "description": "Provide comprehensive discharge instructions including warning signs for return",
        "priority": "medium" if risk_level in ["low", "medium"] else "high"
    })

    return recommendations


def predict_readmission(patient: Patient, db: Session) -> Dict[str, Any]:
    """
    Main prediction function.

    Returns risk assessment with score, level, factors, and recommendations.
    """
    # Extract features
    features = extract_features(patient, db)

    # Calculate risk score
    risk_score = calculate_risk_score(features)

    # Determine risk level
    if risk_score >= 80:
        risk_level = "critical"
    elif risk_score >= 60:
        risk_level = "high"
    elif risk_score >= 35:
        risk_level = "medium"
    else:
        risk_level = "low"

    # Get contributing factors
    risk_factors = get_risk_factors(features, risk_score)

    # Generate recommendations
    recommendations = get_recommendations(risk_level, risk_factors)

    # Calculate confidence (simulated - in production, use model's probability calibration)
    confidence = 0.80 + (len(risk_factors) * 0.02)
    confidence = min(0.95, confidence)

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "probability": risk_score / 100.0,
        "confidence": round(confidence, 2),
        "risk_factors": risk_factors,
        "recommendations": recommendations
    }
