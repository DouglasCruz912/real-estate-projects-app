"use client"

import { useState, useEffect } from "react"
import { Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import type { UserData, UserCreateData, UserUpdateData } from "@/services/userService"

interface UserFormProps {
  user?: UserData | null
  loading?: boolean
  onSubmit: (data: UserCreateData | UserUpdateData) => void
  onCancel: () => void
}

export function UserForm({ user, loading, onSubmit, onCancel }: UserFormProps) {
  const isEdit = !!user
  const [fullName, setFullName] = useState("")
  const [email, setEmail] = useState("")
  const [phone, setPhone] = useState("")
  const [role, setRole] = useState("user")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")

  useEffect(() => {
    if (user) {
      setFullName(user.full_name)
      setEmail(user.email)
      setPhone(user.phone || "")
      setRole(user.role)
    }
  }, [user])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    if (!fullName.trim()) { setError("Nombre requerido"); return }
    if (!email.trim()) { setError("Email requerido"); return }
    if (!isEdit && password.length < 8) { setError("Contraseña mínimo 8 caracteres"); return }

    if (isEdit) {
      const data: UserUpdateData = { full_name: fullName.trim(), email: email.trim(), role }
      if (phone.trim()) data.phone = phone.trim()
      if (password) data.password = password
      onSubmit(data)
    } else {
      const data: UserCreateData = {
        full_name: fullName.trim(),
        email: email.trim(),
        password,
        role,
      }
      if (phone.trim()) data.phone = phone.trim()
      onSubmit(data)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="fullName">Nombre completo</Label>
        <Input id="fullName" value={fullName} onChange={(e) => setFullName(e.target.value)} disabled={loading} />
      </div>

      <div className="space-y-2">
        <Label htmlFor="formEmail">Correo electrónico</Label>
        <Input id="formEmail" type="email" value={email} onChange={(e) => setEmail(e.target.value)} disabled={loading} />
      </div>

      <div className="space-y-2">
        <Label htmlFor="formPhone">Teléfono</Label>
        <Input id="formPhone" value={phone} onChange={(e) => setPhone(e.target.value)} disabled={loading} />
      </div>

      <div className="space-y-2">
        <Label>Rol</Label>
        <Select value={role} onValueChange={setRole} disabled={loading}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="admin">Admin</SelectItem>
            <SelectItem value="editor">Editor</SelectItem>
            <SelectItem value="user">Usuario</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="formPassword">{isEdit ? "Nueva contraseña (opcional)" : "Contraseña"}</Label>
        <Input
          id="formPassword"
          type="password"
          value={password}
          placeholder={isEdit ? "Dejar vacío para no cambiar" : "Mínimo 8 caracteres"}
          onChange={(e) => setPassword(e.target.value)}
          disabled={loading}
        />
      </div>

      {error && <p className="text-sm text-red-500">{error}</p>}

      <div className="flex justify-end gap-2 pt-2">
        <Button type="button" variant="outline" onClick={onCancel} disabled={loading}>
          Cancelar
        </Button>
        <Button type="submit" disabled={loading}>
          {loading && <Loader2 className="mr-2 size-4 animate-spin" />}
          {isEdit ? "Guardar cambios" : "Crear usuario"}
        </Button>
      </div>
    </form>
  )
}
