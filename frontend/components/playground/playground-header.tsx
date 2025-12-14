"use client"

import Link from "next/link"
import { Sparkles, Home } from "lucide-react"
import { ThemeToggle } from "@/components/theme-toggle"
import { ModelSelector } from "./model-selector"
import { Button } from "@/components/ui/button"

interface PlaygroundHeaderProps {
  selectedModel: string
  onSelectModel: (model: string) => void
}

export function PlaygroundHeader({ selectedModel, onSelectModel }: PlaygroundHeaderProps) {
  return (
    <header className="h-16 border-b-4 border-foreground bg-background flex items-center justify-between px-4">
      <div className="flex items-center gap-4">
        <Link href="/" className="flex items-center gap-2 group">
          <div className="w-8 h-8 bg-primary neo-border flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-primary-foreground" />
          </div>
          <span className="font-bold hidden sm:inline">fal playground</span>
        </Link>

        <div className="h-6 w-px bg-border hidden sm:block" />

        <ModelSelector selectedModel={selectedModel} onSelectModel={onSelectModel} />
      </div>

      <div className="flex items-center gap-3">
        <ThemeToggle />
        <Link href="/">
          <Button variant="outline" className="neo-border hidden sm:flex bg-transparent">
            <Home className="w-4 h-4 mr-2" />
            Home
          </Button>
        </Link>
      </div>
    </header>
  )
}
