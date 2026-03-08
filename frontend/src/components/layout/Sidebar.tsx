"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  Building,
  Building2,
  FolderKanban,
  LayoutDashboard,
  Package,
  Users,
  X,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { useAuth } from "@/contexts/AuthContext"

const navigation = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Inmobiliarias", href: "/companies", icon: Building2 },
  { name: "Proyectos", href: "/projects", icon: FolderKanban },
  { name: "Stock", href: "/stock", icon: Package },
]

const adminNavigation = [
  { name: "Usuarios", href: "/users", icon: Users },
]

interface SidebarProps {
  open: boolean
  onClose: () => void
}

export function Sidebar({ open, onClose }: SidebarProps) {
  const pathname = usePathname()
  const { isAdmin } = useAuth()

  const isActive = (href: string) => {
    if (href === "/") return pathname === "/"
    return pathname.startsWith(href)
  }

  const allNavigation = isAdmin ? [...navigation, ...adminNavigation] : navigation

  return (
    <>
      {open && (
        <div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-50 flex w-64 flex-col bg-zinc-900 transition-transform duration-300 lg:translate-x-0",
          open ? "translate-x-0" : "-translate-x-full"
        )}
      >
        <div className="flex h-16 items-center gap-2.5 border-b border-white/10 px-6">
          <Building className="size-6 text-indigo-400" />
          <span className="text-lg font-semibold text-white tracking-tight">
            Real Estate
          </span>
          <button
            onClick={onClose}
            className="ml-auto rounded-md p-1 text-zinc-400 hover:text-white lg:hidden"
          >
            <X className="size-5" />
          </button>
        </div>

        <nav className="flex-1 space-y-1 px-3 py-4">
          {allNavigation.map((item) => {
            const active = isActive(item.href)
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={onClose}
                className={cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                  active
                    ? "bg-white/10 text-white"
                    : "text-zinc-400 hover:bg-white/5 hover:text-white"
                )}
              >
                <item.icon className={cn("size-5", active && "text-indigo-400")} />
                {item.name}
              </Link>
            )
          })}
        </nav>

        <div className="border-t border-white/10 px-4 py-4">
          <p className="text-xs text-zinc-500">&copy; 2026 Real Estate App</p>
        </div>
      </aside>
    </>
  )
}
