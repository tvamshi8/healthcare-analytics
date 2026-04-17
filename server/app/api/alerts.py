from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from ..database import get_db
from ..models.alert import Alert, AlertSeverity
from ..models.user import User
from .auth import get_current_user

router = APIRouter()


@router.get("/")
async def list_alerts(
    acknowledged: Optional[bool] = None,
    severity: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Alert)

    if acknowledged is not None:
        query = query.filter(Alert.acknowledged == acknowledged)
    if severity:
        query = query.filter(Alert.severity == severity)

    total = query.count()
    alerts = query.order_by(Alert.created_at.desc()).offset((page - 1) * limit).limit(limit).all()

    return {
        "data": [
            {
                "id": a.id,
                "type": a.type.value,
                "severity": a.severity.value,
                "patientId": a.patient_id,
                "patientName": a.patient_name,
                "title": a.title,
                "message": a.message,
                "acknowledged": a.acknowledged,
                "acknowledgedAt": a.acknowledged_at,
                "createdAt": a.created_at
            }
            for a in alerts
        ],
        "total": total,
        "page": page,
        "totalPages": (total + limit - 1) // limit
    }


@router.patch("/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.acknowledged = True
    alert.acknowledged_at = datetime.utcnow()
    alert.acknowledged_by = current_user.id
    db.commit()

    return {
        "data": {
            "id": alert.id,
            "type": alert.type.value,
            "severity": alert.severity.value,
            "patientId": alert.patient_id,
            "patientName": alert.patient_name,
            "title": alert.title,
            "message": alert.message,
            "acknowledged": alert.acknowledged,
            "acknowledgedAt": alert.acknowledged_at,
            "createdAt": alert.created_at
        }
    }


@router.get("/stats")
async def get_alert_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    unacknowledged = db.query(Alert).filter(Alert.acknowledged == False).count()

    critical = db.query(Alert).filter(
        Alert.acknowledged == False,
        Alert.severity == AlertSeverity.CRITICAL
    ).count()

    warning = db.query(Alert).filter(
        Alert.acknowledged == False,
        Alert.severity == AlertSeverity.WARNING
    ).count()

    return {
        "data": {
            "unacknowledged": unacknowledged,
            "critical": critical,
            "warning": warning
        }
    }
