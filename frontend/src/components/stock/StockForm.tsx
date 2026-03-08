"use client";

import { useEffect } from "react";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { toast } from "sonner";
import type { StockUnit } from "@/types/stock";
import { useCreateStock, useUpdateStock } from "@/hooks/useStock";
import {
  STOCK_STATUSES,
  UNIT_TYPES,
  ORIENTATION_TYPES,
  CURRENCY_TYPES,
} from "@/lib/constants";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";
import { Separator } from "@/components/ui/separator";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Loader2 } from "lucide-react";

const numField = z
  .union([z.string(), z.number()])
  .optional()
  .transform((v) => {
    if (v === undefined || v === null || v === "") return undefined;
    const n = typeof v === "string" ? parseFloat(v) : v;
    return isNaN(n) ? undefined : n;
  });

const intField = z
  .union([z.string(), z.number()])
  .optional()
  .transform((v) => {
    if (v === undefined || v === null || v === "") return undefined;
    const n = typeof v === "string" ? parseInt(v, 10) : v;
    return isNaN(n) ? undefined : n;
  });

const NONE = "__none__";

const stockSchema = z.object({
  unit_number: z.string().min(1, "La unidad es requerida"),
  unit_type: z.string().min(1, "El tipo es requerido"),
  description: z.string().optional(),
  floor: intField,
  building: z.string().optional(),
  bedrooms: intField.default(0),
  bathrooms: intField.default(0),
  orientation: z.string().optional(),
  has_parking: z.boolean(),
  has_storage: z.boolean(),
  parkings: z.string().optional(),
  storages: z.string().optional(),
  total_area: numField,
  surface_internal: numField,
  surface_terrace: numField,
  surface_garden: numField,
  surface_pantry: numField,
  surface_multiuse_assignable: numField,
  surface_util: numField,
  surface_terrain: numField,
  surface_others: numField,
  currency: z.string(),
  value_base: numField,
  value_uf: numField,
  value_list: numField,
  value_discount: numField,
  value_enabled: numField,
  value_promotion: numField,
  value_bonus: numField,
  value_parking: numField,
  value_storage: numField,
  status: z.string(),
});

type FormValues = z.input<typeof stockSchema>;

function getDefaults(unit?: StockUnit): FormValues {
  if (unit) {
    return {
      unit_number: unit.unit_number,
      unit_type: unit.unit_type,
      description: unit.description ?? "",
      floor: unit.floor ?? "",
      building: unit.building ?? "",
      bedrooms: unit.bedrooms ?? 0,
      bathrooms: unit.bathrooms ?? 0,
      orientation: unit.orientation ?? "",
      has_parking: unit.has_parking,
      has_storage: unit.has_storage,
      parkings: unit.parkings ?? "",
      storages: unit.storages ?? "",
      total_area: unit.total_area ?? "",
      surface_internal: unit.surface_internal ?? "",
      surface_terrace: unit.surface_terrace ?? "",
      surface_garden: unit.surface_garden ?? "",
      surface_pantry: unit.surface_pantry ?? "",
      surface_multiuse_assignable: unit.surface_multiuse_assignable ?? "",
      surface_util: unit.surface_util ?? "",
      surface_terrain: unit.surface_terrain ?? "",
      surface_others: unit.surface_others ?? "",
      currency: unit.currency,
      value_base: unit.value_base ?? "",
      value_uf: unit.value_uf ?? "",
      value_list: unit.value_list ?? "",
      value_discount: unit.value_discount ?? "",
      value_enabled: unit.value_enabled ?? "",
      value_promotion: unit.value_promotion ?? "",
      value_bonus: unit.value_bonus ?? "",
      value_parking: unit.value_parking ?? "",
      value_storage: unit.value_storage ?? "",
      status: unit.status,
    };
  }

  return {
    unit_number: "",
    unit_type: "",
    description: "",
    floor: "",
    building: "",
    bedrooms: 0,
    bathrooms: 0,
    orientation: "",
    has_parking: false,
    has_storage: false,
    parkings: "",
    storages: "",
    total_area: "",
    surface_internal: "",
    surface_terrace: "",
    surface_garden: "",
    surface_pantry: "",
    surface_multiuse_assignable: "",
    surface_util: "",
    surface_terrain: "",
    surface_others: "",
    currency: "UF",
    value_base: "",
    value_uf: "",
    value_list: "",
    value_discount: "",
    value_enabled: "",
    value_promotion: "",
    value_bonus: "",
    value_parking: "",
    value_storage: "",
    status: "available",
  };
}

function cleanData(data: Record<string, unknown>) {
  const cleaned: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(data)) {
    if (typeof value === "string" && value.trim() === "") continue;
    if (value === undefined) continue;
    cleaned[key] = value;
  }
  return cleaned;
}

interface StockFormProps {
  projectId: number;
  unit?: StockUnit;
  onSuccess: () => void;
  onCancel: () => void;
}

export function StockForm({
  projectId,
  unit,
  onSuccess,
  onCancel,
}: StockFormProps) {
  const isEdit = !!unit;
  const createStock = useCreateStock();
  const updateStock = useUpdateStock();

  const {
    register,
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<FormValues>({
    resolver: zodResolver(stockSchema),
    defaultValues: getDefaults(unit),
  });

  useEffect(() => {
    reset(getDefaults(unit));
  }, [unit, reset]);

  const isPending = createStock.isPending || updateStock.isPending;

  function onSubmit(data: FormValues) {
    const parsed = stockSchema.safeParse(data);
    if (!parsed.success) return;

    const payload = cleanData(parsed.data as Record<string, unknown>);

    if (isEdit && unit) {
      updateStock.mutate(
        { id: unit.id, data: payload },
        {
          onSuccess: () => {
            toast.success("Unidad actualizada exitosamente");
            onSuccess();
          },
          onError: () => toast.error("Error al actualizar la unidad"),
        }
      );
    } else {
      createStock.mutate(
        { project_id: projectId, ...payload } as Parameters<
          typeof createStock.mutate
        >[0],
        {
          onSuccess: () => {
            toast.success("Unidad creada exitosamente");
            onSuccess();
          },
          onError: () => toast.error("Error al crear la unidad"),
        }
      );
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      {/* ── Identificación ── */}
      <div>
        <h3 className="text-sm font-semibold mb-3">Identificación</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="unit_number">Unidad *</Label>
            <Input id="unit_number" {...register("unit_number")} />
            {errors.unit_number && (
              <p className="text-sm text-destructive">
                {errors.unit_number.message}
              </p>
            )}
          </div>

          <div className="space-y-2">
            <Label>Tipo *</Label>
            <Controller
              name="unit_type"
              control={control}
              render={({ field }) => (
                <Select
                  value={field.value || undefined}
                  onValueChange={field.onChange}
                >
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Seleccionar tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    {UNIT_TYPES.map((t) => (
                      <SelectItem key={t.value} value={t.value}>
                        {t.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
            />
            {errors.unit_type && (
              <p className="text-sm text-destructive">
                {errors.unit_type.message}
              </p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="floor">Piso</Label>
            <Input id="floor" type="number" {...register("floor")} />
          </div>

          <div className="space-y-2">
            <Label htmlFor="building">Edificio</Label>
            <Input id="building" {...register("building")} />
          </div>

          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="description">Descripción</Label>
            <Textarea id="description" rows={2} {...register("description")} />
          </div>
        </div>
      </div>

      <Separator />

      {/* ── Espacios ── */}
      <div>
        <h3 className="text-sm font-semibold mb-3">Espacios</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="bedrooms">Dormitorios</Label>
            <Input
              id="bedrooms"
              type="number"
              min={0}
              {...register("bedrooms")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="bathrooms">Baños</Label>
            <Input
              id="bathrooms"
              type="number"
              min={0}
              {...register("bathrooms")}
            />
          </div>

          <div className="space-y-2">
            <Label>Orientación</Label>
            <Controller
              name="orientation"
              control={control}
              render={({ field }) => (
                <Select
                  value={field.value || NONE}
                  onValueChange={(val) =>
                    field.onChange(val === NONE ? "" : val)
                  }
                >
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Seleccionar" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value={NONE}>Sin especificar</SelectItem>
                    {ORIENTATION_TYPES.map((o) => (
                      <SelectItem key={o.value} value={o.value}>
                        {o.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
            />
          </div>

          <div />

          <div className="col-span-full flex flex-wrap gap-6 pt-1">
            <Controller
              name="has_parking"
              control={control}
              render={({ field }) => (
                <div className="flex items-center gap-2">
                  <Switch
                    checked={field.value}
                    onCheckedChange={field.onChange}
                  />
                  <Label>Estacionamiento</Label>
                </div>
              )}
            />
            <Controller
              name="has_storage"
              control={control}
              render={({ field }) => (
                <div className="flex items-center gap-2">
                  <Switch
                    checked={field.value}
                    onCheckedChange={field.onChange}
                  />
                  <Label>Bodega</Label>
                </div>
              )}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="parkings">Estacionamientos (detalle)</Label>
            <Input id="parkings" {...register("parkings")} />
          </div>

          <div className="space-y-2">
            <Label htmlFor="storages">Bodegas (detalle)</Label>
            <Input id="storages" {...register("storages")} />
          </div>
        </div>
      </div>

      <Separator />

      {/* ── Superficies ── */}
      <div>
        <h3 className="text-sm font-semibold mb-3">Superficies (m²)</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="total_area">Superficie total</Label>
            <Input
              id="total_area"
              type="number"
              step="0.01"
              {...register("total_area")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="surface_internal">Interior</Label>
            <Input
              id="surface_internal"
              type="number"
              step="0.01"
              {...register("surface_internal")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="surface_terrace">Terraza</Label>
            <Input
              id="surface_terrace"
              type="number"
              step="0.01"
              {...register("surface_terrace")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="surface_garden">Jardín</Label>
            <Input
              id="surface_garden"
              type="number"
              step="0.01"
              {...register("surface_garden")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="surface_pantry">Logia</Label>
            <Input
              id="surface_pantry"
              type="number"
              step="0.01"
              {...register("surface_pantry")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="surface_multiuse_assignable">
              Multiuso asignable
            </Label>
            <Input
              id="surface_multiuse_assignable"
              type="number"
              step="0.01"
              {...register("surface_multiuse_assignable")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="surface_util">Útil</Label>
            <Input
              id="surface_util"
              type="number"
              step="0.01"
              {...register("surface_util")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="surface_terrain">Terreno</Label>
            <Input
              id="surface_terrain"
              type="number"
              step="0.01"
              {...register("surface_terrain")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="surface_others">Otras</Label>
            <Input
              id="surface_others"
              type="number"
              step="0.01"
              {...register("surface_others")}
            />
          </div>
        </div>
      </div>

      <Separator />

      {/* ── Valores ── */}
      <div>
        <h3 className="text-sm font-semibold mb-3">Valores</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label>Moneda</Label>
            <Controller
              name="currency"
              control={control}
              render={({ field }) => (
                <Select value={field.value} onValueChange={field.onChange}>
                  <SelectTrigger className="w-full">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {CURRENCY_TYPES.map((c) => (
                      <SelectItem key={c.value} value={c.value}>
                        {c.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="value_base">Valor base</Label>
            <Input
              id="value_base"
              type="number"
              step="0.01"
              {...register("value_base")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="value_uf">Valor UF</Label>
            <Input
              id="value_uf"
              type="number"
              step="0.01"
              {...register("value_uf")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="value_list">Valor lista</Label>
            <Input
              id="value_list"
              type="number"
              step="0.01"
              {...register("value_list")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="value_discount">Descuento</Label>
            <Input
              id="value_discount"
              type="number"
              step="0.01"
              {...register("value_discount")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="value_enabled">Valor habilitado</Label>
            <Input
              id="value_enabled"
              type="number"
              step="0.01"
              {...register("value_enabled")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="value_promotion">Promoción</Label>
            <Input
              id="value_promotion"
              type="number"
              step="0.01"
              {...register("value_promotion")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="value_bonus">Bono</Label>
            <Input
              id="value_bonus"
              type="number"
              step="0.01"
              {...register("value_bonus")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="value_parking">Estacionamiento</Label>
            <Input
              id="value_parking"
              type="number"
              step="0.01"
              {...register("value_parking")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="value_storage">Bodega</Label>
            <Input
              id="value_storage"
              type="number"
              step="0.01"
              {...register("value_storage")}
            />
          </div>
        </div>
      </div>

      <Separator />

      {/* ── Estado ── */}
      <div>
        <h3 className="text-sm font-semibold mb-3">Estado</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label>Estado</Label>
            <Controller
              name="status"
              control={control}
              render={({ field }) => (
                <Select value={field.value} onValueChange={field.onChange}>
                  <SelectTrigger className="w-full">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {STOCK_STATUSES.map((s) => (
                      <SelectItem key={s.value} value={s.value}>
                        {s.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
            />
          </div>
        </div>
      </div>

      <div className="flex justify-end gap-2 pt-4">
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancelar
        </Button>
        <Button type="submit" disabled={isPending}>
          {isPending && <Loader2 className="size-4 animate-spin" />}
          Guardar
        </Button>
      </div>
    </form>
  );
}
