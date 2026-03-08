import api from "@/services/api";
import type { ProjectImage, ProjectDocument } from "@/types/file";

interface UploadImageOptions {
  image_type?: string;
  alt_text?: string;
  is_featured?: boolean;
}

interface UpdateImageData {
  image_type?: string;
  alt_text?: string;
  is_featured?: boolean;
  is_active?: boolean;
  display_order?: number;
}

const fileService = {
  getImages(
    projectId: number,
    params?: Record<string, unknown>
  ): Promise<ProjectImage[]> {
    return api
      .get(`/api/files/project/${projectId}/images`, { params })
      .then((res) => res.data);
  },

  uploadImages(
    projectId: number,
    files: File[],
    brokerEmail: string,
    opts?: UploadImageOptions
  ): Promise<ProjectImage[]> {
    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));
    if (opts?.image_type) formData.append("image_type", opts.image_type);
    if (opts?.alt_text) formData.append("alt_text", opts.alt_text);
    if (opts?.is_featured !== undefined)
      formData.append("is_featured", String(opts.is_featured));

    return api
      .post(`/api/files/project/${projectId}/images`, formData, {
        params: { broker_email: brokerEmail },
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((res) => res.data);
  },

  updateImage(
    imageId: number,
    brokerEmail: string,
    data: UpdateImageData
  ): Promise<ProjectImage> {
    return api
      .put(`/api/files/project-image/${imageId}`, null, {
        params: { broker_email: brokerEmail, ...data },
      })
      .then((res) => res.data);
  },

  deleteImage(imageId: number, brokerEmail: string): Promise<void> {
    return api
      .delete(`/api/files/project-image/${imageId}`, {
        params: { broker_email: brokerEmail },
      })
      .then((res) => res.data);
  },

  getDocuments(
    projectId: number,
    params?: Record<string, unknown>
  ): Promise<ProjectDocument[]> {
    return api
      .get(`/api/files/project/${projectId}/documents`, { params })
      .then((res) => res.data);
  },

  uploadDocument(
    projectId: number,
    file: File,
    brokerEmail: string,
    documentType?: string
  ): Promise<ProjectDocument> {
    const formData = new FormData();
    formData.append("file", file);
    if (documentType) formData.append("document_type", documentType);

    return api
      .post(`/api/files/project/${projectId}/documents`, formData, {
        params: { broker_email: brokerEmail },
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((res) => res.data);
  },

  deleteDocument(documentId: number, brokerEmail: string): Promise<void> {
    return api
      .delete(`/api/files/project-document/${documentId}`, {
        params: { broker_email: brokerEmail },
      })
      .then((res) => res.data);
  },
};

export default fileService;
