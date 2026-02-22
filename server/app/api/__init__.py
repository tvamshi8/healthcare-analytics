from fastapi import APIRouter
from .auth import router as auth_router
from .patients import router as patients_router
from .analytics import router as analytics_router
from .alerts import router as alerts_router
from .predictions import router as predictions_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(patients_router, prefix="/patients", tags=["Patients"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(alerts_router, prefix="/alerts", tags=["Alerts"])
api_router.include_router(predictions_router, prefix="/predict", tags=["Predictions"])
