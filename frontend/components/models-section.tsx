import { ArrowRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import Link from "next/link"

const models = [
  {
    name: "FLUX.1 Kontext",
    category: "Image Generation",
    image: "/cyberpunk-portrait-digital-art-neon.jpg",
    tag: "Popular",
  },
  {
    name: "Kling v2.5",
    category: "Text to Video",
    image: "/cute-fluffy-animal-3d-render.jpg",
    tag: "New",
  },
  {
    name: "Wan 2.5",
    category: "Image to Video",
    image: "/futuristic-city-skyline-night-neon.jpg",
    tag: "Trending",
  },
  {
    name: "Veo 3.1",
    category: "Video Generation",
    image: "/abstract-digital-art-gradient-waves.jpg",
    tag: "Premium",
  },
]

export function ModelsSection() {
  return (
    <section className="py-24 bg-muted/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-12">
          <h2 className="text-3xl sm:text-4xl font-black">Featured Models</h2>
          <Link href="/playground">
            <Button variant="outline" className="neo-border font-bold group bg-transparent">
              Explore all models
              <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Button>
          </Link>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {models.map((model, index) => (
            <Link href="/playground" key={index}>
              <div className="group neo-border bg-card neo-shadow hover:translate-x-1 hover:translate-y-1 hover:shadow-none transition-all overflow-hidden cursor-pointer">
                <div className="relative aspect-[4/3] overflow-hidden">
                  <img
                    src={model.image || "/placeholder.svg"}
                    alt={model.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div className="absolute top-3 right-3">
                    <span className="px-3 py-1 bg-foreground text-background text-xs font-bold">{model.tag}</span>
                  </div>
                </div>
                <div className="p-4">
                  <h3 className="font-bold text-lg mb-1">{model.name}</h3>
                  <p className="text-sm text-muted-foreground">{model.category}</p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  )
}
