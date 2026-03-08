"use client";

import type { StockFilters as StockFiltersType } from "@/types/stock";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { X } from "lucide-react";

interface StockFiltersProps {
  filters: StockFiltersType;
  onFiltersChange: (f: StockFiltersType) => void;
}

export function StockFilters({ filters, onFiltersChange }: StockFiltersProps) {
  function update(partial: Partial<StockFiltersType>) {
    onFiltersChange({ ...filters, ...partial, skip: 0 });
  }

  function handleClear() {
    onFiltersChange({ limit: filters.limit });
  }

  return (
    <div className="flex flex-wrap items-center gap-3">
      <div className="flex items-center gap-2">
        <Checkbox
          checked={filters.available_only ?? false}
          onCheckedChange={(checked: boolean) =>
            update({ available_only: checked || undefined })
          }
        />
        <Label className="text-sm cursor-pointer">Solo disponibles</Label>
      </div>

      <Button variant="ghost" size="sm" onClick={handleClear}>
        <X className="size-4" />
        Limpiar
      </Button>
    </div>
  );
}
