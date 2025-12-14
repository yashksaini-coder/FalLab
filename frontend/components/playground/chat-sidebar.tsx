"use client"

import { useState } from "react"
import { Plus, MessageSquare, Trash2, ChevronLeft, ChevronRight, Settings } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface Chat {
  id: string
  title: string
  timestamp: Date
}

interface ChatSidebarProps {
  chats: Chat[]
  activeChat: string | null
  onSelectChat: (id: string) => void
  onNewChat: () => void
  onDeleteChat: (id: string) => void
}

export function ChatSidebar({ chats, activeChat, onSelectChat, onNewChat, onDeleteChat }: ChatSidebarProps) {
  const [isCollapsed, setIsCollapsed] = useState(false)

  return (
    <div
      className={cn(
        "relative flex flex-col h-full bg-muted/50 border-r-4 border-foreground transition-all duration-300",
        isCollapsed ? "w-16" : "w-72",
      )}
    >
      {/* Toggle button */}
      <button
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="absolute -right-4 top-6 w-8 h-8 bg-primary neo-border flex items-center justify-center z-10 hover:bg-primary/90"
      >
        {isCollapsed ? (
          <ChevronRight className="w-4 h-4 text-primary-foreground" />
        ) : (
          <ChevronLeft className="w-4 h-4 text-primary-foreground" />
        )}
      </button>

      {/* New chat button */}
      <div className="p-4 border-b-4 border-foreground">
        <Button
          onClick={onNewChat}
          className={cn(
            "w-full bg-primary text-primary-foreground neo-border neo-shadow-sm hover:translate-x-1 hover:translate-y-1 hover:shadow-none transition-all font-bold",
            isCollapsed && "p-2",
          )}
        >
          <Plus className="w-5 h-5" />
          {!isCollapsed && <span className="ml-2">New Chat</span>}
        </Button>
      </div>

      {/* Chat list */}
      <div className="flex-1 overflow-y-auto p-2">
        {chats.map((chat) => (
          <div
            key={chat.id}
            className={cn(
              "group flex items-center gap-3 p-3 mb-2 cursor-pointer transition-all neo-border",
              activeChat === chat.id ? "bg-primary/20 border-primary" : "bg-card hover:bg-muted",
            )}
            onClick={() => onSelectChat(chat.id)}
          >
            <MessageSquare className="w-5 h-5 flex-shrink-0" />
            {!isCollapsed && (
              <>
                <span className="flex-1 truncate text-sm font-medium">{chat.title}</span>
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    onDeleteChat(chat.id)
                  }}
                  className="opacity-0 group-hover:opacity-100 p-1 hover:bg-destructive/20 transition-all"
                >
                  <Trash2 className="w-4 h-4 text-destructive" />
                </button>
              </>
            )}
          </div>
        ))}
      </div>

      {/* Settings button */}
      <div className="p-4 border-t-4 border-foreground">
        <Button variant="outline" className={cn("w-full neo-border font-bold", isCollapsed && "p-2")}>
          <Settings className="w-5 h-5" />
          {!isCollapsed && <span className="ml-2">Settings</span>}
        </Button>
      </div>
    </div>
  )
}
