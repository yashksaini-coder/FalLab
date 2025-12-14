"use client"

import { useState } from "react"
import { ChevronDown, ImageIcon, Video, AudioLines, Box } from "lucide-react"
import { cn } from "@/lib/utils"

const modelCategories = [
  {
    name: "Image",
    icon: ImageIcon,
    models: [
      { id: "flux-kontext", name: "FLUX.1 Kontext", badge: "Popular" },
      { id: "flux-pro", name: "FLUX.1 Pro", badge: null },
      { id: "sdxl", name: "Stable Diffusion XL", badge: null },
      { id: "dalle3", name: "DALL-E 3", badge: null },
    ],
  },
  {
    name: "Video",
    icon: Video,
    models: [
      { id: "kling", name: "Kling v2.5", badge: "New" },
      { id: "wan", name: "Wan 2.5", badge: null },
      { id: "veo", name: "Veo 3.1", badge: "Premium" },
    ],
  },
  {
    name: "Audio",
    icon: AudioLines,
    models: [
      { id: "tts", name: "Text to Speech", badge: null },
      { id: "music", name: "Music Gen", badge: null },
    ],
  },
  {
    name: "3D",
    icon: Box,
    models: [{ id: "mesh", name: "3D Mesh Gen", badge: "Beta" }],
  },
]

interface ModelSelectorProps {
  selectedModel: string
  onSelectModel: (model: string) => void
}

export function ModelSelector({ selectedModel, onSelectModel }: ModelSelectorProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [activeCategory, setActiveCategory] = useState("Image")

  const getSelectedModelName = () => {
    for (const category of modelCategories) {
      const model = category.models.find((m) => m.id === selectedModel)
      if (model) return model.name
    }
    return "Select Model"
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
        <div className="absolute top-full left-0 mt-2 w-80 neo-border bg-card neo-shadow z-50">
          {/* Category tabs */}
          <div className="flex border-b-4 border-foreground">
            {modelCategories.map((category) => (
              <button
                key={category.name}
                onClick={() => setActiveCategory(category.name)}
                className={cn(
                  "flex-1 flex items-center justify-center gap-1 p-3 text-sm font-bold transition-colors",
                  activeCategory === category.name ? "bg-primary text-primary-foreground" : "hover:bg-muted",
                )}
              >
                <category.icon className="w-4 h-4" />
                <span className="hidden sm:inline">{category.name}</span>
              </button>
            ))}
          </div>

          {/* Model list */}
          <div className="p-2 max-h-64 overflow-y-auto">
            {modelCategories
              .find((c) => c.name === activeCategory)
              ?.models.map((model) => (
                <button
                  key={model.id}
                  onClick={() => {
                    onSelectModel(model.id)
                    setIsOpen(false)
                  }}
                  className={cn(
                    "w-full flex items-center justify-between p-3 text-left transition-colors",
                    selectedModel === model.id ? "bg-primary/20" : "hover:bg-muted",
                  )}
                >
                  <span className="font-medium">{model.name}</span>
                  {model.badge && (
                    <span className="px-2 py-0.5 bg-secondary text-secondary-foreground text-xs font-bold">
                      {model.badge}
                    </span>
                  )}
                </button>
              ))}
          </div>
        </div>
      )}
    </div>
  )
}
