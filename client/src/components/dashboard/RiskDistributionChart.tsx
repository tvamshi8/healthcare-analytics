'use client'

import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui'
import type { RiskDistribution } from '@/types'

interface RiskDistributionChartProps {
  data: RiskDistribution
}

const COLORS = {
  low: '#22c55e',
  medium: '#f59e0b',
  high: '#ef4444',
  critical: '#991b1b',
}

export function RiskDistributionChart({ data }: RiskDistributionChartProps) {
  const chartData = [
    { name: 'Low Risk', value: data.low, color: COLORS.low },
    { name: 'Medium Risk', value: data.medium, color: COLORS.medium },
    { name: 'High Risk', value: data.high, color: COLORS.high },
    { name: 'Critical', value: data.critical, color: COLORS.critical },
  ].filter((item) => item.value > 0)

  const total = data.low + data.medium + data.high + data.critical

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Risk Distribution</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={2}
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                formatter={(value: number) => [
                  `${value} patients (${((value / total) * 100).toFixed(1)}%)`,
                ]}
              />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-4 grid grid-cols-2 gap-4">
          <div className="text-center">
            <p className="text-2xl font-bold text-risk-high">{data.high + data.critical}</p>
            <p className="text-sm text-gray-500">High/Critical</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-risk-low">{data.low}</p>
            <p className="text-sm text-gray-500">Low Risk</p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
