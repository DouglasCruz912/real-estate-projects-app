"use client";

import type { StockUnit } from "@/types/stock";
import { STOCK_STATUSES, UNIT_TYPES } from "@/lib/constants";
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
import { MoreHorizontal, Pencil, Trash2, Package } from "lucide-react";

const STATUS_COLORS: Record<string, string> = {
  available:
    "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400",
  reserved:
    "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400",
  sold: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400",
  blocked:
    "bg-gray-100 text-gray-800 dark:bg-gray-800/30 dark:text-gray-400",
};

function getStatusLabel(status: string) {
  return STOCK_STATUSES.find((s) => s.value === status)?.label ?? status;
}

function getUnitTypeLabel(type: string) {
  return UNIT_TYPES.find((t) => t.value === type)?.label ?? type;
}

function formatPrice(value: number | null | undefined) {
  if (value == null) return "—";
  return value.toLocaleString("es-CL");
}

interface StockTableProps {
  stock: StockUnit[];
  isLoading: boolean;
  onEdit: (unit: StockUnit) => void;
  onDelete: (id: number) => void;
}

export function StockTable({
  stock,
  isLoading,
  onEdit,
  onDelete,
}: StockTableProps) {
  if (isLoading) {
    return (
      <div className="space-y-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-10 w-full rounded-md" />
        ))}
      </div>
    );
  }

  if (stock.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-muted-foreground">
        <Package className="size-12 mb-4 opacity-40" />
        <p className="text-lg font-medium">No se encontraron unidades</p>
        <p className="text-sm mt-1">
          Ajusta los filtros o crea una nueva unidad.
        </p>
      </div>
    );
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Unidad</TableHead>
          <TableHead>Tipo</TableHead>
          <TableHead className="text-center">Dormitorios</TableHead>
          <TableHead className="text-center">Baños</TableHead>
          <TableHead className="text-right">Superficie</TableHead>
          <TableHead className="text-right">Precio</TableHead>
          <TableHead>Estado</TableHead>
          <TableHead className="w-[50px]">Acciones</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {stock.map((unit) => (
          <TableRow key={unit.id}>
            <TableCell className="font-medium">{unit.unit_number}</TableCell>
            <TableCell className="text-muted-foreground">
              {getUnitTypeLabel(unit.unit_type)}
            </TableCell>
            <TableCell className="text-center">{unit.bedrooms}</TableCell>
            <TableCell className="text-center">{unit.bathrooms}</TableCell>
            <TableCell className="text-right">
              {unit.total_area != null
                ? `${unit.total_area.toLocaleString("es-CL")} m²`
                : "—"}
            </TableCell>
            <TableCell className="text-right tabular-nums">
              {formatPrice(unit.value_list ?? unit.value_base)}
            </TableCell>
            <TableCell>
              <Badge
                className={
                  STATUS_COLORS[unit.status] ??
                  "bg-gray-100 text-gray-800 dark:bg-gray-800/30 dark:text-gray-400"
                }
              >
                {getStatusLabel(unit.status)}
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
                  <DropdownMenuItem onClick={() => onEdit(unit)}>
                    <Pencil className="size-4" />
                    Editar
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem
                    variant="destructive"
                    onClick={() => onDelete(unit.id)}
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
