export interface Company {
  id: number;
  name: string;
  legal_name?: string | null;
  rut?: string | null;
  email?: string | null;
  phone?: string | null;
  website?: string | null;
  address?: string | null;
  city?: string | null;
  region?: string | null;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface CompanyCreate {
  name: string;
  legal_name?: string;
  rut?: string;
  email?: string;
  phone?: string;
  website?: string;
  address?: string;
  city?: string;
  region?: string;
  is_active?: boolean;
  is_verified?: boolean;
}

export type CompanyUpdate = Partial<CompanyCreate>;

export interface CompanyFilters {
  skip?: number;
  limit?: number;
  search?: string;
  city?: string;
  region?: string;
  is_active?: boolean;
  is_verified?: boolean;
}
