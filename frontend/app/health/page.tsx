"use client"

import { useEffect, useState } from "react"
import { Activity, Database, Server, AlertCircle, CheckCircle, Clock } from "lucide-react"
import Link from "next/link"
import { getHealth } from "@/lib/api"

interface HealthData {
  status: string
  timestamp: string
  version?: string
  redis?: {
    connected: boolean
    latency_ms?: number
  }
  services?: Record<string, any>
}

export default function HealthPage() {
  const [health, setHealth] = useState<HealthData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [lastRefresh, setLastRefresh] = useState<Date>(new Date())

  const fetchHealth = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await getHealth()
      setHealth(data)
      setLastRefresh(new Date())
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch health status")
      setHealth(null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchHealth()
    const interval = setInterval(fetchHealth, 10000) // Refresh every 10 seconds
    return () => clearInterval(interval)
  }, [])

  const isHealthy = health?.status === "healthy"

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Link href="/" className="text-sm font-bold text-muted-foreground hover:text-foreground mb-4 inline-block">
            ← Back
          </Link>
          <h1 className="text-4xl font-bold mb-2">System Health</h1>
          <p className="text-muted-foreground">Real-time backend service status monitoring</p>
        </div>

        {/* Status cards */}
        <div className="grid gap-4 mb-8">
          {/* Overall Status */}
          <div className="neo-border bg-card p-6">
            <div className="flex items-start justify-between mb-4">
              <h2 className="text-lg font-bold">Overall Status</h2>
              {loading && <Clock className="w-5 h-5 animate-spin text-muted-foreground" />}
            </div>
            {error && (
              <div className="flex items-center gap-3 p-4 bg-destructive/10 border-2 border-destructive rounded">
                <AlertCircle className="w-5 h-5 text-destructive flex-shrink-0" />
                <div>
                  <p className="font-bold text-destructive">Connection Error</p>
                  <p className="text-sm text-destructive/80">{error}</p>
                </div>
              </div>
            )}
            {health && !error && (
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  {isHealthy ? (
                    <CheckCircle className="w-6 h-6 text-green-500" />
                  ) : (
                    <AlertCircle className="w-6 h-6 text-yellow-500" />
                  )}
                  <div>
                    <p className="font-bold capitalize">{health.status}</p>
                    <p className="text-sm text-muted-foreground">API operational status</p>
                  </div>
                </div>
                {health.version && (
                  <div className="text-sm">
                    <span className="text-muted-foreground">API Version: </span>
                    <span className="font-mono font-bold">{health.version}</span>
                  </div>
                )}
              </div>
            )}
            <div className="mt-4 text-xs text-muted-foreground">
              Last updated: {lastRefresh.toLocaleTimeString()}
            </div>
          </div>

          {/* Redis Status */}
          {health?.redis && (
            <div className="neo-border bg-card p-6">
              <div className="flex items-center gap-3 mb-4">
                <Database className="w-5 h-5" />
                <h2 className="text-lg font-bold">Redis Cache</h2>
              </div>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 bg-muted rounded">
                  <span className="text-sm font-medium">Connection Status</span>
                  <div className="flex items-center gap-2">
                    {health.redis.connected ? (
                      <>
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        <span className="text-sm font-bold text-green-500">Connected</span>
                      </>
                    ) : (
                      <>
                        <AlertCircle className="w-4 h-4 text-red-500" />
                        <span className="text-sm font-bold text-red-500">Disconnected</span>
                      </>
                    )}
                  </div>
                </div>
                {health.redis.latency_ms !== undefined && (
                  <div className="flex items-center justify-between p-3 bg-muted rounded">
                    <span className="text-sm font-medium">Latency</span>
                    <span className="text-sm font-mono font-bold">{health.redis.latency_ms}ms</span>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Services Status */}
          {health?.services && Object.keys(health.services).length > 0 && (
            <div className="neo-border bg-card p-6">
              <div className="flex items-center gap-3 mb-4">
                <Server className="w-5 h-5" />
                <h2 className="text-lg font-bold">External Services</h2>
              </div>
              <div className="space-y-2">
                {Object.entries(health.services).map(([service, status]: [string, any]) => (
                  <div key={service} className="flex items-center justify-between p-3 bg-muted rounded">
                    <span className="text-sm font-medium capitalize">{service}</span>
                    <div className="flex items-center gap-2">
                      {status.status === "ok" ? (
                        <>
                          <CheckCircle className="w-4 h-4 text-green-500" />
                          <span className="text-sm font-bold text-green-500">OK</span>
                        </>
                      ) : (
                        <>
                          <AlertCircle className="w-4 h-4 text-red-500" />
                          <span className="text-sm font-bold text-red-500">Error</span>
                        </>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Raw Response */}
        {health && (
          <div className="neo-border bg-card p-6">
            <h2 className="text-lg font-bold mb-4">Raw Response</h2>
            <div className="p-4 bg-muted font-mono text-xs overflow-x-auto neo-border">
              <pre>{JSON.stringify(health, null, 2)}</pre>
            </div>
          </div>
        )}

        {/* Refresh button */}
        <div className="mt-8 flex justify-center">
          <button
            onClick={fetchHealth}
            disabled={loading}
            className="px-6 py-3 font-bold neo-border bg-primary text-primary-foreground hover:opacity-90 disabled:opacity-50 transition-all"
          >
            {loading ? "Refreshing..." : "Refresh Status"}
          </button>
        </div>
      </div>
    </div>
  )
}
