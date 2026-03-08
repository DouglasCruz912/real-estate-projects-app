"use client";

import { useEffect } from "react";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { toast } from "sonner";
import type { Project } from "@/types/project";
import { useCompanies } from "@/hooks/useCompanies";
import { useCreateProject, useUpdateProject } from "@/hooks/useProjects";
import { PROJECT_STATES, CURRENCY_TYPES } from "@/lib/constants";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Loader2 } from "lucide-react";

const numField = z
  .union([z.string(), z.number()])
  .optional()
  .transform((v) => {
    if (v === undefined || v === null || v === "") return undefined;
    const n = typeof v === "string" ? parseFloat(v) : v;
    return isNaN(n) ? undefined : n;
  });

const projectSchema = z.object({
  name: z
    .string()
    .min(1, "El nombre es requerido")
    .max(200, "Máximo 200 caracteres"),
  company_id: z.number().min(1, "La empresa es requerida"),
  type: z.string().optional(),
  delivery_type: z.string().optional(),
  state: z.string(),
  executive: z.string().optional(),
  executive_email: z.string().optional(),
  is_active: z.boolean(),
  is_published: z.boolean(),
  is_promo: z.boolean(),
  is_hot: z.boolean(),
  address: z.string().optional(),
  street_number: z.string().optional(),
  city: z.string().optional(),
  commune: z.string().optional(),
  region: z.string().optional(),
  country: z.string().optional(),
  postal_code: z.string().optional(),
  url_google_maps: z.string().optional(),
  latitude: z.string().optional(),
  longitude: z.string().optional(),
  phone: z.string().optional(),
  website: z.string().optional(),
  currency: z.string(),
  price_from: numField,
  price_to: numField,
  unique_price: numField,
  start_date: z.string().optional(),
  delivery_date: z.string().optional(),
  delivery_end_date: z.string().optional(),
  launch_date: z.string().optional(),
  after_sales_email: z.string().optional(),
  after_sales_executive: z.string().optional(),
  after_sales_phone: z.string().optional(),
  finances_insurance_company: z.string().optional(),
  finances_insurance_policy: z.string().optional(),
  finances_insured_value: z.string().optional(),
  finances_insured_value_util: z.string().optional(),
  finances_benefit: z.string().optional(),
  finances_annual_rate: numField,
  finances_credit_rate: numField,
  down_payment_bonus: numField,
  reservation: numField,
  pre_approval: z.string().optional(),
  installments: numField,
  balloon_payment: z.string().optional(),
  annual_capital_gain: numField,
  construction_capital_gain: numField,
  vacancy: numField,
  additional_information: z.string().optional(),
  initial_payment: numField,
  big_down_payment: numField,
});

type FormValues = z.input<typeof projectSchema>;

function getDefaults(project?: Project): FormValues {
  if (project) {
    return {
      name: project.name,
      company_id: project.company_id,
      type: project.type ?? "",
      delivery_type: project.delivery_type ?? "",
      state: project.state,
      executive: project.executive ?? "",
      executive_email: project.executive_email ?? "",
      is_active: project.is_active,
      is_published: project.is_published,
      is_promo: project.is_promo,
      is_hot: project.is_hot,
      address: project.address ?? "",
      street_number: project.street_number ?? "",
      city: project.city ?? "",
      commune: project.commune ?? "",
      region: project.region ?? "",
      country: project.country ?? "",
      postal_code: project.postal_code ?? "",
      url_google_maps: project.url_google_maps ?? "",
      latitude: project.latitude ?? "",
      longitude: project.longitude ?? "",
      phone: project.phone ?? "",
      website: project.website ?? "",
      currency: project.currency,
      price_from: project.price_from ?? "",
      price_to: project.price_to ?? "",
      unique_price: project.unique_price ?? "",
      start_date: project.start_date ?? "",
      delivery_date: project.delivery_date ?? "",
      delivery_end_date: project.delivery_end_date ?? "",
      launch_date: project.launch_date ?? "",
      after_sales_email: project.after_sales_email ?? "",
      after_sales_executive: project.after_sales_executive ?? "",
      after_sales_phone: project.after_sales_phone ?? "",
      finances_insurance_company: project.finances_insurance_company ?? "",
      finances_insurance_policy: project.finances_insurance_policy ?? "",
      finances_insured_value: project.finances_insured_value ?? "",
      finances_insured_value_util: project.finances_insured_value_util ?? "",
      finances_benefit: project.finances_benefit ?? "",
      finances_annual_rate: project.finances_annual_rate ?? "",
      finances_credit_rate: project.finances_credit_rate ?? "",
      down_payment_bonus: project.down_payment_bonus ?? "",
      reservation: project.reservation ?? "",
      pre_approval: project.pre_approval ?? "",
      installments: project.installments ?? "",
      balloon_payment: project.balloon_payment ?? "",
      annual_capital_gain: project.annual_capital_gain ?? "",
      construction_capital_gain: project.construction_capital_gain ?? "",
      vacancy: project.vacancy ?? "",
      additional_information: project.additional_information ?? "",
      initial_payment: project.initial_payment ?? "",
      big_down_payment: project.big_down_payment ?? "",
    };
  }

  return {
    name: "",
    company_id: 0,
    type: "",
    delivery_type: "",
    state: "planning",
    executive: "",
    executive_email: "",
    is_active: true,
    is_published: false,
    is_promo: false,
    is_hot: false,
    address: "",
    street_number: "",
    city: "",
    commune: "",
    region: "",
    country: "",
    postal_code: "",
    url_google_maps: "",
    latitude: "",
    longitude: "",
    phone: "",
    website: "",
    currency: "UF",
    price_from: "",
    price_to: "",
    unique_price: "",
    start_date: "",
    delivery_date: "",
    delivery_end_date: "",
    launch_date: "",
    after_sales_email: "",
    after_sales_executive: "",
    after_sales_phone: "",
    finances_insurance_company: "",
    finances_insurance_policy: "",
    finances_insured_value: "",
    finances_insured_value_util: "",
    finances_benefit: "",
    finances_annual_rate: "",
    finances_credit_rate: "",
    down_payment_bonus: "",
    reservation: "",
    pre_approval: "",
    installments: "",
    balloon_payment: "",
    annual_capital_gain: "",
    construction_capital_gain: "",
    vacancy: "",
    additional_information: "",
    initial_payment: "",
    big_down_payment: "",
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

interface ProjectFormProps {
  project?: Project;
  onSuccess: () => void;
}

export function ProjectForm({ project, onSuccess }: ProjectFormProps) {
  const isEdit = !!project;
  const { data: companies } = useCompanies();
  const createProject = useCreateProject();
  const updateProject = useUpdateProject();

  const {
    register,
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<FormValues>({
    resolver: zodResolver(projectSchema),
    defaultValues: getDefaults(project),
  });

  useEffect(() => {
    if (project) {
      reset(getDefaults(project));
    }
  }, [project, reset]);

  const isPending = createProject.isPending || updateProject.isPending;

  function onSubmit(data: z.input<typeof projectSchema>) {
    const parsed = projectSchema.safeParse(data);
    if (!parsed.success) return;

    const payload = cleanData(parsed.data as Record<string, unknown>);

    if (isEdit && project) {
      updateProject.mutate(
        { id: project.id, data: payload },
        {
          onSuccess: () => {
            toast.success("Proyecto actualizado exitosamente");
            onSuccess();
          },
          onError: () => toast.error("Error al actualizar el proyecto"),
        }
      );
    } else {
      createProject.mutate(payload as unknown as Parameters<typeof createProject.mutate>[0], {
        onSuccess: () => {
          toast.success("Proyecto creado exitosamente");
          onSuccess();
        },
        onError: () => toast.error("Error al crear el proyecto"),
      });
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <Tabs defaultValue="basic">
        <TabsList className="w-full justify-start">
          <TabsTrigger value="basic">Información Básica</TabsTrigger>
          <TabsTrigger value="location">Ubicación</TabsTrigger>
          <TabsTrigger value="prices">Precios y Fechas</TabsTrigger>
          <TabsTrigger value="commercial">Info Comercial</TabsTrigger>
        </TabsList>

        {/* ── Tab 1: Información Básica ── */}
        <TabsContent value="basic" className="mt-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="name">Nombre *</Label>
              <Input id="name" {...register("name")} />
              {errors.name && (
                <p className="text-sm text-destructive">{errors.name.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label>Empresa *</Label>
              <Controller
                name="company_id"
                control={control}
                render={({ field }) => (
                  <Select
                    value={field.value > 0 ? String(field.value) : null}
                    onValueChange={(val) => field.onChange(Number(val))}
                  >
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="Seleccionar empresa" />
                    </SelectTrigger>
                    <SelectContent>
                      {companies?.map((c) => (
                        <SelectItem key={c.id} value={String(c.id)}>
                          {c.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
              {errors.company_id && (
                <p className="text-sm text-destructive">
                  {errors.company_id.message}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="type">Tipo</Label>
              <Input id="type" {...register("type")} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="delivery_type">Tipo de entrega</Label>
              <Input id="delivery_type" {...register("delivery_type")} />
            </div>

            <div className="space-y-2">
              <Label>Estado</Label>
              <Controller
                name="state"
                control={control}
                render={({ field }) => (
                  <Select value={field.value} onValueChange={field.onChange}>
                    <SelectTrigger className="w-full">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {PROJECT_STATES.map((s) => (
                        <SelectItem key={s.value} value={s.value}>
                          {s.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="executive">Ejecutivo</Label>
              <Input id="executive" {...register("executive")} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="executive_email">Email ejecutivo</Label>
              <Input
                id="executive_email"
                type="email"
                {...register("executive_email")}
              />
            </div>

            <div className="col-span-full flex flex-wrap gap-6 pt-2">
              <Controller
                name="is_active"
                control={control}
                render={({ field }) => (
                  <div className="flex items-center gap-2">
                    <Switch
                      checked={field.value}
                      onCheckedChange={field.onChange}
                    />
                    <Label>Activo</Label>
                  </div>
                )}
              />
              <Controller
                name="is_published"
                control={control}
                render={({ field }) => (
                  <div className="flex items-center gap-2">
                    <Switch
                      checked={field.value}
                      onCheckedChange={field.onChange}
                    />
                    <Label>Publicado</Label>
                  </div>
                )}
              />
              <Controller
                name="is_promo"
                control={control}
                render={({ field }) => (
                  <div className="flex items-center gap-2">
                    <Switch
                      checked={field.value}
                      onCheckedChange={field.onChange}
                    />
                    <Label>Promoción</Label>
                  </div>
                )}
              />
              <Controller
                name="is_hot"
                control={control}
                render={({ field }) => (
                  <div className="flex items-center gap-2">
                    <Switch
                      checked={field.value}
                      onCheckedChange={field.onChange}
                    />
                    <Label>Destacado</Label>
                  </div>
                )}
              />
            </div>
          </div>
        </TabsContent>

        {/* ── Tab 2: Ubicación ── */}
        <TabsContent value="location" className="mt-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="address">Dirección</Label>
              <Textarea id="address" rows={2} {...register("address")} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="street_number">Número</Label>
              <Input id="street_number" {...register("street_number")} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="city">Ciudad</Label>
              <Input id="city" {...register("city")} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="commune">Comuna</Label>
              <Input id="commune" {...register("commune")} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="region">Región</Label>
              <Input id="region" {...register("region")} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="country">País</Label>
              <Input id="country" {...register("country")} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="postal_code">Código postal</Label>
              <Input id="postal_code" {...register("postal_code")} />
            </div>

            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="url_google_maps">URL Google Maps</Label>
              <Input
                id="url_google_maps"
                type="url"
                {...register("url_google_maps")}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="latitude">Latitud</Label>
              <Input id="latitude" {...register("latitude")} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="longitude">Longitud</Label>
              <Input id="longitude" {...register("longitude")} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="phone">Teléfono</Label>
              <Input id="phone" type="tel" {...register("phone")} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="website">Sitio web</Label>
              <Input id="website" type="url" {...register("website")} />
            </div>
          </div>
        </TabsContent>

        {/* ── Tab 3: Precios y Fechas ── */}
        <TabsContent value="prices" className="mt-4">
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
              <Label htmlFor="unique_price">Precio único</Label>
              <Input
                id="unique_price"
                type="number"
                step="0.01"
                {...register("unique_price")}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="price_from">Precio desde</Label>
              <Input
                id="price_from"
                type="number"
                step="0.01"
                {...register("price_from")}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="price_to">Precio hasta</Label>
              <Input
                id="price_to"
                type="number"
                step="0.01"
                {...register("price_to")}
              />
            </div>

            <Separator className="col-span-full my-2" />

            <div className="space-y-2">
              <Label htmlFor="start_date">Fecha de inicio</Label>
              <Input id="start_date" type="date" {...register("start_date")} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="delivery_date">Fecha de entrega</Label>
              <Input
                id="delivery_date"
                type="date"
                {...register("delivery_date")}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="delivery_end_date">Fin de entrega</Label>
              <Input
                id="delivery_end_date"
                type="date"
                {...register("delivery_end_date")}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="launch_date">Fecha de lanzamiento</Label>
              <Input
                id="launch_date"
                type="date"
                {...register("launch_date")}
              />
            </div>
          </div>
        </TabsContent>

        {/* ── Tab 4: Información Comercial ── */}
        <TabsContent value="commercial" className="mt-4 space-y-6">
          {/* Postventa */}
          <div>
            <h3 className="text-sm font-semibold mb-3">Postventa</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="after_sales_email">Email postventa</Label>
                <Input
                  id="after_sales_email"
                  type="email"
                  {...register("after_sales_email")}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="after_sales_executive">Ejecutivo postventa</Label>
                <Input
                  id="after_sales_executive"
                  {...register("after_sales_executive")}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="after_sales_phone">Teléfono postventa</Label>
                <Input
                  id="after_sales_phone"
                  type="tel"
                  {...register("after_sales_phone")}
                />
              </div>
            </div>
          </div>

          <Separator />

          {/* Financiera */}
          <div>
            <h3 className="text-sm font-semibold mb-3">Financiera</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="finances_insurance_company">
                  Compañía de seguros
                </Label>
                <Input
                  id="finances_insurance_company"
                  {...register("finances_insurance_company")}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="finances_insurance_policy">
                  Póliza de seguros
                </Label>
                <Input
                  id="finances_insurance_policy"
                  {...register("finances_insurance_policy")}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="finances_insured_value">Valor asegurado</Label>
                <Input
                  id="finances_insured_value"
                  {...register("finances_insured_value")}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="finances_insured_value_util">
                  Valor asegurado útil
                </Label>
                <Input
                  id="finances_insured_value_util"
                  {...register("finances_insured_value_util")}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="finances_benefit">Beneficio</Label>
                <Input
                  id="finances_benefit"
                  {...register("finances_benefit")}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="finances_annual_rate">Tasa anual</Label>
                <Input
                  id="finances_annual_rate"
                  type="number"
                  step="0.01"
                  {...register("finances_annual_rate")}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="finances_credit_rate">Tasa de crédito</Label>
                <Input
                  id="finances_credit_rate"
                  type="number"
                  step="0.01"
                  {...register("finances_credit_rate")}
                />
              </div>
            </div>
          </div>

          <Separator />

          {/* Pagos */}
          <div>
            <h3 className="text-sm font-semibold mb-3">Pagos</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="down_payment_bonus">Bono pie</Label>
                <Input
                  id="down_payment_bonus"
                  type="number"
                  step="0.01"
                  {...register("down_payment_bonus")}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="reservation">Reserva</Label>
                <Input
                  id="reservation"
                  type="number"
                  step="0.01"
                  {...register("reservation")}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="pre_approval">Pre-aprobación</Label>
                <Input id="pre_approval" {...register("pre_approval")} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="installments">Cuotas</Label>
                <Input
                  id="installments"
                  type="number"
                  {...register("installments")}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="balloon_payment">Pago globo</Label>
                <Input
                  id="balloon_payment"
                  {...register("balloon_payment")}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="initial_payment">Pago inicial</Label>
                <Input
                  id="initial_payment"
                  type="number"
                  step="0.01"
                  {...register("initial_payment")}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="big_down_payment">Pie grande</Label>
                <Input
                  id="big_down_payment"
                  type="number"
                  step="0.01"
                  {...register("big_down_payment")}
                />
              </div>
            </div>
          </div>

          <Separator />

          {/* Rentabilidad */}
          <div>
            <h3 className="text-sm font-semibold mb-3">Rentabilidad</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="annual_capital_gain">Plusvalía anual</Label>
                <Input
                  id="annual_capital_gain"
                  type="number"
                  step="0.01"
                  {...register("annual_capital_gain")}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="construction_capital_gain">
                  Plusvalía construcción
                </Label>
                <Input
                  id="construction_capital_gain"
                  type="number"
                  step="0.01"
                  {...register("construction_capital_gain")}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="vacancy">Vacancia</Label>
                <Input
                  id="vacancy"
                  type="number"
                  step="0.01"
                  {...register("vacancy")}
                />
              </div>
            </div>
          </div>

          <Separator />

          {/* Adicional */}
          <div>
            <h3 className="text-sm font-semibold mb-3">Adicional</h3>
            <div className="space-y-2">
              <Label htmlFor="additional_information">
                Información adicional
              </Label>
              <Textarea
                id="additional_information"
                rows={4}
                {...register("additional_information")}
              />
            </div>
          </div>
        </TabsContent>
      </Tabs>

      <div className="flex justify-end pt-4">
        <Button type="submit" disabled={isPending}>
          {isPending && <Loader2 className="size-4 animate-spin" />}
          {isEdit ? "Guardar Cambios" : "Crear Proyecto"}
        </Button>
      </div>
    </form>
  );
}
