import axios from 'axios'
import type {
  Patient,
  VitalSigns,
  LabResult,
  RiskAssessment,
  DashboardMetrics,
  RiskDistribution,
  DepartmentStats,
  ReadmissionTrend,
  Alert,
  User,
  AuditLog,
} from '@/types'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const storage = localStorage.getItem('auth-storage')
    if (storage) {
      const { state } = JSON.parse(storage)
      if (state?.token) {
        config.headers.Authorization = `Bearer ${state.token}`
      }
    }
  }
  return config
})

// Auth
export const authAPI = {
  login: async (email: string, password: string) => {
    const { data } = await api.post<{ user: User; token: string }>('/auth/login', { email, password })
    return data
  },
  logout: async () => {
    await api.post('/auth/logout')
  },
  me: async () => {
    const { data } = await api.get<{ user: User }>('/auth/me')
    return data
  },
}

// Patients
export const patientsAPI = {
  getAll: async (params?: {
    department?: string
    riskLevel?: string
    status?: string
    page?: number
    limit?: number
  }) => {
    const { data } = await api.get<{
      data: Patient[]
      total: number
      page: number
      totalPages: number
    }>('/patients', { params })
    return data
  },
  getById: async (id: string) => {
    const { data } = await api.get<{ data: Patient }>(`/patients/${id}`)
    return data.data
  },
  getVitals: async (id: string, params?: { start?: string; end?: string }) => {
    const { data } = await api.get<{ data: VitalSigns[] }>(`/patients/${id}/vitals`, { params })
    return data.data
  },
  getLabResults: async (id: string) => {
    const { data } = await api.get<{ data: LabResult[] }>(`/patients/${id}/labs`)
    return data.data
  },
  getRiskAssessment: async (id: string) => {
    const { data } = await api.get<{ data: RiskAssessment }>(`/patients/${id}/risk`)
    return data.data
  },
}

// Analytics
export const analyticsAPI = {
  getDashboard: async () => {
    const { data } = await api.get<{ data: DashboardMetrics }>('/analytics/dashboard')
    return data.data
  },
  getRiskDistribution: async () => {
    const { data } = await api.get<{ data: RiskDistribution }>('/analytics/risk-distribution')
    return data.data
  },
  getDepartmentStats: async () => {
    const { data } = await api.get<{ data: DepartmentStats[] }>('/analytics/departments')
    return data.data
  },
  getReadmissionTrends: async (days = 30) => {
    const { data } = await api.get<{ data: ReadmissionTrend[] }>('/analytics/readmission-trends', {
      params: { days },
    })
    return data.data
  },
  getPopulationHealth: async () => {
    const { data } = await api.get<{ data: Record<string, unknown> }>('/analytics/population')
    return data.data
  },
}

// Predictions
export const predictionsAPI = {
  predictReadmission: async (patientId: string) => {
    const { data } = await api.post<{ data: RiskAssessment }>('/predict/readmission', { patientId })
    return data.data
  },
  getExplanation: async (patientId: string) => {
    const { data } = await api.get<{ data: { features: Record<string, number>; summary: string } }>(
      `/predict/explain/${patientId}`
    )
    return data.data
  },
}

// Alerts
export const alertsAPI = {
  getAll: async (params?: { acknowledged?: boolean; severity?: string }) => {
    const { data } = await api.get<{ data: Alert[] }>('/alerts', { params })
    return data.data
  },
  acknowledge: async (id: string) => {
    const { data } = await api.patch<{ data: Alert }>(`/alerts/${id}/acknowledge`)
    return data.data
  },
}

// Audit Logs (Admin only)
export const auditAPI = {
  getLogs: async (params?: { userId?: string; action?: string; start?: string; end?: string }) => {
    const { data } = await api.get<{ data: AuditLog[]; total: number }>('/audit/logs', { params })
    return data
  },
}

export default api
