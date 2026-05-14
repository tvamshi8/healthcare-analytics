'use client'

import { useState } from 'react'
import {
  Users,
  AlertTriangle,
  RotateCcw,
  Clock,
  CalendarCheck,
  Stethoscope,
} from 'lucide-react'
import { Sidebar, Header } from '@/components/layout'
import {
  MetricCard,
  RiskDistributionChart,
  ReadmissionTrends,
  PriorityPatients,
  LiveAlerts,
  DepartmentOverview,
} from '@/components/dashboard'
import { formatNumber, formatPercentage } from '@/lib/utils'
import type {
  DashboardMetrics,
  RiskDistribution,
  ReadmissionTrend,
  Patient,
  Alert,
  DepartmentStats,
} from '@/types'

// Mock data
const mockMetrics: DashboardMetrics = {
  totalPatients: 247,
  patientsChange: 5,
  highRiskPatients: 23,
  highRiskChange: -12,
  readmissionRate: 22.5,
  readmissionRateChange: -25,
  avgLengthOfStay: 4.6,
  losChange: -11.5,
  interventionsToday: 18,
  dischargesPending: 12,
}

const mockRiskDistribution: RiskDistribution = {
  low: 156,
  medium: 45,
  high: 38,
  critical: 8,
}

const mockTrends: ReadmissionTrend[] = Array.from({ length: 30 }, (_, i) => {
  const date = new Date()
  date.setDate(date.getDate() - (29 - i))
  return {
    date: date.toISOString().split('T')[0],
    predicted: Math.floor(Math.random() * 10) + 20,
    actual: Math.floor(Math.random() * 10) + 18,
    interventions: Math.floor(Math.random() * 8) + 5,
  }
})

const mockPatients: Patient[] = [
  {
    id: '1',
    mrn: 'MRN-001234',
    firstName: 'John',
    lastName: 'Doe',
    dateOfBirth: '1952-03-15',
    gender: 'male',
    age: 72,
    admissionDate: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    department: 'Cardiology',
    room: '302',
    bed: 'A',
    attendingPhysician: 'Dr. Sarah Johnson',
    primaryDiagnosis: 'Congestive Heart Failure (CHF)',
    diagnoses: [
      { code: 'I50.9', description: 'Heart failure, unspecified', type: 'primary', diagnosedAt: new Date().toISOString() },
    ],
    riskScore: 92,
    riskLevel: 'critical',
    clinicalStatus: 'watch',
    status: 'admitted',
  },
  {
    id: '2',
    mrn: 'MRN-005678',
    firstName: 'Mary',
    lastName: 'Smith',
    dateOfBirth: '1945-08-22',
    gender: 'female',
    age: 79,
    admissionDate: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
    department: 'Pulmonology',
    room: '415',
    bed: 'B',
    attendingPhysician: 'Dr. Michael Chen',
    primaryDiagnosis: 'COPD Exacerbation',
    diagnoses: [
      { code: 'J44.1', description: 'COPD with acute exacerbation', type: 'primary', diagnosedAt: new Date().toISOString() },
    ],
    riskScore: 78,
    riskLevel: 'high',
    clinicalStatus: 'watch',
    status: 'admitted',
  },
  {
    id: '3',
    mrn: 'MRN-009012',
    firstName: 'Robert',
    lastName: 'Johnson',
    dateOfBirth: '1958-11-30',
    gender: 'male',
    age: 66,
    admissionDate: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    department: 'Medicine',
    room: '210',
    bed: 'A',
    attendingPhysician: 'Dr. Emily Brown',
    primaryDiagnosis: 'Diabetic Ketoacidosis',
    diagnoses: [
      { code: 'E11.10', description: 'Type 2 diabetes with ketoacidosis', type: 'primary', diagnosedAt: new Date().toISOString() },
    ],
    riskScore: 71,
    riskLevel: 'high',
    clinicalStatus: 'stable',
    status: 'admitted',
  },
]

const mockAlerts: Alert[] = [
  {
    id: '1',
    type: 'vitals',
    severity: 'critical',
    patientId: '1',
    patientName: 'John Doe',
    title: 'Vital Signs Deteriorating',
    message: 'Blood pressure dropped to 90/60, heart rate elevated to 110 bpm',
    createdAt: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
    acknowledged: false,
  },
  {
    id: '2',
    type: 'risk',
    severity: 'warning',
    patientId: '2',
    patientName: 'Mary Smith',
    title: 'Risk Score Increased',
    message: 'Readmission risk increased from 65% to 78% based on new lab results',
    createdAt: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
    acknowledged: false,
  },
  {
    id: '3',
    type: 'discharge',
    severity: 'info',
    patientId: '4',
    patientName: 'Alice Williams',
    title: 'Discharge Planning Required',
    message: 'Patient scheduled for discharge tomorrow, care plan needs review',
    createdAt: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
    acknowledged: false,
  },
  {
    id: '4',
    type: 'deterioration',
    severity: 'warning',
    patientId: '3',
    patientName: 'Robert Johnson',
    title: 'Early Warning Score Elevated',
    message: 'NEWS2 score increased to 6, recommend clinical review',
    createdAt: new Date(Date.now() - 45 * 60 * 1000).toISOString(),
    acknowledged: true,
  },
]

const mockDepartments: DepartmentStats[] = [
  { department: 'Cardiology', totalPatients: 45, highRisk: 12, avgRiskScore: 48, readmissionRate: 28 },
  { department: 'Pulmonology', totalPatients: 38, highRisk: 8, avgRiskScore: 42, readmissionRate: 24 },
  { department: 'Medicine', totalPatients: 62, highRisk: 15, avgRiskScore: 38, readmissionRate: 22 },
  { department: 'Surgery', totalPatients: 54, highRisk: 6, avgRiskScore: 32, readmissionRate: 18 },
  { department: 'ICU', totalPatients: 18, highRisk: 14, avgRiskScore: 68, readmissionRate: 35 },
  { department: 'Oncology', totalPatients: 30, highRisk: 8, avgRiskScore: 45, readmissionRate: 26 },
]

export default function DashboardPage() {
  const [alerts, setAlerts] = useState<Alert[]>(mockAlerts)

  const handleAcknowledge = (id: string) => {
    setAlerts((prev) =>
      prev.map((a) => (a.id === id ? { ...a, acknowledged: true } : a))
    )
  }

  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header
          title="Patient Risk Dashboard"
          subtitle={`Monitoring ${formatNumber(mockMetrics.totalPatients)} patients across 6 departments`}
        />
        <main className="flex-1 overflow-auto p-6 bg-gray-50">
          {/* Metrics Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <MetricCard
              title="Total Patients"
              value={formatNumber(mockMetrics.totalPatients)}
              change={mockMetrics.patientsChange}
              icon={Users}
              iconColor="text-medical-primary"
              trend="up"
            />
            <MetricCard
              title="High Risk Patients"
              value={formatNumber(mockMetrics.highRiskPatients)}
              change={mockMetrics.highRiskChange}
              icon={AlertTriangle}
              iconColor="text-risk-high"
              trend="down"
            />
            <MetricCard
              title="Readmission Rate"
              value={formatPercentage(mockMetrics.readmissionRate)}
              change={mockMetrics.readmissionRateChange}
              changeLabel="vs target 30%"
              icon={RotateCcw}
              iconColor="text-amber-600"
              trend="down"
            />
            <MetricCard
              title="Avg Length of Stay"
              value={`${mockMetrics.avgLengthOfStay} days`}
              change={mockMetrics.losChange}
              icon={Clock}
              iconColor="text-purple-600"
              trend="down"
            />
          </div>

          {/* Secondary Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <MetricCard
              title="Interventions Today"
              value={formatNumber(mockMetrics.interventionsToday)}
              changeLabel="proactive care actions"
              icon={Stethoscope}
              iconColor="text-green-600"
            />
            <MetricCard
              title="Pending Discharges"
              value={formatNumber(mockMetrics.dischargesPending)}
              changeLabel="requiring review"
              icon={CalendarCheck}
              iconColor="text-blue-600"
            />
          </div>

          {/* Charts Row */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
            <div className="lg:col-span-2">
              <ReadmissionTrends data={mockTrends} />
            </div>
            <RiskDistributionChart data={mockRiskDistribution} />
          </div>

          {/* Priority Patients and Alerts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <PriorityPatients patients={mockPatients} />
            <LiveAlerts alerts={alerts} onAcknowledge={handleAcknowledge} />
          </div>

          {/* Department Overview */}
          <div className="mb-6">
            <DepartmentOverview data={mockDepartments} />
          </div>
        </main>
      </div>
    </div>
  )
}
