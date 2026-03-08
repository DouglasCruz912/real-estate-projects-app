export interface ProjectImage {
  id: number;
  project_id: number;
  filename: string;
  url: string;
  urls_list?: string[];
  individual_images_count?: number;
  alt_text?: string | null;
  image_type: string;
  is_featured: boolean;
  is_active: boolean;
  display_order: number;
  created_at: string;
  updated_at: string;
}

export interface ProjectDocument {
  id: number;
  project_id: number;
  filename: string;
  url: string;
  document_type: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}
