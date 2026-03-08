"use client";

import { useParams } from "next/navigation";
import Link from "next/link";
import {
  useProjectImages,
  useDeleteImage,
  useProjectDocuments,
  useDeleteDocument,
} from "@/hooks/useFiles";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ImageUploader } from "@/components/files/ImageUploader";
import { ImageGallery } from "@/components/files/ImageGallery";
import { DocumentList } from "@/components/files/DocumentList";
import { ArrowLeft, ImageIcon, FileText } from "lucide-react";
import { toast } from "sonner";

export default function ProjectFilesPage() {
  const params = useParams();
  const projectId = Number(params.id);

  const {
    data: rawImages,
    isLoading: imagesLoading,
    refetch: refetchImages,
  } = useProjectImages(projectId);

  const { data: rawDocuments, isLoading: documentsLoading } =
    useProjectDocuments(projectId);

  const images = Array.isArray(rawImages) ? rawImages : [];
  const documents = Array.isArray(rawDocuments) ? rawDocuments : [];

  const deleteImageMutation = useDeleteImage();
  const deleteDocumentMutation = useDeleteDocument();

  async function handleDeleteImage(imageId: number) {
    try {
      await deleteImageMutation.mutateAsync(imageId);
      toast.success("Imagen eliminada");
    } catch {
      toast.error("Error al eliminar la imagen");
    }
  }

  async function handleDeleteDocument(documentId: number) {
    try {
      await deleteDocumentMutation.mutateAsync(documentId);
      toast.success("Documento eliminado");
    } catch {
      toast.error("Error al eliminar el documento");
    }
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          size="icon"
          nativeButton={false}
          render={<Link href={`/projects/${projectId}`} />}
        >
          <ArrowLeft className="size-4" />
        </Button>
        <h1 className="text-2xl font-bold tracking-tight">
          Archivos del Proyecto
        </h1>
      </div>

      <Tabs defaultValue="images">
        <TabsList>
          <TabsTrigger value="images">
            <ImageIcon className="size-4" />
            Imágenes
          </TabsTrigger>
          <TabsTrigger value="documents">
            <FileText className="size-4" />
            Documentos
          </TabsTrigger>
        </TabsList>

        <TabsContent value="images" className="space-y-6 pt-4">
          <ImageUploader
            projectId={projectId}
            onSuccess={() => refetchImages()}
          />
          <Separator />
          <ImageGallery
            images={images}
            isLoading={imagesLoading}
            onDelete={handleDeleteImage}
          />
        </TabsContent>

        <TabsContent value="documents" className="pt-4">
          <DocumentList
            projectId={projectId}
            documents={documents}
            isLoading={documentsLoading}
            onDelete={handleDeleteDocument}
          />
        </TabsContent>
      </Tabs>
    </div>
  );
}
