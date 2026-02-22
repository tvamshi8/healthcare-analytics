from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from ..database import Base


class AuditLog(Base):
    """
    HIPAA-compliant audit logging for all PHI access.
    """
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False, index=True)
    user_name = Column(String(100), nullable=False)
    action = Column(String(50), nullable=False, index=True)  # VIEW, CREATE, UPDATE, DELETE
    resource = Column(String(50), nullable=False, index=True)  # patient, vitals, lab_result, etc.
    resource_id = Column(String(36), nullable=True)
    details = Column(Text, nullable=True)  # JSON string with additional context
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible

    timestamp = Column(DateTime, server_default=func.now(), index=True)
