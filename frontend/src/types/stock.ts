export interface StockUnit {
  id: number;
  project_id: number;
  unit_number: string;
  unit_type: string;
  description?: string | null;
  bedrooms: number;
  bathrooms: number;
  orientation?: string | null;
  total_area?: number | null;
  floor?: number | null;
  building?: string | null;
  parkings?: string | null;
  storages?: string | null;
  has_parking: boolean;
  has_storage: boolean;
  surface_internal?: number | null;
  surface_terrace?: number | null;
  surface_garden?: number | null;
  surface_pantry?: number | null;
  surface_multiuse_assignable?: number | null;
  surface_util?: number | null;
  surface_terrain?: number | null;
  surface_others?: number | null;
  currency: string;
  value_base?: number | null;
  value_uf?: number | null;
  value_list?: number | null;
  value_discount?: number | null;
  value_enabled?: number | null;
  value_promotion?: number | null;
  value_bonus?: number | null;
  value_parking?: number | null;
  value_storage?: number | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface StockCreate {
  project_id: number;
  unit_number: string;
  unit_type: string;
  description?: string;
  bedrooms?: number;
  bathrooms?: number;
  orientation?: string;
  total_area?: number;
  floor?: number;
  building?: string;
  parkings?: string;
  storages?: string;
  has_parking?: boolean;
  has_storage?: boolean;
  surface_internal?: number;
  surface_terrace?: number;
  surface_garden?: number;
  surface_pantry?: number;
  surface_multiuse_assignable?: number;
  surface_util?: number;
  surface_terrain?: number;
  surface_others?: number;
  currency?: string;
  value_base?: number;
  value_uf?: number;
  value_list?: number;
  value_discount?: number;
  value_enabled?: number;
  value_promotion?: number;
  value_bonus?: number;
  value_parking?: number;
  value_storage?: number;
  status?: string;
}

export type StockUpdate = Partial<Omit<StockCreate, "project_id">>;

export interface StockFilters {
  skip?: number;
  limit?: number;
  available_only?: boolean;
}

export interface StockListResponse {
  stock: StockUnit[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}
