"use client";

import type { ProjectFilters as ProjectFiltersType } from "@/types/project";
import { useCompanies } from "@/hooks/useCompanies";
import { PROJECT_STATES, CURRENCY_TYPES } from "@/lib/constants";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { X } from "lucide-react";

interface ProjectFiltersProps {
  filters: ProjectFiltersType;
  onFiltersChange: (f: ProjectFiltersType) => void;
}

const ALL = "__all__";

export function ProjectFilters({
  filters,
  onFiltersChange,
}: ProjectFiltersProps) {
  const { data: companies } = useCompanies();

  function update(partial: Partial<ProjectFiltersType>) {
    onFiltersChange({ ...filters, ...partial, skip: 0 });
  }

  function handleClear() {
    onFiltersChange({ limit: filters.limit });
  }

  return (
    <div className="flex flex-wrap items-end gap-3">
      <div className="space-y-1">
        <Label className="text-xs">Empresa</Label>
        <Select
          value={filters.company_id ? String(filters.company_id) : ALL}
          onValueChange={(val) =>
            update({ company_id: !val || val === ALL ? undefined : Number(val) })
          }
        >
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Todas" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ALL}>Todas</SelectItem>
            {companies?.map((c) => (
              <SelectItem key={c.id} value={String(c.id)}>
                {c.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-1">
        <Label className="text-xs">Estado</Label>
        <Select
          value={filters.state ?? ALL}
          onValueChange={(val) =>
            update({ state: !val || val === ALL ? undefined : val })
          }
        >
          <SelectTrigger className="w-[160px]">
            <SelectValue placeholder="Todos" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ALL}>Todos</SelectItem>
            {PROJECT_STATES.map((s) => (
              <SelectItem key={s.value} value={s.value}>
                {s.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-1">
        <Label className="text-xs">Ubicación</Label>
        <Input
          placeholder="Ciudad, comuna..."
          className="w-[160px]"
          value={filters.location ?? ""}
          onChange={(e) => update({ location: e.target.value || undefined })}
        />
      </div>

      <div className="space-y-1">
        <Label className="text-xs">Precio mín.</Label>
        <Input
          type="number"
          placeholder="0"
          className="w-[120px]"
          value={filters.price_min ?? ""}
          onChange={(e) =>
            update({
              price_min: e.target.value ? Number(e.target.value) : undefined,
            })
          }
        />
      </div>

      <div className="space-y-1">
        <Label className="text-xs">Precio máx.</Label>
        <Input
          type="number"
          placeholder="∞"
          className="w-[120px]"
          value={filters.price_max ?? ""}
          onChange={(e) =>
            update({
              price_max: e.target.value ? Number(e.target.value) : undefined,
            })
          }
        />
      </div>

      <div className="space-y-1">
        <Label className="text-xs">Moneda</Label>
        <Select
          value={filters.currency ?? ALL}
          onValueChange={(val) =>
            update({ currency: !val || val === ALL ? undefined : val })
          }
        >
          <SelectTrigger className="w-[100px]">
            <SelectValue placeholder="Todas" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ALL}>Todas</SelectItem>
            {CURRENCY_TYPES.map((c) => (
              <SelectItem key={c.value} value={c.value}>
                {c.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="flex items-center gap-2 pb-0.5">
        <Checkbox
          checked={filters.available_only ?? false}
          onCheckedChange={(checked: boolean) =>
            update({ available_only: checked || undefined })
          }
        />
        <Label className="text-xs cursor-pointer">Solo disponibles</Label>
      </div>

      <Button variant="ghost" size="sm" onClick={handleClear}>
        <X className="size-4" />
        Limpiar
      </Button>
    </div>
  );
}
