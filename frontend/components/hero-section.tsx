"use client"

import { ArrowRight, Play, Zap } from "lucide-react"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export function HeroSection() {
  return (
    <section className="relative min-h-screen pt-24 pb-16 overflow-hidden">
      {/* Cyberpunk grid background */}
      <div className="absolute inset-0 cyber-grid opacity-30" />

      {/* Decorative shapes */}
      <div className="absolute top-32 left-10 w-20 h-20 bg-primary neo-border rotate-12 hidden lg:block" />
      <div className="absolute top-48 right-16 w-16 h-16 bg-secondary neo-border -rotate-6 hidden lg:block" />
      <div className="absolute bottom-32 left-24 w-12 h-12 bg-accent neo-border rotate-45 hidden lg:block" />
      <div className="absolute top-1/3 right-1/4 w-24 h-24 border-4 border-primary rotate-12 hidden xl:block" />

      {/* Pixel art decorations */}
      <div className="absolute top-40 right-10 hidden lg:grid grid-cols-4 gap-1">
        {[...Array(16)].map((_, i) => (
          <div key={i} className={`w-3 h-3 ${Math.random() > 0.5 ? "bg-secondary" : "bg-transparent"}`} />
        ))}
      </div>

      <div className="absolute bottom-40 left-10 hidden lg:grid grid-cols-5 gap-1">
        {[...Array(25)].map((_, i) => (
          <div key={i} className={`w-2 h-2 ${Math.random() > 0.6 ? "bg-primary" : "bg-transparent"}`} />
        ))}
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Announcement banner */}
        <div className="flex justify-center mb-8">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-secondary/10 neo-border text-sm font-medium">
            <Zap className="w-4 h-4 text-secondary" />
            <span>FalLab Playground is here - create with AI instantly!</span>
            <ArrowRight className="w-4 h-4" />
          </div>
        </div>

        {/* Main hero content */}
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl sm:text-6xl lg:text-8xl font-black tracking-tight mb-6 leading-[0.9]">
            <span className="text-primary">G</span>enerative
            <br />
            <span className="relative inline-block">
              media platform
              <div className="absolute -bottom-2 left-0 right-0 h-4 bg-accent -z-10" />
            </span>
            <br />
            for developers.
          </h1>

          <p className="text-lg sm:text-xl text-muted-foreground max-w-2xl mx-auto mb-10 leading-relaxed">
            The world's best generative image, video, and audio models, all in one place. Develop and fine-tune models
            with serverless GPUs and on-demand clusters.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/playground">
              <Button
                size="lg"
                className="bg-foreground text-background neo-border neo-shadow hover:translate-x-1 hover:translate-y-1 hover:shadow-none transition-all text-lg px-8 py-6 font-bold"
              >
                Get started
                <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
            </Link>
          </div>
        </div>

        {/* Trusted by section */}
        <div className="mt-20">
          <p className="text-center text-sm text-muted-foreground mb-8">
            Trusted by over <span className="font-bold text-foreground">1,000,000</span> developers and leading
            companies
          </p>
          <div className="flex flex-wrap items-center justify-center gap-8 md:gap-12 opacity-60">
            {["Adobe", "Shopify", "Canva", "Quora", "Perplexity", "PlayAI"].map((company) => (
              <span key={company} className="text-xl font-bold tracking-tight">
                {company}
              </span>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
