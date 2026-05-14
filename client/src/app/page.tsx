'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Activity, Lock, Mail } from 'lucide-react'
import { Button } from '@/components/ui'
import { useAuthStore } from '@/stores/authStore'

export default function LoginPage() {
  const router = useRouter()
  const { login } = useAuthStore()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    // Demo login
    if (email === 'doctor@medinsight.com' && password === 'demo123') {
      login(
        {
          id: '1',
          email: 'doctor@medinsight.com',
          name: 'Dr. Sarah Johnson',
          role: 'physician',
          department: 'Cardiology',
        },
        'demo-token-12345'
      )
      router.push('/dashboard')
    } else {
      setError('Invalid credentials. Use: doctor@medinsight.com / demo123')
    }

    setIsLoading(false)
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-medical-primary/20 mb-4">
            <Activity className="h-8 w-8 text-medical-secondary" />
          </div>
          <h1 className="text-3xl font-bold text-white">MedInsight</h1>
          <p className="text-gray-400 mt-2">Healthcare Analytics Platform</p>
        </div>

        {/* Login Form */}
        <div className="bg-white rounded-xl shadow-xl p-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Sign in to your account</h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                {error}
              </div>
            )}

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                Email address
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="doctor@medinsight.com"
                  className="w-full rounded-lg border border-gray-300 py-2.5 pl-10 pr-4 focus:border-medical-primary focus:outline-none focus:ring-1 focus:ring-medical-primary"
                  required
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="w-full rounded-lg border border-gray-300 py-2.5 pl-10 pr-4 focus:border-medical-primary focus:outline-none focus:ring-1 focus:ring-medical-primary"
                  required
                />
              </div>
            </div>

            <Button
              type="submit"
              className="w-full"
              size="lg"
              disabled={isLoading}
            >
              {isLoading ? 'Signing in...' : 'Sign in'}
            </Button>
          </form>

          <div className="mt-6 pt-6 border-t border-gray-200">
            <p className="text-sm text-gray-500 text-center">
              Demo credentials:
            </p>
            <div className="mt-2 bg-gray-50 rounded-lg p-3 text-sm font-mono">
              <p className="text-gray-600">Email: doctor@medinsight.com</p>
              <p className="text-gray-600">Password: demo123</p>
            </div>
          </div>
        </div>

        {/* HIPAA Notice */}
        <div className="mt-6 text-center">
          <p className="text-xs text-gray-400">
            This system is for authorized users only. All access is logged for HIPAA compliance.
          </p>
        </div>
      </div>
    </div>
  )
}
