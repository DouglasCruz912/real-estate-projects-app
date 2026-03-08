"use client"

import { Menu, UserCircle, LogOut } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useAuth } from "@/contexts/AuthContext"

interface HeaderProps {
  onToggleSidebar: () => void
}

export function Header({ onToggleSidebar }: HeaderProps) {
  const { user, logout } = useAuth()

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
        <div className="hidden flex-col items-end sm:flex">
          <span className="text-sm font-medium text-zinc-700">
            {user?.full_name}
          </span>
          <span className="text-xs text-zinc-400 capitalize">
            {user?.role}
          </span>
        </div>
        <div className="flex size-9 items-center justify-center rounded-full bg-zinc-100">
          <UserCircle className="size-5 text-zinc-500" />
        </div>
        <Button variant="ghost" size="icon" onClick={logout} title="Cerrar sesión">
          <LogOut className="size-4 text-zinc-500" />
        </Button>
      </div>
    </header>
  )
}
