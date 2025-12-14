import Link from "next/link"
import { Sparkles, Github, Twitter, Linkedin, Youtube } from "lucide-react"

export function Footer() {
  return (
    <footer className="bg-foreground text-background border-t-4 border-primary">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
          {/* Logo and description */}
          <div className="lg:col-span-2">
            <Link href="/" className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 bg-primary flex items-center justify-center border-4 border-background">
                <Sparkles className="w-6 h-6 text-primary-foreground" />
              </div>
              <span className="text-2xl font-bold">fal</span>
            </Link>
            <p className="text-background/70 max-w-sm mb-6">
              The world's best generative image, video, and audio models, all in one place.
            </p>
            <div className="flex gap-3">
              <a
                href="#"
                className="p-2 border-2 border-background hover:bg-primary hover:border-primary transition-colors"
              >
                <Twitter className="w-5 h-5" />
              </a>
              <a
                href="#"
                className="p-2 border-2 border-background hover:bg-primary hover:border-primary transition-colors"
              >
                <Github className="w-5 h-5" />
              </a>
              <a
                href="#"
                className="p-2 border-2 border-background hover:bg-primary hover:border-primary transition-colors"
              >
                <Linkedin className="w-5 h-5" />
              </a>
              <a
                href="#"
                className="p-2 border-2 border-background hover:bg-primary hover:border-primary transition-colors"
              >
                <Youtube className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Products */}
          <div>
            <h3 className="font-bold text-lg mb-4 text-primary">Products</h3>
            <ul className="space-y-3">
              <li>
                <Link href="/playground" className="text-background/70 hover:text-primary transition-colors">
                  Playground
                </Link>
              </li>
              <li>
                <Link href="#" className="text-background/70 hover:text-primary transition-colors">
                  Model APIs
                </Link>
              </li>
              <li>
                <Link href="#" className="text-background/70 hover:text-primary transition-colors">
                  Serverless
                </Link>
              </li>
              <li>
                <Link href="#" className="text-background/70 hover:text-primary transition-colors">
                  Compute
                </Link>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="font-bold text-lg mb-4 text-primary">Resources</h3>
            <ul className="space-y-3">
              <li>
                <Link href="#" className="text-background/70 hover:text-primary transition-colors">
                  Documentation
                </Link>
              </li>
              <li>
                <Link href="#" className="text-background/70 hover:text-primary transition-colors">
                  Blog
                </Link>
              </li>
              <li>
                <Link href="#" className="text-background/70 hover:text-primary transition-colors">
                  Changelog
                </Link>
              </li>
              <li>
                <Link href="#" className="text-background/70 hover:text-primary transition-colors">
                  Status
                </Link>
              </li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="font-bold text-lg mb-4 text-primary">Company</h3>
            <ul className="space-y-3">
              <li>
                <Link href="#" className="text-background/70 hover:text-primary transition-colors">
                  About
                </Link>
              </li>
              <li>
                <Link href="#" className="text-background/70 hover:text-primary transition-colors">
                  Careers
                </Link>
              </li>
              <li>
                <Link href="#" className="text-background/70 hover:text-primary transition-colors">
                  Contact
                </Link>
              </li>
              <li>
                <Link href="#" className="text-background/70 hover:text-primary transition-colors">
                  Privacy
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="mt-12 pt-8 border-t-2 border-background/20 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-background/50 text-sm">© 2025 Fal AI. All rights reserved.</p>
          <div className="flex gap-6 text-sm">
            <Link href="#" className="text-background/50 hover:text-primary transition-colors">
              Terms
            </Link>
            <Link href="#" className="text-background/50 hover:text-primary transition-colors">
              Privacy
            </Link>
            <Link href="#" className="text-background/50 hover:text-primary transition-colors">
              Cookies
            </Link>
          </div>
        </div>
      </div>
    </footer>
  )
}
