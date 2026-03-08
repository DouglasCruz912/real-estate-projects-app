"use client";

import { useRouter } from "next/navigation";
import type { Project } from "@/types/project";
import { PROJECT_STATES } from "@/lib/constants";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  MoreHorizontal,
  Eye,
  Pencil,
  Package,
  FolderOpen,
  Trash2,
} from "lucide-react";

const STATE_COLORS: Record<string, string> = {
  planning:
    "bg-gray-100 text-gray-800 dark:bg-gray-800/30 dark:text-gray-400",
  development:
    "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400",
  pre_sale:
    "bg-cyan-100 text-cyan-800 dark:bg-cyan-900/30 dark:text-cyan-400",
  construction:
    "bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400",
  sale: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400",
  delivered:
    "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400",
  completed:
    "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400",
  cancelled:
    "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400",
};

function getStateLabel(state: string) {
  return PROJECT_STATES.find((s) => s.value === state)?.label ?? state;
}

function formatPrice(value: number | null | undefined) {
  if (value == null) return null;
  return value.toLocaleString("es-CL");
}

function renderPriceRange(from: number | null | undefined, to: number | null | undefined) {
  const f = formatPrice(from);
  const t = formatPrice(to);
  if (f && t) return `${f} – ${t}`;
  if (f) return `Desde ${f}`;
  if (t) return `Hasta ${t}`;
  return "—";
}

interface ProjectTableProps {
  projects: Project[];
  isLoading: boolean;
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
}

export function ProjectTable({
  projects,
  isLoading,
  onEdit,
  onDelete,
}: ProjectTableProps) {
  const router = useRouter();

  if (isLoading) {
    return (
      <div className="space-y-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-12 w-full rounded-md" />
        ))}
      </div>
    );
  }

  if (projects.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-muted-foreground">
        <Package className="size-12 mb-4 opacity-40" />
        <p className="text-lg font-medium">No se encontraron proyectos</p>
        <p className="text-sm mt-1">
          Ajusta los filtros o crea un nuevo proyecto.
        </p>
      </div>
    );
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Nombre</TableHead>
          <TableHead>Empresa</TableHead>
          <TableHead>Ciudad</TableHead>
          <TableHead>Estado</TableHead>
          <TableHead>Precio</TableHead>
          <TableHead>Unidades</TableHead>
          <TableHead>Activo</TableHead>
          <TableHead className="w-[50px]">Acciones</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {projects.map((project) => (
          <TableRow key={project.id}>
            <TableCell className="font-medium">{project.name}</TableCell>
            <TableCell className="text-muted-foreground">
              ID {project.company_id}
            </TableCell>
            <TableCell>{project.city ?? "—"}</TableCell>
            <TableCell>
              <Badge
                className={
                  STATE_COLORS[project.state] ??
                  "bg-gray-100 text-gray-800 dark:bg-gray-800/30 dark:text-gray-400"
                }
              >
                {getStateLabel(project.state)}
              </Badge>
            </TableCell>
            <TableCell>{renderPriceRange(project.price_from, project.price_to)}</TableCell>
            <TableCell>
              {project.available_units != null && project.total_units != null
                ? `${project.available_units}/${project.total_units}`
                : "—"}
            </TableCell>
            <TableCell>
              <Badge
                className={
                  project.is_active
                    ? "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400"
                    : "bg-gray-100 text-gray-800 dark:bg-gray-800/30 dark:text-gray-400"
                }
              >
                {project.is_active ? "Sí" : "No"}
              </Badge>
            </TableCell>
            <TableCell>
              <DropdownMenu>
                <DropdownMenuTrigger
                  render={<Button variant="ghost" size="icon" />}
                >
                  <MoreHorizontal className="size-4" />
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem
                    onClick={() => router.push(`/projects/${project.id}`)}
                  >
                    <Eye className="size-4" />
                    Ver Detalle
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => onEdit(project.id)}>
                    <Pencil className="size-4" />
                    Editar
                  </DropdownMenuItem>
                  <DropdownMenuItem
                    onClick={() =>
                      router.push(`/projects/${project.id}/stock`)
                    }
                  >
                    <Package className="size-4" />
                    Stock
                  </DropdownMenuItem>
                  <DropdownMenuItem
                    onClick={() =>
                      router.push(`/projects/${project.id}/files`)
                    }
                  >
                    <FolderOpen className="size-4" />
                    Archivos
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem
                    variant="destructive"
                    onClick={() => onDelete(project.id)}
                  >
                    <Trash2 className="size-4" />
                    Eliminar
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
