"use client"

import Link from "next/link"
import { useState } from "react"
import { Menu, X, Sparkles } from "lucide-react"
import { ThemeToggle } from "./theme-toggle"
import { Button } from "@/components/ui/button"

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b-4 border-foreground">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group">
            <div className="w-10 h-10 bg-primary neo-border flex items-center justify-center neo-shadow-sm group-hover:translate-x-1 group-hover:translate-y-1 group-hover:shadow-none transition-all">
              <Sparkles className="w-6 h-6 text-primary-foreground" />
            </div>
            <span className="text-xl font-bold tracking-tight">FalLab</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-1">
            <Link href="/" className="px-4 py-2 font-medium hover:bg-muted transition-colors">
              Explore
            </Link>
            <Link href="/models" className="px-4 py-2 font-medium hover:bg-muted transition-colors">
              Models
            </Link>
            <Link href="/playground" className="px-4 py-2 font-medium hover:bg-muted transition-colors">
              Playground
            </Link>
            <Link href="/health" className="px-4 py-2 font-medium hover:bg-muted transition-colors">
              Health
            </Link>
            <Link href="#" className="px-4 py-2 font-medium hover:bg-muted transition-colors">
              Documentation
            </Link>
          </div>

          {/* Right side */}
          <div className="hidden md:flex items-center gap-3">
            <ThemeToggle />
            <Button className="bg-primary text-primary-foreground neo-border neo-shadow-sm hover:translate-x-1 hover:translate-y-1 hover:shadow-none transition-all font-bold">
              Login
            </Button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center gap-2">
            <ThemeToggle />
            <button onClick={() => setIsOpen(!isOpen)} className="p-2 neo-border bg-background">
              {isOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <div className="md:hidden bg-background border-b-4 border-foreground">
          <div className="px-4 py-4 space-y-2">
            <Link href="/" className="block px-4 py-3 font-medium neo-border bg-muted" onClick={() => setIsOpen(false)}>
              Explore
            </Link>
            <Link href="/models" className="block px-4 py-3 font-medium neo-border bg-muted" onClick={() => setIsOpen(false)}>
              Models
            </Link>
            <Link
              href="/playground"
              className="block px-4 py-3 font-medium neo-border bg-muted"
              onClick={() => setIsOpen(false)}
            >
              Playground
            </Link>
            <Link href="/health" className="block px-4 py-3 font-medium neo-border bg-muted" onClick={() => setIsOpen(false)}>
              Health
            </Link>
            <Link href="#" className="block px-4 py-3 font-medium neo-border bg-muted">
              Documentation
            </Link>
            <div className="pt-4 flex flex-col gap-2">
              <Button variant="outline" className="w-full neo-border font-bold bg-transparent">
                Contact Sales
              </Button>
              <Button className="w-full bg-primary text-primary-foreground neo-border font-bold">Login</Button>
            </div>
          </div>
        </div>
      )}
    </nav>
  )
}
