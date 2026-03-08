"use client"

import type { Company } from "@/types/company"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Skeleton } from "@/components/ui/skeleton"
import { MoreHorizontal, Pencil, Trash2 } from "lucide-react"

interface CompanyTableProps {
  companies: Company[]
  isLoading: boolean
  onEdit: (id: number) => void
  onDelete: (id: number) => void
}

function SkeletonRows() {
  return Array.from({ length: 5 }).map((_, i) => (
    <TableRow key={i}>
      <TableCell><Skeleton className="h-4 w-32" /></TableCell>
      <TableCell><Skeleton className="h-4 w-20" /></TableCell>
      <TableCell><Skeleton className="h-4 w-24" /></TableCell>
      <TableCell><Skeleton className="h-4 w-24" /></TableCell>
      <TableCell><Skeleton className="h-5 w-16" /></TableCell>
      <TableCell><Skeleton className="h-5 w-20" /></TableCell>
      <TableCell><Skeleton className="h-8 w-8" /></TableCell>
    </TableRow>
  ))
}

export function CompanyTable({
  companies,
  isLoading,
  onEdit,
  onDelete,
}: CompanyTableProps) {
  if (!isLoading && companies.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center rounded-lg border border-dashed py-12 text-muted-foreground">
        <p className="text-lg font-medium">No se encontraron inmobiliarias</p>
        <p className="text-sm">Intenta cambiar los filtros o crea una nueva.</p>
      </div>
    )
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Nombre</TableHead>
          <TableHead>RUT</TableHead>
          <TableHead>Ciudad</TableHead>
          <TableHead>Región</TableHead>
          <TableHead>Estado</TableHead>
          <TableHead>Verificada</TableHead>
          <TableHead className="w-[70px]">Acciones</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {isLoading ? (
          <SkeletonRows />
        ) : (
          companies.map((company) => (
            <TableRow key={company.id}>
              <TableCell className="font-medium">{company.name}</TableCell>
              <TableCell>{company.rut ?? "—"}</TableCell>
              <TableCell>{company.city ?? "—"}</TableCell>
              <TableCell>{company.region ?? "—"}</TableCell>
              <TableCell>
                {company.is_active ? (
                  <Badge
                    variant="outline"
                    className="border-green-200 bg-green-50 text-green-700 dark:border-green-800 dark:bg-green-950 dark:text-green-400"
                  >
                    Activa
                  </Badge>
                ) : (
                  <Badge variant="secondary">Inactiva</Badge>
                )}
              </TableCell>
              <TableCell>
                {company.is_verified ? (
                  <Badge
                    variant="outline"
                    className="border-blue-200 bg-blue-50 text-blue-700 dark:border-blue-800 dark:bg-blue-950 dark:text-blue-400"
                  >
                    Verificada
                  </Badge>
                ) : (
                  <span className="text-muted-foreground">—</span>
                )}
              </TableCell>
              <TableCell>
                <DropdownMenu>
                  <DropdownMenuTrigger
                    render={<Button variant="ghost" size="icon" />}
                  >
                    <MoreHorizontal className="size-4" />
                    <span className="sr-only">Acciones</span>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem onClick={() => onEdit(company.id)}>
                      <Pencil />
                      Editar
                    </DropdownMenuItem>
                    <DropdownMenuItem
                      variant="destructive"
                      onClick={() => onDelete(company.id)}
                    >
                      <Trash2 />
                      Eliminar
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>
          ))
        )}
      </TableBody>
    </Table>
  )
}
