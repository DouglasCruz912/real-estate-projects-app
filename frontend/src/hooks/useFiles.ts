import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import fileService from "@/services/fileService";

export function useProjectImages(projectId: number) {
  return useQuery({
    queryKey: ["images", projectId],
    queryFn: () => fileService.getImages(projectId),
    enabled: projectId > 0,
  });
}

export function useUploadImages() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      projectId,
      files,
      opts,
    }: {
      projectId: number;
      files: File[];
      opts?: { image_type?: string; alt_text?: string; is_featured?: boolean };
    }) => fileService.uploadImages(projectId, files, opts),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["images"] });
    },
  });
}

export function useDeleteImage() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (imageId: number) => fileService.deleteImage(imageId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["images"] });
    },
  });
}

export function useProjectDocuments(projectId: number) {
  return useQuery({
    queryKey: ["documents", projectId],
    queryFn: () => fileService.getDocuments(projectId),
    enabled: projectId > 0,
  });
}

export function useUploadDocument() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      projectId,
      file,
      documentType,
    }: {
      projectId: number;
      file: File;
      documentType?: string;
    }) => fileService.uploadDocument(projectId, file, documentType),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["documents"] });
    },
  });
}

export function useDeleteDocument() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (documentId: number) => fileService.deleteDocument(documentId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["documents"] });
    },
  });
}
