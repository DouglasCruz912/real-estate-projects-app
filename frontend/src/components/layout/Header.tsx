"use client"

import { Menu, UserCircle } from "lucide-react"
import { Button } from "@/components/ui/button"

interface HeaderProps {
  onToggleSidebar: () => void
}

export function Header({ onToggleSidebar }: HeaderProps) {
  return (
    <header className="sticky top-0 z-30 flex h-16 items-center gap-4 border-b border-border bg-white px-4 sm:px-6">
      <Button
        variant="ghost"
        size="icon"
        className="lg:hidden"
        onClick={onToggleSidebar}
      >
        <Menu className="size-5" />
      </Button>

      <div className="flex-1" />

      <div className="flex items-center gap-3">
        <div className="flex size-9 items-center justify-center rounded-full bg-zinc-100">
          <UserCircle className="size-5 text-zinc-500" />
        </div>
      </div>
    </header>
  )
}
