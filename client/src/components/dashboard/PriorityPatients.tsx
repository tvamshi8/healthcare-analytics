'use client'

import Link from 'next/link'
import { AlertTriangle, ChevronRight, Clock } from 'lucide-react'
import { Card, CardHeader, CardTitle, CardContent, Badge, Button } from '@/components/ui'
import { cn, formatTimeAgo, getRiskBgColor, getStatusBgColor } from '@/lib/utils'
import type { Patient } from '@/types'

interface PriorityPatientsProps {
  patients: Patient[]
}

export function PriorityPatients({ patients }: PriorityPatientsProps) {
  const highRiskPatients = patients
    .filter((p) => p.riskLevel === 'high' || p.riskLevel === 'critical')
    .sort((a, b) => b.riskScore - a.riskScore)
    .slice(0, 5)

  return (
    <Card className="h-full">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="flex items-center">
          <AlertTriangle className="mr-2 h-5 w-5 text-risk-high" />
          Priority Patients
        </CardTitle>
        <Link href="/patients?riskLevel=high">
          <Button variant="ghost" size="sm">
            View All <ChevronRight className="ml-1 h-4 w-4" />
          </Button>
        </Link>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {highRiskPatients.length === 0 ? (
            <p className="text-center text-gray-500 py-8">No high-risk patients at this time</p>
          ) : (
            highRiskPatients.map((patient) => (
              <Link
                key={patient.id}
                href={`/patients/${patient.id}`}
                className="block rounded-lg border border-gray-200 p-4 hover:border-medical-primary hover:shadow-sm transition-all"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <p className="font-semibold text-gray-900">
                        {patient.lastName}, {patient.firstName}
                      </p>
                      <Badge
                        className={cn(getRiskBgColor(patient.riskLevel))}
                      >
                        {patient.riskScore}% Risk
                      </Badge>
                    </div>
                    <p className="text-sm text-gray-500 mt-1">
                      MRN: {patient.mrn} | Room {patient.room}-{patient.bed}
                    </p>
                    <p className="text-sm text-gray-600 mt-2">
                      {patient.primaryDiagnosis}
                    </p>
                  </div>
                  <Badge className={cn(getStatusBgColor(patient.clinicalStatus))}>
                    {patient.clinicalStatus}
                  </Badge>
                </div>
                <div className="mt-3 flex items-center text-xs text-gray-500">
                  <Clock className="mr-1 h-3 w-3" />
                  Admitted {formatTimeAgo(patient.admissionDate)}
                </div>
              </Link>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  )
}
