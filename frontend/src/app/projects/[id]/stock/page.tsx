"use client";

import { useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { toast } from "sonner";
import type { StockUnit, StockFilters as StockFiltersType } from "@/types/stock";
import { useProjectStock, useDeleteStock } from "@/hooks/useStock";
import { StockTable } from "@/components/stock/StockTable";
import { StockFilters } from "@/components/stock/StockFilters";
import { StockForm } from "@/components/stock/StockForm";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { ArrowLeft, Plus, Loader2 } from "lucide-react";

const PAGE_SIZE = 15;

export default function ProjectStockPage() {
  const params = useParams();
  const projectId = Number(params.id);

  const [filters, setFilters] = useState<StockFiltersType>({
    skip: 0,
    limit: PAGE_SIZE,
  });
  const [formOpen, setFormOpen] = useState(false);
  const [editUnit, setEditUnit] = useState<StockUnit | undefined>();
  const [deleteId, setDeleteId] = useState<number | null>(null);

  const { data, isLoading } = useProjectStock(projectId, filters);
  const deleteStock = useDeleteStock();

  const stock = data?.stock ?? [];
  const total = data?.total ?? 0;
  const currentPage = Math.floor((filters.skip ?? 0) / PAGE_SIZE) + 1;
  const totalPages = data?.total_pages ?? 1;

  function handlePageChange(page: number) {
    setFilters((prev) => ({ ...prev, skip: (page - 1) * PAGE_SIZE }));
  }

  function handleNewUnit() {
    setEditUnit(undefined);
    setFormOpen(true);
  }

  function handleEdit(unit: StockUnit) {
    setEditUnit(unit);
    setFormOpen(true);
  }

  function handleFormSuccess() {
    setFormOpen(false);
    setEditUnit(undefined);
  }

  function handleFormCancel() {
    setFormOpen(false);
    setEditUnit(undefined);
  }

  function handleDelete() {
    if (!deleteId) return;
    deleteStock.mutate(deleteId, {
      onSuccess: () => {
        toast.success("Unidad eliminada exitosamente");
        setDeleteId(null);
      },
      onError: () => {
        toast.error("Error al eliminar la unidad");
      },
    });
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            size="icon"
            render={<Link href={`/projects/${projectId}`} />}
          >
            <ArrowLeft className="size-4" />
          </Button>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">
              Stock del Proyecto
            </h1>
            <p className="text-sm text-muted-foreground">
              Proyecto ID: {projectId}
            </p>
          </div>
        </div>
        <Button onClick={handleNewUnit}>
          <Plus className="size-4" />
          Nueva Unidad
        </Button>
      </div>

      <StockFilters filters={filters} onFiltersChange={setFilters} />

      <StockTable
        stock={stock}
        isLoading={isLoading}
        onEdit={handleEdit}
        onDelete={(id) => setDeleteId(id)}
      />

      {total > 0 && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            Mostrando {Math.min((filters.skip ?? 0) + 1, total)}–
            {Math.min((filters.skip ?? 0) + PAGE_SIZE, total)} de {total}{" "}
            unidades
          </p>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              disabled={currentPage <= 1}
              onClick={() => handlePageChange(currentPage - 1)}
            >
              Anterior
            </Button>
            <Button
              variant="outline"
              size="sm"
              disabled={currentPage >= totalPages}
              onClick={() => handlePageChange(currentPage + 1)}
            >
              Siguiente
            </Button>
          </div>
        </div>
      )}

      {/* Dialog para crear/editar unidad */}
      <Dialog open={formOpen} onOpenChange={setFormOpen}>
        <DialogContent className="sm:max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>
              {editUnit ? "Editar Unidad" : "Nueva Unidad"}
            </DialogTitle>
          </DialogHeader>
          <StockForm
            projectId={projectId}
            unit={editUnit}
            onSuccess={handleFormSuccess}
            onCancel={handleFormCancel}
          />
        </DialogContent>
      </Dialog>

      {/* Confirmación de eliminación */}
      <AlertDialog
        open={deleteId !== null}
        onOpenChange={(open) => {
          if (!open) setDeleteId(null);
        }}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>¿Eliminar unidad?</AlertDialogTitle>
            <AlertDialogDescription>
              Esta acción no se puede deshacer. La unidad será eliminada
              permanentemente.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancelar</AlertDialogCancel>
            <AlertDialogAction
              variant="destructive"
              disabled={deleteStock.isPending}
              onClick={handleDelete}
            >
              {deleteStock.isPending && (
                <Loader2 className="size-4 animate-spin" />
              )}
              Eliminar
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
