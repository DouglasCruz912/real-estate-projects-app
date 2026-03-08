"use client";

import { useState, useRef } from "react";
import type { ProjectDocument } from "@/types/file";
import { useUploadDocument } from "@/hooks/useFiles";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import {
  Upload,
  Trash2,
  FileText,
  ExternalLink,
  Loader2,
} from "lucide-react";
import { toast } from "sonner";

interface DocumentListProps {
  projectId: number;
  documents: ProjectDocument[];
  isLoading: boolean;
  onDelete: (id: number) => void;
}

export function DocumentList({
  projectId,
  documents,
  isLoading,
  onDelete,
}: DocumentListProps) {
  const [file, setFile] = useState<File | null>(null);
  const [documentType, setDocumentType] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  const uploadMutation = useUploadDocument();

  async function handleUpload() {
    if (!file) return;

    try {
      await uploadMutation.mutateAsync({
        projectId,
        file,
        documentType: documentType || undefined,
      });
      toast.success("Documento subido correctamente");
      setFile(null);
      setDocumentType("");
      if (inputRef.current) inputRef.current.value = "";
    } catch {
      toast.error("Error al subir el documento");
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end gap-4 rounded-lg border bg-muted/30 p-4">
        <div className="space-y-1">
          <Label className="text-xs">Archivo</Label>
          <Input
            ref={inputRef}
            type="file"
            className="w-[260px]"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          />
        </div>

        <div className="space-y-1">
          <Label className="text-xs">Tipo de documento</Label>
          <Input
            placeholder="Ej: contrato, plano, escritura"
            className="w-[200px]"
            value={documentType}
            onChange={(e) => setDocumentType(e.target.value)}
          />
        </div>

        <Button
          onClick={handleUpload}
          disabled={!file || uploadMutation.isPending}
        >
          {uploadMutation.isPending ? (
            <Loader2 className="size-4 animate-spin" />
          ) : (
            <Upload className="size-4" />
          )}
          Subir Documento
        </Button>
      </div>

      {isLoading ? (
        <div className="space-y-3">
          {Array.from({ length: 4 }).map((_, i) => (
            <Skeleton key={i} className="h-12 w-full rounded-md" />
          ))}
        </div>
      ) : documents.length === 0 ? (
        <div className="flex flex-col items-center gap-3 py-16 text-muted-foreground">
          <FileText className="size-12" />
          <p className="text-sm">No hay documentos</p>
        </div>
      ) : (
        <div className="rounded-lg border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Nombre</TableHead>
                <TableHead>Tipo</TableHead>
                <TableHead>Fecha</TableHead>
                <TableHead className="w-[80px]">Acciones</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {documents.map((doc) => (
                <TableRow key={doc.id}>
                  <TableCell>
                    <a
                      href={doc.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1.5 text-sm font-medium hover:underline"
                    >
                      <FileText className="size-4 shrink-0 text-muted-foreground" />
                      {doc.filename}
                      <ExternalLink className="size-3 text-muted-foreground" />
                    </a>
                  </TableCell>
                  <TableCell>
                    {doc.document_type && (
                      <Badge variant="secondary">{doc.document_type}</Badge>
                    )}
                  </TableCell>
                  <TableCell className="text-sm text-muted-foreground">
                    {new Date(doc.created_at).toLocaleDateString("es-CL")}
                  </TableCell>
                  <TableCell>
                    <AlertDialog>
                      <AlertDialogTrigger
                        render={
                          <Button
                            variant="ghost"
                            size="icon-xs"
                            className="text-muted-foreground hover:text-destructive"
                          />
                        }
                      >
                        <Trash2 className="size-3.5" />
                      </AlertDialogTrigger>
                      <AlertDialogContent>
                        <AlertDialogHeader>
                          <AlertDialogTitle>
                            Eliminar documento
                          </AlertDialogTitle>
                          <AlertDialogDescription>
                            ¿Estás seguro de que deseas eliminar &quot;{doc.filename}
                            &quot;? Esta acción no se puede deshacer.
                          </AlertDialogDescription>
                        </AlertDialogHeader>
                        <AlertDialogFooter>
                          <AlertDialogCancel>Cancelar</AlertDialogCancel>
                          <AlertDialogAction
                            variant="destructive"
                            onClick={() => onDelete(doc.id)}
                          >
                            Eliminar
                          </AlertDialogAction>
                        </AlertDialogFooter>
                      </AlertDialogContent>
                    </AlertDialog>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  );
}
