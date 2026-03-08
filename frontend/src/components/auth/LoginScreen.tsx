"use client"

import { useState } from "react"
import { Building2, LogIn, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useAuth } from "@/contexts/AuthContext"

export function LoginScreen() {
  const { login } = useAuth()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const trimmedEmail = email.trim().toLowerCase()

    if (!trimmedEmail) {
      setError("Ingresa tu correo electrónico")
      return
    }
    if (!password) {
      setError("Ingresa tu contraseña")
      return
    }

    setError("")
    setLoading(true)

    try {
      await login(trimmedEmail, password)
    } catch (err: any) {
      const detail = err?.response?.data?.detail
      setError(detail || "Error al iniciar sesión")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 px-4">
      <div className="w-full max-w-sm space-y-8">
        <div className="flex flex-col items-center gap-3">
          <div className="flex size-14 items-center justify-center rounded-2xl bg-zinc-900">
            <Building2 className="size-7 text-white" />
          </div>
          <div className="text-center">
            <h1 className="text-2xl font-semibold tracking-tight text-zinc-900">
              Real Estate Projects
            </h1>
            <p className="mt-1 text-sm text-zinc-500">
              Ingresa tus credenciales para acceder
            </p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Correo electrónico</Label>
            <Input
              id="email"
              type="email"
              placeholder="usuario@empresa.com"
              value={email}
              onChange={(e) => { setEmail(e.target.value); if (error) setError("") }}
              autoFocus
              autoComplete="email"
              disabled={loading}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Contraseña</Label>
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => { setPassword(e.target.value); if (error) setError("") }}
              autoComplete="current-password"
              disabled={loading}
            />
          </div>

          {error && <p className="text-sm text-red-500">{error}</p>}

          <Button type="submit" className="w-full" size="lg" disabled={loading}>
            {loading ? (
              <Loader2 className="mr-2 size-4 animate-spin" />
            ) : (
              <LogIn className="mr-2 size-4" />
            )}
            {loading ? "Ingresando..." : "Ingresar"}
          </Button>
        </form>

        <p className="text-center text-xs text-zinc-400">
          Contacta al administrador si no tienes credenciales
        </p>
      </div>
    </div>
  )
}
