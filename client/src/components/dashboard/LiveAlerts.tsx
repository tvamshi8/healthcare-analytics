'use client'

import { Bell, Check, AlertTriangle, Activity, TrendingDown } from 'lucide-react'
import { Card, CardHeader, CardTitle, CardContent, Badge, Button } from '@/components/ui'
import { cn, formatTimeAgo } from '@/lib/utils'
import type { Alert } from '@/types'

interface LiveAlertsProps {
  alerts: Alert[]
  onAcknowledge: (id: string) => void
}

const alertIcons = {
  vitals: Activity,
  risk: TrendingDown,
  deterioration: AlertTriangle,
  discharge: Bell,
}

const severityColors = {
  info: 'bg-blue-100 text-blue-800',
  warning: 'bg-amber-100 text-amber-800',
  critical: 'bg-red-100 text-red-800',
}

export function LiveAlerts({ alerts, onAcknowledge }: LiveAlertsProps) {
  const unacknowledged = alerts.filter((a) => !a.acknowledged)

  return (
    <Card className="h-full">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="flex items-center">
          <Bell className="mr-2 h-5 w-5 text-amber-500" />
          Live Alerts
          {unacknowledged.length > 0 && (
            <Badge variant="danger" className="ml-2">
              {unacknowledged.length}
            </Badge>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3 max-h-80 overflow-y-auto scrollbar-thin">
          {alerts.length === 0 ? (
            <p className="text-center text-gray-500 py-8">No active alerts</p>
          ) : (
            alerts.slice(0, 10).map((alert) => {
              const Icon = alertIcons[alert.type]
              return (
                <div
                  key={alert.id}
                  className={cn(
                    'rounded-lg border p-3 transition-all',
                    alert.acknowledged
                      ? 'border-gray-100 bg-gray-50 opacity-60'
                      : 'border-amber-200 bg-amber-50'
                  )}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-3">
                      <div
                        className={cn(
                          'rounded-full p-2',
                          alert.severity === 'critical'
                            ? 'bg-red-100 text-red-600'
                            : alert.severity === 'warning'
                            ? 'bg-amber-100 text-amber-600'
                            : 'bg-blue-100 text-blue-600'
                        )}
                      >
                        <Icon className="h-4 w-4" />
                      </div>
                      <div>
                        <div className="flex items-center space-x-2">
                          <p className="font-medium text-gray-900 text-sm">{alert.title}</p>
                          <Badge className={cn(severityColors[alert.severity])}>
                            {alert.severity}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mt-1">{alert.message}</p>
                        <p className="text-xs text-gray-500 mt-1">
                          {alert.patientName} | {formatTimeAgo(alert.createdAt)}
                        </p>
                      </div>
                    </div>
                    {!alert.acknowledged && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onAcknowledge(alert.id)}
                        className="text-gray-400 hover:text-gray-600"
                      >
                        <Check className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                </div>
              )
            })
          )}
        </div>
      </CardContent>
    </Card>
  )
}
