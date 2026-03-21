import { LucideIcon } from 'lucide-react'
import { Card, CardContent } from '@/components/ui'
import { cn } from '@/lib/utils'

interface MetricCardProps {
  title: string
  value: string | number
  change?: number
  changeLabel?: string
  icon: LucideIcon
  iconColor?: string
  trend?: 'up' | 'down'
}

export function MetricCard({
  title,
  value,
  change,
  changeLabel,
  icon: Icon,
  iconColor = 'text-medical-primary',
  trend,
}: MetricCardProps) {
  const isPositive = trend === 'up' || (change !== undefined && change > 0)
  const showTrend = change !== undefined && change !== 0

  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-sm font-medium text-gray-500">{title}</p>
            <p className="mt-2 text-3xl font-bold text-gray-900">{value}</p>
            {showTrend && (
              <p
                className={cn(
                  'mt-2 text-sm font-medium',
                  isPositive ? 'text-green-600' : 'text-red-600'
                )}
              >
                {isPositive ? '+' : ''}
                {change}% {changeLabel || 'vs last period'}
              </p>
            )}
            {!showTrend && changeLabel && (
              <p className="mt-2 text-sm text-gray-500">{changeLabel}</p>
            )}
          </div>
          <div className={cn('rounded-lg bg-gray-50 p-3', iconColor)}>
            <Icon className="h-6 w-6" />
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
