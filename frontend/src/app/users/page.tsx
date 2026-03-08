"use client"

import { useState } from "react"
import { Plus, Users, Loader2 } from "lucide-react"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import { UserTable } from "@/components/users/UserTable"
import { UserForm } from "@/components/users/UserForm"
import { useUsers, useCreateUser, useUpdateUser, useDeleteUser } from "@/hooks/useUsers"
import { useAuth } from "@/contexts/AuthContext"
import type { UserData, UserCreateData, UserUpdateData } from "@/services/userService"

export default function UsersPage() {
  const { isAdmin } = useAuth()
  const { data: users, isLoading } = useUsers()
  const createUser = useCreateUser()
  const updateUser = useUpdateUser()
  const deleteUser = useDeleteUser()

  const [formOpen, setFormOpen] = useState(false)
  const [editingUser, setEditingUser] = useState<UserData | null>(null)
  const [deletingUser, setDeletingUser] = useState<UserData | null>(null)

  if (!isAdmin) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-zinc-400">
        <Users className="size-12 mb-4" />
        <p className="text-lg font-medium">Acceso restringido</p>
        <p className="text-sm">Solo los administradores pueden gestionar usuarios</p>
      </div>
    )
  }

  const handleCreate = () => {
    setEditingUser(null)
    setFormOpen(true)
  }

  const handleEdit = (user: UserData) => {
    setEditingUser(user)
    setFormOpen(true)
  }

  const handleSubmit = async (data: UserCreateData | UserUpdateData) => {
    try {
      if (editingUser) {
        await updateUser.mutateAsync({ id: editingUser.id, data: data as UserUpdateData })
        toast.success("Usuario actualizado")
      } else {
        await createUser.mutateAsync(data as UserCreateData)
        toast.success("Usuario creado")
      }
      setFormOpen(false)
      setEditingUser(null)
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || "Error al guardar usuario")
    }
  }

  const handleDelete = async () => {
    if (!deletingUser) return
    try {
      await deleteUser.mutateAsync(deletingUser.id)
      toast.success("Usuario desactivado")
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || "Error al desactivar usuario")
    }
    setDeletingUser(null)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Usuarios</h1>
          <p className="text-sm text-zinc-500">Gestiona los usuarios del sistema</p>
        </div>
        <Button onClick={handleCreate}>
          <Plus className="mr-2 size-4" />
          Nuevo usuario
        </Button>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-12">
          <Loader2 className="size-8 animate-spin text-zinc-400" />
        </div>
      ) : (
        <UserTable
          users={users || []}
          onEdit={handleEdit}
          onDelete={(user) => setDeletingUser(user)}
        />
      )}

      <Dialog open={formOpen} onOpenChange={setFormOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>{editingUser ? "Editar usuario" : "Nuevo usuario"}</DialogTitle>
          </DialogHeader>
          <UserForm
            user={editingUser}
            loading={createUser.isPending || updateUser.isPending}
            onSubmit={handleSubmit}
            onCancel={() => { setFormOpen(false); setEditingUser(null) }}
          />
        </DialogContent>
      </Dialog>

      <AlertDialog open={!!deletingUser} onOpenChange={(open) => !open && setDeletingUser(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Desactivar usuario</AlertDialogTitle>
            <AlertDialogDescription>
              ¿Estás seguro de desactivar a <strong>{deletingUser?.full_name}</strong>?
              El usuario no podrá iniciar sesión.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancelar</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete}>Desactivar</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
