import { ArrowRight, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export function CTASection() {
  return (
    <section className="py-24 relative overflow-hidden">
      {/* Background pattern */}
      <div className="absolute inset-0 cyber-grid opacity-20" />

      {/* Decorative elements */}
      <div className="absolute top-10 left-10 w-16 h-16 bg-primary neo-border rotate-12 hidden lg:block" />
      <div className="absolute bottom-10 right-10 w-20 h-20 bg-secondary neo-border -rotate-6 hidden lg:block" />
      <div className="absolute top-1/2 left-20 w-8 h-8 bg-accent neo-border hidden xl:block" />

      <div className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 neo-border mb-8">
          <Sparkles className="w-5 h-5 text-primary" />
          <span className="font-bold">Ready to create?</span>
        </div>

        <h2 className="text-4xl sm:text-5xl lg:text-6xl font-black mb-6 leading-tight">
          Build, deploy,
          <br />
          <span className="relative inline-block">
            train
            <div className="absolute -bottom-1 left-0 right-0 h-3 bg-accent -z-10" />
          </span>
          .
        </h2>

        <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-10 leading-relaxed">
          Start generating images and videos in minutes. Access the world's best AI models through our simple API or
          interactive playground.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button
            variant="outline"
            size="lg"
            className="neo-border text-lg px-8 py-6 font-bold hover:text-white text-muted-foreground hover:bg-muted bg-transparent"
            >
            View documentation
            </Button>
        </div>

        <p className="mt-8 text-sm text-muted-foreground">No credit card required · Free tier available</p>
      </div>
    </section>
  )
}
