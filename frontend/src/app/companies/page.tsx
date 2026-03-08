"use client"

import { useState, useCallback } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import type { CompanyFilters as CompanyFiltersType } from "@/types/company"
import { useCompanies, useDeleteCompany } from "@/hooks/useCompanies"
import { CompanyTable } from "@/components/companies/CompanyTable"
import { CompanyFilters } from "@/components/companies/CompanyFilters"
import { Button } from "@/components/ui/button"
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
import { toast } from "sonner"
import { Plus, ChevronLeft, ChevronRight } from "lucide-react"

const PAGE_SIZE = 10

export default function CompaniesPage() {
  const router = useRouter()
  const [filters, setFilters] = useState<CompanyFiltersType>({
    skip: 0,
    limit: PAGE_SIZE,
  })
  const [companyToDelete, setCompanyToDelete] = useState<number | null>(null)

  const { data: companies = [], isLoading } = useCompanies(filters)
  const deleteMutation = useDeleteCompany()

  const currentPage = Math.floor((filters.skip ?? 0) / PAGE_SIZE)
  const hasNextPage = companies.length === PAGE_SIZE

  const handleFiltersChange = useCallback(
    (newFilters: CompanyFiltersType) => {
      setFilters({ ...newFilters, limit: PAGE_SIZE })
    },
    []
  )

  const handlePageChange = (page: number) => {
    setFilters((prev) => ({ ...prev, skip: page * PAGE_SIZE }))
  }

  const handleDeleteConfirm = () => {
    if (companyToDelete === null) return

    deleteMutation.mutate(companyToDelete, {
      onSuccess: () => {
        toast.success("Inmobiliaria eliminada correctamente")
        setCompanyToDelete(null)
      },
      onError: () => {
        toast.error("Error al eliminar la inmobiliaria")
        setCompanyToDelete(null)
      },
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight">Inmobiliarias</h1>
        <Button render={<Link href="/companies/new" />}>
          <Plus className="size-4" />
          Nueva Inmobiliaria
        </Button>
      </div>

      <CompanyFilters
        filters={filters}
        onFiltersChange={handleFiltersChange}
      />

      <CompanyTable
        companies={companies}
        isLoading={isLoading}
        onEdit={(id) => router.push(`/companies/${id}`)}
        onDelete={(id) => setCompanyToDelete(id)}
      />

      {!isLoading && companies.length > 0 && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            Página {currentPage + 1}
          </p>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              disabled={currentPage === 0}
              onClick={() => handlePageChange(currentPage - 1)}
            >
              <ChevronLeft className="size-4" />
              Anterior
            </Button>
            <Button
              variant="outline"
              size="sm"
              disabled={!hasNextPage}
              onClick={() => handlePageChange(currentPage + 1)}
            >
              Siguiente
              <ChevronRight className="size-4" />
            </Button>
          </div>
        </div>
      )}

      <AlertDialog
        open={companyToDelete !== null}
        onOpenChange={(open) => {
          if (!open) setCompanyToDelete(null)
        }}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>¿Eliminar inmobiliaria?</AlertDialogTitle>
            <AlertDialogDescription>
              Esta acción no se puede deshacer. La inmobiliaria y todos sus datos
              asociados serán eliminados permanentemente.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancelar</AlertDialogCancel>
            <AlertDialogAction
              variant="destructive"
              onClick={handleDeleteConfirm}
              disabled={deleteMutation.isPending}
            >
              {deleteMutation.isPending ? "Eliminando..." : "Eliminar"}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
