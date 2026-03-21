import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'
import { format, formatDistanceToNow, parseISO } from 'date-fns'
import type { RiskLevel, ClinicalStatus } from '@/types'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: string | Date) {
  const d = typeof date === 'string' ? parseISO(date) : date
  return format(d, 'MMM d, yyyy')
}

export function formatDateTime(date: string | Date) {
  const d = typeof date === 'string' ? parseISO(date) : date
  return format(d, 'MMM d, yyyy h:mm a')
}

export function formatTimeAgo(date: string | Date) {
  const d = typeof date === 'string' ? parseISO(date) : date
  return formatDistanceToNow(d, { addSuffix: true })
}

export function formatNumber(num: number) {
  return new Intl.NumberFormat('en-US').format(num)
}

export function formatPercentage(num: number, decimals = 1) {
  return `${num.toFixed(decimals)}%`
}

export function getRiskColor(level: RiskLevel) {
  switch (level) {
    case 'low':
      return 'text-risk-low'
    case 'medium':
      return 'text-risk-medium'
    case 'high':
      return 'text-risk-high'
    case 'critical':
      return 'text-risk-critical'
    default:
      return 'text-gray-500'
  }
}

export function getRiskBgColor(level: RiskLevel) {
  switch (level) {
    case 'low':
      return 'bg-risk-low/10 text-risk-low'
    case 'medium':
      return 'bg-risk-medium/10 text-risk-medium'
    case 'high':
      return 'bg-risk-high/10 text-risk-high'
    case 'critical':
      return 'bg-risk-critical/10 text-risk-critical'
    default:
      return 'bg-gray-100 text-gray-500'
  }
}

export function getStatusColor(status: ClinicalStatus) {
  switch (status) {
    case 'stable':
      return 'text-status-stable'
    case 'watch':
      return 'text-status-watch'
    case 'critical':
      return 'text-status-critical'
    default:
      return 'text-gray-500'
  }
}

export function getStatusBgColor(status: ClinicalStatus) {
  switch (status) {
    case 'stable':
      return 'bg-status-stable/10 text-status-stable'
    case 'watch':
      return 'bg-status-watch/10 text-status-watch'
    case 'critical':
      return 'bg-status-critical/10 text-status-critical'
    default:
      return 'bg-gray-100 text-gray-500'
  }
}

export function getRiskLabel(level: RiskLevel) {
  return level.charAt(0).toUpperCase() + level.slice(1)
}

export function calculateAge(dateOfBirth: string) {
  const today = new Date()
  const birthDate = new Date(dateOfBirth)
  let age = today.getFullYear() - birthDate.getFullYear()
  const monthDiff = today.getMonth() - birthDate.getMonth()
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--
  }
  return age
}

export function getVitalStatus(value: number, min: number, max: number): 'normal' | 'low' | 'high' | 'critical' {
  if (value < min * 0.8 || value > max * 1.2) return 'critical'
  if (value < min || value > max) return value < min ? 'low' : 'high'
  return 'normal'
}

export function getVitalStatusColor(status: 'normal' | 'low' | 'high' | 'critical') {
  switch (status) {
    case 'normal':
      return 'text-green-600'
    case 'low':
      return 'text-blue-600'
    case 'high':
      return 'text-amber-600'
    case 'critical':
      return 'text-red-600'
    default:
      return 'text-gray-600'
  }
}

// HIPAA-safe patient name display (last name + first initial)
export function formatPatientName(firstName: string, lastName: string, full = false) {
  if (full) {
    return `${lastName}, ${firstName}`
  }
  return `${lastName}, ${firstName.charAt(0)}.`
}

// Format MRN with consistent display
export function formatMRN(mrn: string) {
  return `MRN: ${mrn}`
}
