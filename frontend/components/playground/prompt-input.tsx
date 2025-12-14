"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Send, Paperclip, Sparkles, X, ImageIcon } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface PromptInputProps {
  onSubmit: (prompt: string, attachments: File[]) => void
  isLoading: boolean
}

export function PromptInput({ onSubmit, isLoading }: PromptInputProps) {
  const [prompt, setPrompt] = useState("")
  const [attachments, setAttachments] = useState<File[]>([])
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`
    }
  }, [prompt])

  const handleSubmit = () => {
    if (prompt.trim() || attachments.length > 0) {
      onSubmit(prompt, attachments)
      setPrompt("")
      setAttachments([])
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setAttachments([...attachments, ...Array.from(e.target.files)])
    }
  }

  const removeAttachment = (index: number) => {
    setAttachments(attachments.filter((_, i) => i !== index))
  }

  return (
    <div className="p-4 border-t-4 border-foreground bg-background">
      {/* Attachments preview */}
      {attachments.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-3">
          {attachments.map((file, index) => (
            <div key={index} className="flex items-center gap-2 px-3 py-1 neo-border bg-muted text-sm">
              <ImageIcon className="w-4 h-4" />
              <span className="max-w-32 truncate">{file.name}</span>
              <button onClick={() => removeAttachment(index)}>
                <X className="w-4 h-4 hover:text-destructive" />
              </button>
            </div>
          ))}
        </div>
      )}

      <div className="flex items-end gap-3">
        {/* Attachment button */}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          multiple
          className="hidden"
          onChange={handleFileChange}
        />
        <Button
          variant="outline"
          size="icon"
          onClick={() => fileInputRef.current?.click()}
          className="neo-border h-12 w-12 flex-shrink-0"
        >
          <Paperclip className="w-5 h-5" />
        </Button>

        {/* Text input */}
        <div className="flex-1 neo-border bg-card relative">
          <textarea
            ref={textareaRef}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe the image or video you want to generate..."
            className="w-full p-4 pr-12 bg-transparent resize-none outline-none min-h-[48px] max-h-[200px] font-sans"
            rows={1}
          />
          <div className="absolute right-3 bottom-3">
            <Sparkles className="w-5 h-5 text-muted-foreground" />
          </div>
        </div>

        {/* Submit button */}
        <Button
          onClick={handleSubmit}
          disabled={isLoading || (!prompt.trim() && attachments.length === 0)}
          className={cn(
            "h-12 w-12 flex-shrink-0 neo-border transition-all",
            isLoading
              ? "bg-muted"
              : "bg-primary text-primary-foreground neo-shadow-sm hover:translate-x-1 hover:translate-y-1 hover:shadow-none",
          )}
        >
          <Send className="w-5 h-5" />
        </Button>
      </div>

      <p className="text-xs text-muted-foreground mt-3 text-center">Press Enter to send, Shift+Enter for new line</p>
    </div>
  )
}
