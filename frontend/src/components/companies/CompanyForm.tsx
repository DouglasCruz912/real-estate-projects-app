"use client"

import { useForm, Controller } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import type { Company } from "@/types/company"
import { useCreateCompany, useUpdateCompany } from "@/hooks/useCompanies"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { toast } from "sonner"
import { Loader2 } from "lucide-react"

const companySchema = z.object({
  name: z.string().min(1, "El nombre es requerido").max(255),
  legal_name: z.string().optional(),
  tax_id: z.string().max(20, "Máximo 20 caracteres").optional(),
  email: z.string().email("Email inválido").or(z.literal("")).optional(),
  phone: z.string().optional(),
  website: z.string().optional(),
  address: z.string().optional(),
  city: z.string().optional(),
  region: z.string().optional(),
  is_active: z.boolean(),
  is_verified: z.boolean(),
})

type CompanyFormValues = z.infer<typeof companySchema>

interface CompanyFormProps {
  company?: Company
  onSuccess: () => void
}

function cleanOptionalStrings(
  data: CompanyFormValues
): Record<string, unknown> {
  return Object.fromEntries(
    Object.entries(data).map(([key, value]) => [
      key,
      typeof value === "string" && value.trim() === "" ? undefined : value,
    ])
  )
}

export function CompanyForm({ company, onSuccess }: CompanyFormProps) {
  const createMutation = useCreateCompany()
  const updateMutation = useUpdateCompany()
  const isEditing = !!company

  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
  } = useForm<CompanyFormValues>({
    resolver: zodResolver(companySchema),
    defaultValues: {
      name: company?.name ?? "",
      legal_name: company?.legal_name ?? "",
      tax_id: company?.tax_id ?? "",
      email: company?.email ?? "",
      phone: company?.phone ?? "",
      website: company?.website ?? "",
      address: company?.address ?? "",
      city: company?.city ?? "",
      region: company?.region ?? "",
      is_active: company?.is_active ?? true,
      is_verified: company?.is_verified ?? false,
    },
  })

  const isPending = createMutation.isPending || updateMutation.isPending

  const onSubmit = (data: CompanyFormValues) => {
    const payload = cleanOptionalStrings(data)

    if (isEditing) {
      updateMutation.mutate(
        { id: company.id, data: payload },
        {
          onSuccess: () => {
            toast.success("Inmobiliaria actualizada correctamente")
            onSuccess()
          },
          onError: () => toast.error("Error al actualizar la inmobiliaria"),
        }
      )
    } else {
      createMutation.mutate(payload as CompanyFormValues, {
        onSuccess: () => {
          toast.success("Inmobiliaria creada correctamente")
          onSuccess()
        },
        onError: () => toast.error("Error al crear la inmobiliaria"),
      })
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-2">
        <div className="space-y-1.5">
          <Label htmlFor="name">Nombre *</Label>
          <Input
            id="name"
            placeholder="Nombre de la inmobiliaria"
            aria-invalid={!!errors.name}
            {...register("name")}
          />
          {errors.name && (
            <p className="text-sm text-destructive">{errors.name.message}</p>
          )}
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="legal_name">Razón Social</Label>
          <Input
            id="legal_name"
            placeholder="Razón social"
            {...register("legal_name")}
          />
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="tax_id">ID Fiscal</Label>
          <Input
            id="tax_id"
            placeholder="RUT, NIF, EIN, etc."
            aria-invalid={!!errors.tax_id}
            {...register("tax_id")}
          />
          {errors.tax_id && (
            <p className="text-sm text-destructive">{errors.tax_id.message}</p>
          )}
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            placeholder="contacto@empresa.com"
            aria-invalid={!!errors.email}
            {...register("email")}
          />
          {errors.email && (
            <p className="text-sm text-destructive">{errors.email.message}</p>
          )}
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="phone">Teléfono</Label>
          <Input
            id="phone"
            placeholder="+1 234 567 8900"
            {...register("phone")}
          />
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="website">Sitio Web</Label>
          <Input
            id="website"
            placeholder="https://www.empresa.com"
            {...register("website")}
          />
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="city">Ciudad</Label>
          <Input
            id="city"
            placeholder="Ciudad"
            {...register("city")}
          />
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="region">Región / Estado</Label>
          <Input
            id="region"
            placeholder="Región, estado o provincia"
            {...register("region")}
          />
        </div>
      </div>

      <div className="space-y-1.5">
        <Label htmlFor="address">Dirección</Label>
        <Textarea
          id="address"
          placeholder="Dirección completa"
          {...register("address")}
        />
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <Controller
          name="is_active"
          control={control}
          render={({ field }) => (
            <div className="flex items-center justify-between rounded-lg border p-3">
              <div className="space-y-0.5">
                <Label htmlFor="is_active">Activa</Label>
                <p className="text-xs text-muted-foreground">
                  La inmobiliaria aparecerá en el sistema
                </p>
              </div>
              <Switch
                id="is_active"
                checked={field.value}
                onCheckedChange={field.onChange}
              />
            </div>
          )}
        />

        <Controller
          name="is_verified"
          control={control}
          render={({ field }) => (
            <div className="flex items-center justify-between rounded-lg border p-3">
              <div className="space-y-0.5">
                <Label htmlFor="is_verified">Verificada</Label>
                <p className="text-xs text-muted-foreground">
                  Empresa con documentación verificada
                </p>
              </div>
              <Switch
                id="is_verified"
                checked={field.value}
                onCheckedChange={field.onChange}
              />
            </div>
          )}
        />
      </div>

      <div className="flex justify-end">
        <Button type="submit" disabled={isPending}>
          {isPending && <Loader2 className="size-4 animate-spin" />}
          {isEditing ? "Guardar Cambios" : "Crear Inmobiliaria"}
        </Button>
      </div>
    </form>
  )
}
