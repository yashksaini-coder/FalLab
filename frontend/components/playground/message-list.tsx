"use client"

import { User, Bot, Download, Copy, Check, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { useState } from "react"

export interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  image?: string
  timestamp: Date
  model?: string
}

interface MessageListProps {
  messages: Message[]
  isLoading: boolean
}

export function MessageList({ messages, isLoading }: MessageListProps) {
  const [copiedId, setCopiedId] = useState<string | null>(null)

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center max-w-md">
          <div className="w-24 h-24 mx-auto mb-6 neo-border bg-primary/10 flex items-center justify-center">
            <Bot className="w-12 h-12 text-primary" />
          </div>
          <h3 className="text-2xl font-bold mb-3">Start Creating</h3>
          <p className="text-muted-foreground">
            Describe what you want to generate. Be specific about style, colors, mood, and composition for best results.
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-2">
            {["Cyberpunk city", "Portrait photo", "Abstract art", "Product shot"].map((suggestion) => (
              <span
                key={suggestion}
                className="px-3 py-1 neo-border bg-muted text-sm font-medium cursor-pointer hover:bg-primary/20"
              >
                {suggestion}
              </span>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-6">
      {messages.map((message) => (
        <div key={message.id} className={cn("flex gap-4", message.role === "user" ? "flex-row-reverse" : "flex-row")}>
          {/* Avatar */}
          <div
            className={cn(
              "w-10 h-10 neo-border flex-shrink-0 flex items-center justify-center",
              message.role === "user" ? "bg-secondary" : "bg-primary",
            )}
          >
            {message.role === "user" ? (
              <User className="w-5 h-5 text-secondary-foreground" />
            ) : (
              <Bot className="w-5 h-5 text-primary-foreground" />
            )}
          </div>

          {/* Message content */}
          <div className={cn("flex-1 max-w-2xl", message.role === "user" ? "text-right" : "text-left")}>
            <div className={cn("inline-block neo-border p-4", message.role === "user" ? "bg-secondary/20" : "bg-card")}>
              {message.content && <p className="text-sm mb-3 whitespace-pre-wrap">{message.content}</p>}

              {message.image && (
                <div className="relative group">
                  <img src={message.image || "/placeholder.svg"} alt="Generated" className="neo-border max-w-full" />
                  <div className="absolute top-2 right-2 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <Button size="icon" variant="secondary" className="neo-border h-8 w-8">
                      <Download className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              )}

              {message.model && <p className="text-xs text-muted-foreground mt-2">Generated with {message.model}</p>}
            </div>

            {/* Message actions */}
            <div className={cn("flex gap-2 mt-2", message.role === "user" ? "justify-end" : "justify-start")}>
              <button
                onClick={() => copyToClipboard(message.content, message.id)}
                className="p-1 hover:bg-muted rounded transition-colors"
              >
                {copiedId === message.id ? (
                  <Check className="w-4 h-4 text-green-500" />
                ) : (
                  <Copy className="w-4 h-4 text-muted-foreground" />
                )}
              </button>
              {message.role === "assistant" && (
                <button className="p-1 hover:bg-muted rounded transition-colors">
                  <RefreshCw className="w-4 h-4 text-muted-foreground" />
                </button>
              )}
            </div>
          </div>
        </div>
      ))}

      {/* Loading indicator */}
      {isLoading && (
        <div className="flex gap-4">
          <div className="w-10 h-10 neo-border bg-primary flex-shrink-0 flex items-center justify-center">
            <Bot className="w-5 h-5 text-primary-foreground" />
          </div>
          <div className="neo-border bg-card p-4">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-primary animate-bounce" style={{ animationDelay: "0ms" }} />
              <div className="w-2 h-2 bg-primary animate-bounce" style={{ animationDelay: "150ms" }} />
              <div className="w-2 h-2 bg-primary animate-bounce" style={{ animationDelay: "300ms" }} />
              <span className="text-sm text-muted-foreground ml-2">Generating...</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
