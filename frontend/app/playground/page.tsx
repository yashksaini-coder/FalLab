"use client"

import { useState, useCallback } from "react"
import { ChatSidebar } from "@/components/playground/chat-sidebar"
import { PlaygroundHeader } from "@/components/playground/playground-header"
import { MessageList, type Message } from "@/components/playground/message-list"
import { PromptInput } from "@/components/playground/prompt-input"

interface Chat {
  id: string
  title: string
  timestamp: Date
  messages: Message[]
}

export default function PlaygroundPage() {
  const [chats, setChats] = useState<Chat[]>([
    {
      id: "1",
      title: "Cyberpunk cityscape",
      timestamp: new Date(),
      messages: [],
    },
  ])
  const [activeChat, setActiveChat] = useState<string | null>("1")
  const [selectedModel, setSelectedModel] = useState("flux-kontext")
  const [isLoading, setIsLoading] = useState(false)

  const activeMessages = chats.find((c) => c.id === activeChat)?.messages || []

  const handleNewChat = useCallback(() => {
    const newChat: Chat = {
      id: Date.now().toString(),
      title: "New Chat",
      timestamp: new Date(),
      messages: [],
    }
    setChats([newChat, ...chats])
    setActiveChat(newChat.id)
  }, [chats])

  const handleDeleteChat = useCallback(
    (id: string) => {
      setChats(chats.filter((c) => c.id !== id))
      if (activeChat === id) {
        setActiveChat(chats[0]?.id || null)
      }
    },
    [chats, activeChat],
  )

  const handleSubmit = useCallback(
    async (prompt: string, attachments: File[]) => {
      if (!activeChat) return

      const userMessage: Message = {
        id: Date.now().toString(),
        role: "user",
        content: prompt,
        timestamp: new Date(),
      }

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === activeChat
            ? {
                ...chat,
                title: chat.messages.length === 0 ? prompt.slice(0, 30) + "..." : chat.title,
                messages: [...chat.messages, userMessage],
              }
            : chat,
        ),
      )

      setIsLoading(true)

      // Simulate AI response
      await new Promise((resolve) => setTimeout(resolve, 2000))

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: `Here's your generated image based on: "${prompt}"`,
        image: `/placeholder.svg?height=512&width=512&query=${encodeURIComponent(prompt)}`,
        timestamp: new Date(),
        model: selectedModel,
      }

      setChats((prev) =>
        prev.map((chat) => (chat.id === activeChat ? { ...chat, messages: [...chat.messages, aiMessage] } : chat)),
      )

      setIsLoading(false)
    },
    [activeChat, selectedModel],
  )

  return (
    <div className="h-screen flex overflow-hidden bg-background">
      {/* Sidebar - hidden on mobile */}
      <div className="hidden md:block">
        <ChatSidebar
          chats={chats}
          activeChat={activeChat}
          onSelectChat={setActiveChat}
          onNewChat={handleNewChat}
          onDeleteChat={handleDeleteChat}
        />
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0">
        <PlaygroundHeader selectedModel={selectedModel} onSelectModel={setSelectedModel} />

        <MessageList messages={activeMessages} isLoading={isLoading} />

        <PromptInput onSubmit={handleSubmit} isLoading={isLoading} />
      </div>
    </div>
  )
}
