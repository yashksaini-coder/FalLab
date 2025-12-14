import { Video, ImageIcon, AudioLines, Box } from "lucide-react"

const features = [
  {
    icon: ImageIcon,
    title: "Image Generation",
    description: "Create stunning images with FLUX, Stable Diffusion, and more cutting-edge models.",
    color: "bg-primary",
  },
  {
    icon: Video,
    title: "Video Generation",
    description: "Generate high-quality videos with Kling, Wan, and other state-of-the-art models.",
    color: "bg-secondary",
  },
  {
    icon: AudioLines,
    title: "Audio & Speech",
    description: "Text-to-speech, music generation, and audio enhancement capabilities.",
    color: "bg-accent",
  },
  {
    icon: Box,
    title: "3D Generation",
    description: "Create 3D models and assets from text or images with advanced AI.",
    color: "bg-primary",
  },
]

const stats = [
  { value: "600+", label: "Production Models" },
  { value: "1M+", label: "Developers" },
  { value: "99.9%", label: "Uptime SLA" },
  { value: "<100ms", label: "Latency" },
]

export function FeaturesSection() {
  return (
    <section className="py-24 relative">
      {/* Section header */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center mb-16">
          <div>
            <h2 className="text-4xl sm:text-5xl lg:text-6xl font-black leading-tight">
              The world's largest
              <br />
              generative media
              <br />
              <span className="text-primary">model gallery</span>
            </h2>
          </div>
          <div>
            <p className="text-lg text-muted-foreground leading-relaxed">
              Choose from <span className="font-bold text-foreground">600+ production ready</span> image, video, audio
              and 3D models. Build products using fal model APIs. Scale custom AI models with fal serverless.
            </p>
          </div>
        </div>

        {/* Feature cards */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-20">
          {features.map((feature, index) => (
            <div
              key={index}
              className="group neo-border bg-card neo-shadow hover:translate-x-1 hover:translate-y-1 hover:shadow-none transition-all cursor-pointer"
            >
              <div className="p-6">
                <div className={`w-14 h-14 ${feature.color} neo-border flex items-center justify-center mb-4`}>
                  <feature.icon className="w-7 h-7 text-primary-foreground" />
                </div>
                <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                <p className="text-muted-foreground text-sm leading-relaxed">{feature.description}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Stats section */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map((stat, index) => (
            <div key={index} className="p-6 neo-border bg-muted text-center">
              <div className="text-3xl sm:text-4xl font-black text-primary mb-1">{stat.value}</div>
              <div className="text-sm text-muted-foreground font-medium">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
