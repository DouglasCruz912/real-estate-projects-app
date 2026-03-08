"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { toast } from "sonner";
import type { ProjectFilters as ProjectFiltersType } from "@/types/project";
import { useProjects, useDeleteProject } from "@/hooks/useProjects";
import { ProjectTable } from "@/components/projects/ProjectTable";
import { ProjectFilters } from "@/components/projects/ProjectFilters";
import { Button } from "@/components/ui/button";
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
import { Plus, Loader2 } from "lucide-react";

const PAGE_SIZE = 10;

export default function ProjectsPage() {
  const router = useRouter();
  const [filters, setFilters] = useState<ProjectFiltersType>({
    skip: 0,
    limit: PAGE_SIZE,
  });
  const [deleteId, setDeleteId] = useState<number | null>(null);

  const { data, isLoading } = useProjects(filters);
  const deleteProject = useDeleteProject();

  const projects = data?.projects ?? [];
  const total = data?.total ?? 0;
  const currentPage = Math.floor((filters.skip ?? 0) / PAGE_SIZE) + 1;
  const totalPages = data?.total_pages ?? 1;

  function handlePageChange(page: number) {
    setFilters((prev) => ({ ...prev, skip: (page - 1) * PAGE_SIZE }));
  }

  function handleDelete() {
    if (!deleteId) return;
    deleteProject.mutate(deleteId, {
      onSuccess: () => {
        toast.success("Proyecto eliminado exitosamente");
        setDeleteId(null);
      },
      onError: () => {
        toast.error("Error al eliminar el proyecto");
      },
    });
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight">Proyectos</h1>
        <Button render={<Link href="/projects/new" />}>
          <Plus className="size-4" />
          Nuevo Proyecto
        </Button>
      </div>

      <ProjectFilters filters={filters} onFiltersChange={setFilters} />

      <ProjectTable
        projects={projects}
        isLoading={isLoading}
        onEdit={(id) => router.push(`/projects/${id}`)}
        onDelete={(id) => setDeleteId(id)}
      />

      {/* Paginación */}
      {total > 0 && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            Mostrando{" "}
            {Math.min((filters.skip ?? 0) + 1, total)}–
            {Math.min((filters.skip ?? 0) + PAGE_SIZE, total)} de {total}{" "}
            proyectos
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

      {/* Diálogo de confirmación de eliminación */}
      <AlertDialog
        open={deleteId !== null}
        onOpenChange={(open) => {
          if (!open) setDeleteId(null);
        }}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>¿Eliminar proyecto?</AlertDialogTitle>
            <AlertDialogDescription>
              Esta acción no se puede deshacer. El proyecto y toda su
              información asociada serán eliminados permanentemente.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancelar</AlertDialogCancel>
            <AlertDialogAction
              variant="destructive"
              disabled={deleteProject.isPending}
              onClick={handleDelete}
            >
              {deleteProject.isPending && (
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
