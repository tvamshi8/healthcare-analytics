export type RiskLevel = 'low' | 'medium' | 'high' | 'critical'

export type PatientStatus = 'admitted' | 'discharged' | 'transferred' | 'deceased'

export type ClinicalStatus = 'stable' | 'watch' | 'critical'

export interface Patient {
  id: string
  mrn: string
  firstName: string
  lastName: string
  dateOfBirth: string
  gender: 'male' | 'female' | 'other'
  age: number
  admissionDate: string
  dischargeDate?: string
  department: string
  room: string
  bed: string
  attendingPhysician: string
  primaryDiagnosis: string
  diagnoses: Diagnosis[]
  riskScore: number
  riskLevel: RiskLevel
  clinicalStatus: ClinicalStatus
  status: PatientStatus
  insuranceProvider?: string
  emergencyContact?: EmergencyContact
}

export interface Diagnosis {
  code: string
  description: string
  type: 'primary' | 'secondary' | 'comorbidity'
  diagnosedAt: string
}

export interface EmergencyContact {
  name: string
  relationship: string
  phone: string
}

export interface VitalSigns {
  id: string
  patientId: string
  timestamp: string
  heartRate: number
  bloodPressureSystolic: number
  bloodPressureDiastolic: number
  temperature: number
  respiratoryRate: number
  oxygenSaturation: number
  painLevel?: number
}

export interface LabResult {
  id: string
  patientId: string
  testName: string
  value: number
  unit: string
  normalMin: number
  normalMax: number
  status: 'normal' | 'low' | 'high' | 'critical'
  timestamp: string
}

export interface RiskAssessment {
  patientId: string
  riskScore: number
  riskLevel: RiskLevel
  readmissionProbability: number
  confidence: number
  riskFactors: RiskFactor[]
  recommendations: Recommendation[]
  assessedAt: string
}

export interface RiskFactor {
  factor: string
  description: string
  contribution: number
  severity: 'low' | 'medium' | 'high'
}

export interface Recommendation {
  id: string
  type: 'intervention' | 'follow-up' | 'referral' | 'education'
  title: string
  description: string
  priority: 'low' | 'medium' | 'high' | 'urgent'
  status: 'pending' | 'in-progress' | 'completed' | 'declined'
}

export interface DashboardMetrics {
  totalPatients: number
  patientsChange: number
  highRiskPatients: number
  highRiskChange: number
  readmissionRate: number
  readmissionRateChange: number
  avgLengthOfStay: number
  losChange: number
  interventionsToday: number
  dischargesPending: number
}

export interface RiskDistribution {
  low: number
  medium: number
  high: number
  critical: number
}

export interface DepartmentStats {
  department: string
  totalPatients: number
  highRisk: number
  avgRiskScore: number
  readmissionRate: number
}

export interface ReadmissionTrend {
  date: string
  predicted: number
  actual: number
  interventions: number
}

export interface Alert {
  id: string
  type: 'vitals' | 'risk' | 'deterioration' | 'discharge'
  severity: 'info' | 'warning' | 'critical'
  patientId: string
  patientName: string
  title: string
  message: string
  createdAt: string
  acknowledged: boolean
}

export interface User {
  id: string
  email: string
  name: string
  role: 'physician' | 'nurse' | 'admin' | 'analyst'
  department?: string
  avatar?: string
}

export interface AuditLog {
  id: string
  userId: string
  userName: string
  action: string
  resource: string
  resourceId: string
  details: string
  ipAddress: string
  timestamp: string
}
