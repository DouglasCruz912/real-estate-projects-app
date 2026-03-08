"use client"

import { useState, useEffect, useRef } from "react"
import type { CompanyFilters as CompanyFiltersType } from "@/types/company"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Search, X } from "lucide-react"

interface CompanyFiltersProps {
  filters: CompanyFiltersType
  onFiltersChange: (filters: CompanyFiltersType) => void
}

export function CompanyFilters({
  filters,
  onFiltersChange,
}: CompanyFiltersProps) {
  const [search, setSearch] = useState(filters.search ?? "")
  const filtersRef = useRef(filters)
  filtersRef.current = filters

  useEffect(() => {
    const timer = setTimeout(() => {
      const current = filtersRef.current
      const newSearch = search || undefined
      if (newSearch !== current.search) {
        onFiltersChange({ ...current, search: newSearch, skip: 0 })
      }
    }, 300)
    return () => clearTimeout(timer)
  }, [search, onFiltersChange])

  const handleClear = () => {
    setSearch("")
    onFiltersChange({})
  }

  const activeValue =
    filters.is_active === undefined ? "all" : String(filters.is_active)
  const verifiedValue =
    filters.is_verified === undefined ? "all" : String(filters.is_verified)

  return (
    <div className="flex flex-wrap items-end gap-4">
      <div className="relative w-64">
        <Search className="absolute left-2.5 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          placeholder="Buscar nombre, RUT..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="pl-8"
        />
      </div>

      <Input
        placeholder="Ciudad"
        value={filters.city ?? ""}
        onChange={(e) =>
          onFiltersChange({
            ...filters,
            city: e.target.value || undefined,
            skip: 0,
          })
        }
        className="w-40"
      />

      <Input
        placeholder="Región"
        value={filters.region ?? ""}
        onChange={(e) =>
          onFiltersChange({
            ...filters,
            region: e.target.value || undefined,
            skip: 0,
          })
        }
        className="w-40"
      />

      <Select
        value={activeValue}
        onValueChange={(val) =>
          onFiltersChange({
            ...filters,
            is_active: val === "all" ? undefined : val === "true",
            skip: 0,
          })
        }
      >
        <SelectTrigger className="w-36">
          <SelectValue placeholder="Estado" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">Todos</SelectItem>
          <SelectItem value="true">Activas</SelectItem>
          <SelectItem value="false">Inactivas</SelectItem>
        </SelectContent>
      </Select>

      <Select
        value={verifiedValue}
        onValueChange={(val) =>
          onFiltersChange({
            ...filters,
            is_verified: val === "all" ? undefined : val === "true",
            skip: 0,
          })
        }
      >
        <SelectTrigger className="w-44">
          <SelectValue placeholder="Verificación" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">Todas</SelectItem>
          <SelectItem value="true">Verificadas</SelectItem>
          <SelectItem value="false">No verificadas</SelectItem>
        </SelectContent>
      </Select>

      <Button variant="outline" onClick={handleClear}>
        <X className="size-4" />
        Limpiar
      </Button>
    </div>
  )
}
