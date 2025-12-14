"use client"

import { useState, useEffect } from "react"
import { ChevronDown, ImageIcon, Video, AudioLines, Box, Loader2 } from "lucide-react"
import { cn } from "@/lib/utils"
import { getCategories, getModels, type Model } from "@/lib/api"

const categoryIcons: Record<string, any> = {
  "text-to-image": ImageIcon,
  "image-to-image": ImageIcon,
  "text-to-video": Video,
  "image-to-video": Video,
  "audio-generation": AudioLines,
  "3d-generation": Box,
  "image-generation": ImageIcon,
  "video-generation": Video,
}

interface ModelSelectorProps {
  selectedModel: string
  onSelectModel: (model: string) => void
}

export function ModelSelector({ selectedModel, onSelectModel }: ModelSelectorProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [activeCategory, setActiveCategory] = useState<string | null>(null)
  const [categories, setCategories] = useState<string[]>([])
  const [modelsByCategory, setModelsByCategory] = useState<Record<string, Model[]>>({})
  const [loading, setLoading] = useState(true)
  const [selectedModelData, setSelectedModelData] = useState<Model | null>(null)

  // Fetch categories and models on mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const { categories: cats } = await getCategories()
        setCategories(cats)

        if (cats.length > 0) {
          setActiveCategory(cats[0])

          // Fetch models for each category
          const byCategory: Record<string, Model[]> = {}
          for (const cat of cats) {
            try {
              const { models } = await getModels(50, 0, cat)
              byCategory[cat] = models
            } catch (error) {
              console.error(`Failed to fetch models for ${cat}:`, error)
              byCategory[cat] = []
            }
          }
          setModelsByCategory(byCategory)
        }
      } catch (error) {
        console.error("Failed to fetch categories:", error)
        setCategories([])
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  // Update selected model data when selectedModel changes
  useEffect(() => {
    const findModel = (): Model | null => {
      for (const models of Object.values(modelsByCategory)) {
        const model = models.find((m) => m.endpoint_id === selectedModel)
        if (model) return model
      }
      return null
    }
    setSelectedModelData(findModel())
  }, [selectedModel, modelsByCategory])

  const getSelectedModelName = () => {
    return selectedModelData?.metadata.display_name || "Select Model"
  }

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 neo-border bg-card hover:bg-muted transition-colors font-bold"
      >
        <span>{getSelectedModelName()}</span>
        <ChevronDown className={cn("w-4 h-4 transition-transform", isOpen && "rotate-180")} />
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 mt-2 w-96 neo-border bg-card neo-shadow z-50 max-h-96 overflow-hidden flex flex-col">
          {/* Loading state */}
          {loading ? (
            <div className="flex items-center justify-center p-8">
              <Loader2 className="w-5 h-5 animate-spin mr-2" />
              <span className="text-sm">Loading models...</span>
            </div>
          ) : (
            <>
              {/* Category tabs */}
              <div className="flex border-b-4 border-foreground overflow-x-auto">
                {categories.map((category) => {
                  const Icon = categoryIcons[category] || Box
                  return (
                    <button
                      key={category}
                      onClick={() => setActiveCategory(category)}
                      className={cn(
                        "flex-shrink-0 flex items-center justify-center gap-1 p-3 text-xs font-bold transition-colors",
                        activeCategory === category
                          ? "bg-primary text-primary-foreground"
                          : "hover:bg-muted",
                      )}
                      title={category}
                    >
                      <Icon className="w-4 h-4" />
                      <span className="hidden sm:inline line-clamp-1">{category}</span>
                    </button>
                  )
                })}
              </div>

              {/* Model list */}
              <div className="flex-1 p-2 overflow-y-auto">
                {activeCategory && modelsByCategory[activeCategory]?.length > 0 ? (
                  modelsByCategory[activeCategory].map((model) => (
                    <button
                      key={model.endpoint_id}
                      onClick={() => {
                        onSelectModel(model.endpoint_id)
                        setIsOpen(false)
                      }}
                      className={cn(
                        "w-full flex items-center justify-between gap-2 p-3 text-left transition-colors text-sm",
                        selectedModel === model.endpoint_id
                          ? "bg-primary/20 border-l-4 border-primary"
                          : "hover:bg-muted",
                      )}
                    >
                      <div className="flex-1 min-w-0">
                        <div className="font-medium truncate">{model.metadata.display_name}</div>
                        <div className="text-xs text-muted-foreground truncate">{model.endpoint_id}</div>
                      </div>
                      {model.metadata.pinned && (
                        <span className="px-2 py-0.5 bg-secondary text-secondary-foreground text-xs font-bold flex-shrink-0">
                          ★
                        </span>
                      )}
                    </button>
                  ))
                ) : (
                  <div className="p-4 text-center text-sm text-muted-foreground">
                    No models available
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  )
}
