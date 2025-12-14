"use client"

import { useState, useEffect } from "react"
import { Search, Loader2, ChevronRight, Star } from "lucide-react"
import Link from "next/link"
import { getModels, searchModels, getCategories, type Model } from "@/lib/api"

export default function ModelsPage() {
  const [models, setModels] = useState<Model[]>([])
  const [categories, setCategories] = useState<string[]>([])
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState("")
  const [loading, setLoading] = useState(true)
  const [searching, setSearching] = useState(false)

  // Fetch categories on mount
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const { categories: cats } = await getCategories()
        setCategories(cats)
        if (cats.length > 0) {
          setSelectedCategory(cats[0])
        }
      } catch (error) {
        console.error("Failed to fetch categories:", error)
      }
    }

    fetchCategories()
  }, [])

  // Fetch models based on category or search
  useEffect(() => {
    const fetchModels = async () => {
      try {
        setLoading(true)

        if (searchQuery.trim()) {
          // Search mode
          setSearching(true)
          const { models: searchResults } = await searchModels(searchQuery, 100)
          setModels(searchResults)
        } else if (selectedCategory) {
          // Category mode
          setSearching(false)
          const { models: catModels } = await getModels(100, 0, selectedCategory)
          setModels(catModels)
        } else {
          // All models
          setSearching(false)
          const { models: allModels } = await getModels(100, 0)
          setModels(allModels)
        }
      } catch (error) {
        console.error("Failed to fetch models:", error)
        setModels([])
      } finally {
        setLoading(false)
      }
    }

    const timer = setTimeout(fetchModels, 300) // Debounce search
    return () => clearTimeout(timer)
  }, [searchQuery, selectedCategory])

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="sticky top-0 z-40 border-b-4 border-foreground bg-card">
        <div className="max-w-6xl mx-auto px-4 md:px-8 py-6">
          <Link href="/" className="text-sm font-bold text-muted-foreground hover:text-foreground mb-4 inline-block">
            ← Back
          </Link>
          <h1 className="text-4xl font-bold mb-2">Model Explorer</h1>
          <p className="text-muted-foreground mb-6">Browse and search AI models available in FalLab</p>

          {/* Search bar */}
          <div className="relative">
            <Search className="absolute left-3 top-3 w-5 h-5 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search models by name, capability, or description..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 neo-border bg-background text-foreground placeholder:text-muted-foreground focus:outline-none"
            />
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 md:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar - Categories */}
          {!searchQuery && (
            <div className="lg:w-56 flex-shrink-0">
              <div className="neo-border bg-card p-6 sticky top-24">
                <h3 className="text-lg font-bold mb-4">Categories</h3>
                <div className="space-y-2">
                  <button
                    onClick={() => setSelectedCategory(null)}
                    className={`w-full text-left px-3 py-2 transition-colors font-medium ${
                      selectedCategory === null
                        ? "bg-primary text-primary-foreground"
                        : "hover:bg-muted text-foreground"
                    }`}
                  >
                    All Models
                  </button>
                  {categories.map((category) => (
                    <button
                      key={category}
                      onClick={() => setSelectedCategory(category)}
                      className={`w-full text-left px-3 py-2 transition-colors font-medium ${
                        selectedCategory === category
                          ? "bg-primary text-primary-foreground"
                          : "hover:bg-muted text-foreground"
                      }`}
                    >
                      {category}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Models Grid */}
          <div className="flex-1">
            {loading ? (
              <div className="flex flex-col items-center justify-center py-16">
                <Loader2 className="w-8 h-8 animate-spin mb-4 text-primary" />
                <p className="text-muted-foreground font-bold">Loading models...</p>
              </div>
            ) : models.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-16">
                <div className="text-6xl mb-4">🔍</div>
                <h3 className="text-2xl font-bold mb-2">No models found</h3>
                <p className="text-muted-foreground">
                  {searchQuery ? "Try a different search query" : "No models available in this category"}
                </p>
              </div>
            ) : (
              <>
                <div className="mb-6 flex items-center justify-between">
                  <h2 className="text-lg font-bold">
                    {searching ? "Search Results" : selectedCategory || "All Models"}{" "}
                    <span className="text-muted-foreground text-sm">({models.length})</span>
                  </h2>
                </div>

                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {models.map((model) => (
                    <Link
                      key={model.endpoint_id}
                      href={`/playground?model=${model.endpoint_id}`}
                      className="group neo-border bg-card p-6 hover:bg-primary/10 transition-colors cursor-pointer"
                    >
                      {/* Header */}
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <h3 className="font-bold text-base group-hover:text-primary transition-colors">
                            {model.metadata.display_name}
                          </h3>
                          <p className="text-xs text-muted-foreground font-mono truncate">
                            {model.endpoint_id}
                          </p>
                        </div>
                        {model.metadata.pinned && (
                          <Star className="w-5 h-5 text-yellow-500 fill-yellow-500 flex-shrink-0 ml-2" />
                        )}
                      </div>

                      {/* Category */}
                      <div className="mb-3">
                        <span className="inline-block px-2 py-1 bg-muted text-xs font-bold">
                          {model.metadata.category || "General"}
                        </span>
                      </div>

                      {/* Description */}
                      {model.metadata.description && (
                        <p className="text-sm text-muted-foreground mb-4 line-clamp-2">
                          {model.metadata.description}
                        </p>
                      )}

                      {/* Tags */}
                      {model.metadata.tags && model.metadata.tags.length > 0 && (
                        <div className="mb-4 flex flex-wrap gap-1">
                          {model.metadata.tags.slice(0, 3).map((tag) => (
                            <span key={tag} className="text-xs px-2 py-0.5 bg-secondary/30 rounded">
                              {tag}
                            </span>
                          ))}
                          {model.metadata.tags.length > 3 && (
                            <span className="text-xs px-2 py-0.5 text-muted-foreground">
                              +{model.metadata.tags.length - 3}
                            </span>
                          )}
                        </div>
                      )}

                      {/* Footer */}
                      <div className="flex items-center justify-between pt-4 border-t-2 border-foreground/20">
                        <div className="flex items-center gap-1 text-xs text-muted-foreground">
                          <span>Use Model</span>
                          <ChevronRight className="w-3 h-3 group-hover:translate-x-1 transition-transform" />
                        </div>
                        <span className="text-xs font-mono px-2 py-1 bg-primary/10 rounded">
                          {model.metadata.status}
                        </span>
                      </div>
                    </Link>
                  ))}
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
