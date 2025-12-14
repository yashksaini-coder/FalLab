/**
 * FalLab API Client
 * Connects to the backend services for model discovery and generation
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"

export interface Model {
  endpoint_id: string
  metadata: {
    display_name: string
    category: string
    description?: string
    status: string
    tags: string[]
    thumbnail_url?: string
    model_url?: string
    license_type?: string
    pinned?: boolean
    highlighted?: boolean
    duration_estimate?: number
  }
}

export interface GenerationRequest {
  model_id: string
  prompt: string
  parameters?: Record<string, any>
}

export interface GenerationResponse {
  request_id: string
  status: "queued" | "processing" | "completed" | "failed"
  model_id: string
  created_at: string
  completed_at?: string
  result?: Record<string, any>
  error?: string
  queue_position?: number
}

export interface HealthResponse {
  status: string
  timestamp: string
  services?: {
    backend: string
    redis: string
  }
}

// Health Check
export async function getHealth(): Promise<HealthResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return await response.json()
  } catch (error) {
    console.error("Health check failed:", error)
    throw error
  }
}

// Models API

export async function getModels(limit = 50, skip = 0, category?: string): Promise<{
  models: Model[]
  total: number
  next_cursor: string | null
}> {
  try {
    const params = new URLSearchParams({
      limit: limit.toString(),
      skip: skip.toString(),
      ...(category && { category }),
    })

    const response = await fetch(`${API_BASE_URL}/models?${params}`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return await response.json()
  } catch (error) {
    console.error("Failed to fetch models:", error)
    throw error
  }
}

export async function searchModels(query: string, limit = 20): Promise<{
  models: Model[]
  total: number
  query: string
}> {
  try {
    const params = new URLSearchParams({
      q: query,
      limit: limit.toString(),
    })

    const response = await fetch(`${API_BASE_URL}/models/search?${params}`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return await response.json()
  } catch (error) {
    console.error("Failed to search models:", error)
    throw error
  }
}

export async function getCategories(): Promise<{
  categories: string[]
  total: number
}> {
  try {
    const response = await fetch(`${API_BASE_URL}/models/categories`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return await response.json()
  } catch (error) {
    console.error("Failed to fetch categories:", error)
    throw error
  }
}

export async function getModelDetail(modelId: string): Promise<Model> {
  try {
    const response = await fetch(`${API_BASE_URL}/models/${encodeURIComponent(modelId)}`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return await response.json()
  } catch (error) {
    console.error(`Failed to fetch model ${modelId}:`, error)
    throw error
  }
}

export async function refreshModels(): Promise<{
  status: string
  total_models: number
  message: string
}> {
  try {
    const response = await fetch(`${API_BASE_URL}/models/refresh`, {
      method: "POST",
    })
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return await response.json()
  } catch (error) {
    console.error("Failed to refresh models:", error)
    throw error
  }
}

// Generation API

export async function submitGeneration(
  request: GenerationRequest,
): Promise<GenerationResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    })
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.message || `HTTP ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    console.error("Failed to submit generation:", error)
    throw error
  }
}

export async function submitGenerationSync(
  request: GenerationRequest,
): Promise<GenerationResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/generate/sync`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    })
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.message || `HTTP ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    console.error("Failed to submit sync generation:", error)
    throw error
  }
}

export async function getGenerationStatus(requestId: string): Promise<GenerationResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/status/${requestId}`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return await response.json()
  } catch (error) {
    console.error(`Failed to fetch status for ${requestId}:`, error)
    throw error
  }
}

// Polling utility
export async function pollGenerationUntilComplete(
  requestId: string,
  maxWaitMs = 600000,
  pollIntervalMs = 2000,
): Promise<GenerationResponse> {
  const startTime = Date.now()

  while (Date.now() - startTime < maxWaitMs) {
    try {
      const status = await getGenerationStatus(requestId)

      if (status.status === "completed" || status.status === "failed") {
        return status
      }

      // Wait before next poll
      await new Promise((resolve) => setTimeout(resolve, pollIntervalMs))
    } catch (error) {
      console.error("Polling error:", error)
      throw error
    }
  }

  throw new Error("Generation request timeout")
}
