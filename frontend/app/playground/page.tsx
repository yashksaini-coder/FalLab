"use client"

import { useState, useCallback } from "react"
import { ChatSidebar } from "@/components/playground/chat-sidebar"
import { PlaygroundHeader } from "@/components/playground/playground-header"
import { MessageList, type Message } from "@/components/playground/message-list"
import { PromptInput } from "@/components/playground/prompt-input"
import { submitGeneration, pollGenerationUntilComplete } from "@/lib/api"

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
      if (!activeChat || !selectedModel) return

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

      try {
        // Call the backend API to generate
        const { request_id, status } = await submitGeneration({
          model_id: selectedModel,
          prompt,
          parameters: {},
        })

        // Add a loading message while waiting for generation
        const loadingMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: "Generating your image...",
          timestamp: new Date(),
          model: selectedModel,
          requestId: request_id,
          status: status || "submitted",
        }

        setChats((prev) =>
          prev.map((chat) =>
            chat.id === activeChat ? { ...chat, messages: [...chat.messages, loadingMessage] } : chat,
          ),
        )

        // Poll for completion
        const result = await pollGenerationUntilComplete(request_id)

        // Replace loading message with result
        setChats((prev) =>
          prev.map((chat) => {
            if (chat.id === activeChat) {
              return {
                ...chat,
                messages: chat.messages.map((msg) =>
                  msg.id === loadingMessage.id
                    ? {
                        ...msg,
                        content: "Image generated successfully!",
                        image:
                          result.result?.images?.[0]?.url ||
                          result.result?.output?.[0] ||
                          undefined,
                        status: result.status,
                        requestId: result.request_id,
                      }
                    : msg,
                ),
              }
            }
            return chat
          }),
        )
      } catch (error) {
        console.error("Generation failed:", error)

        // Add error message
        const errorMessage: Message = {
          id: (Date.now() + 2).toString(),
          role: "assistant",
          content: `Error: ${error instanceof Error ? error.message : "Generation failed. Please try again."}`,
          timestamp: new Date(),
          model: selectedModel,
        }

        setChats((prev) =>
          prev.map((chat) =>
            chat.id === activeChat ? { ...chat, messages: [...chat.messages, errorMessage] } : chat,
          ),
        )
      } finally {
        setIsLoading(false)
      }
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
