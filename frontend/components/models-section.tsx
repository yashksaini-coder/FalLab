"use client"

import { useState, useEffect } from "react"
import { ArrowRight, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { getModels, type Model } from "@/lib/api"

export function ModelsSection() {
  const [models, setModels] = useState<Model[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchFeaturedModels = async () => {
      try {
        setLoading(true)
        // Fetch pinned/featured models first, then other popular ones
        const { models: allModels } = await getModels(4, 0)
        setModels(allModels.slice(0, 4))
      } catch (error) {
        console.error("Failed to fetch models:", error)
        // Fallback to mock data if API fails
        setModels([])
      } finally {
        setLoading(false)
      }
    }

    fetchFeaturedModels()
  }, [])

  return (
    <section className="py-24 bg-muted/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-12">
          <h2 className="text-3xl sm:text-4xl font-black">Featured Models</h2>
          <Link href="/models">
            <Button variant="outline" className="neo-border font-bold group bg-transparent">
              Explore all models
              <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Button>
          </Link>
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-16">
            <Loader2 className="w-8 h-8 animate-spin mb-4 text-primary" />
            <p className="text-muted-foreground font-bold">Loading featured models...</p>
          </div>
        ) : models.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-16 neo-border bg-card p-12">
            <p className="text-muted-foreground font-bold mb-4">Unable to load featured models</p>
            <Link href="/models">
              <Button className="bg-primary text-primary-foreground neo-border font-bold">
                Browse All Models
              </Button>
            </Link>
          </div>
        ) : (
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {models.map((model) => (
              <Link href={`/playground?model=${model.endpoint_id}`} key={model.endpoint_id}>
                <div className="group neo-border bg-card neo-shadow hover:translate-x-1 hover:translate-y-1 hover:shadow-none transition-all overflow-hidden cursor-pointer h-full flex flex-col">
                  {/* Thumbnail */}
                  <div className="relative aspect-[4/3] overflow-hidden bg-muted flex items-center justify-center">
                    <div className="text-center p-4">
                      <div className="text-4xl mb-2">🤖</div>
                      <p className="text-xs text-muted-foreground">
                        {model.metadata.category || "AI Model"}
                      </p>
                    </div>
                  </div>

                  {/* Content */}
                  <div className="p-4 flex-1 flex flex-col">
                    <h3 className="font-bold text-lg mb-1 line-clamp-2">
                      {model.metadata.display_name}
                    </h3>
                    <p className="text-sm text-muted-foreground mb-3 flex-1">
                      {model.metadata.category || "Model"}
                    </p>
                    {model.metadata.pinned && (
                      <div className="text-xs font-bold text-yellow-600 mb-2">
                        ⭐ Featured
                      </div>
                    )}
                    <p className="text-xs text-muted-foreground truncate font-mono">
                      {model.endpoint_id}
                    </p>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}
