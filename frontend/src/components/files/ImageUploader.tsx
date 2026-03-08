"use client";

import { useState, useRef, useCallback } from "react";
import { useUploadImages } from "@/hooks/useFiles";
import { IMAGE_TYPES } from "@/lib/constants";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Upload, X, Loader2 } from "lucide-react";
import { toast } from "sonner";

interface ImageUploaderProps {
  projectId: number;
  onSuccess: () => void;
}

export function ImageUploader({ projectId, onSuccess }: ImageUploaderProps) {
  const [files, setFiles] = useState<File[]>([]);
  const [previews, setPreviews] = useState<string[]>([]);
  const [imageType, setImageType] = useState("general");
  const [altText, setAltText] = useState("");
  const [isFeatured, setIsFeatured] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const uploadMutation = useUploadImages();

  const addFiles = useCallback((incoming: File[]) => {
    const imageFiles = incoming.filter((f) => f.type.startsWith("image/"));
    if (imageFiles.length === 0) return;

    setFiles((prev) => [...prev, ...imageFiles]);

    const newPreviews = imageFiles.map((f) => URL.createObjectURL(f));
    setPreviews((prev) => [...prev, ...newPreviews]);
  }, []);

  const removeFile = useCallback(
    (index: number) => {
      URL.revokeObjectURL(previews[index]);
      setFiles((prev) => prev.filter((_, i) => i !== index));
      setPreviews((prev) => prev.filter((_, i) => i !== index));
    },
    [previews]
  );

  const clearAll = useCallback(() => {
    previews.forEach((p) => URL.revokeObjectURL(p));
    setFiles([]);
    setPreviews([]);
    setAltText("");
    setIsFeatured(false);
    setImageType("general");
  }, [previews]);

  function handleDragOver(e: React.DragEvent) {
    e.preventDefault();
    setIsDragOver(true);
  }

  function handleDragLeave(e: React.DragEvent) {
    e.preventDefault();
    setIsDragOver(false);
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setIsDragOver(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    addFiles(droppedFiles);
  }

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    if (e.target.files) {
      addFiles(Array.from(e.target.files));
      e.target.value = "";
    }
  }

  async function handleUpload() {
    if (files.length === 0) return;

    try {
      await uploadMutation.mutateAsync({
        projectId,
        files,
        opts: {
          image_type: imageType,
          alt_text: altText || undefined,
          is_featured: isFeatured,
        },
      });
      toast.success("Imágenes subidas correctamente");
      clearAll();
      onSuccess();
    } catch {
      toast.error("Error al subir las imágenes");
    }
  }

  return (
    <div className="space-y-4">
      <div
        role="button"
        tabIndex={0}
        onClick={() => inputRef.current?.click()}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") inputRef.current?.click();
        }}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={cn(
          "flex cursor-pointer flex-col items-center justify-center gap-2 rounded-lg border-2 border-dashed p-8 text-center transition-colors",
          isDragOver
            ? "border-primary bg-primary/5"
            : "border-muted-foreground/25 hover:border-muted-foreground/50"
        )}
      >
        <Upload className="size-8 text-muted-foreground" />
        <p className="text-sm text-muted-foreground">
          Arrastra imágenes o haz clic para seleccionar
        </p>
        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          multiple
          className="hidden"
          onChange={handleFileChange}
        />
      </div>

      {previews.length > 0 && (
        <div className="grid grid-cols-3 gap-3 sm:grid-cols-4 md:grid-cols-6">
          {previews.map((src, i) => (
            <div key={src} className="group relative aspect-square">
              <img
                src={src}
                alt={files[i]?.name}
                className="size-full rounded-md object-cover"
              />
              <button
                type="button"
                onClick={() => removeFile(i)}
                className="absolute -top-1.5 -right-1.5 flex size-5 items-center justify-center rounded-full bg-destructive text-destructive-foreground opacity-0 transition-opacity group-hover:opacity-100"
              >
                <X className="size-3" />
              </button>
              <p className="absolute inset-x-0 bottom-0 truncate rounded-b-md bg-black/60 px-1 py-0.5 text-[10px] text-white">
                {files[i]?.name}
              </p>
            </div>
          ))}
        </div>
      )}

      {files.length > 0 && (
        <div className="flex flex-wrap items-end gap-4">
          <div className="space-y-1">
            <Label className="text-xs">Tipo de imagen</Label>
            <Select value={imageType} onValueChange={(v) => setImageType(v ?? "general")}>
              <SelectTrigger className="w-[160px]">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {IMAGE_TYPES.map((t) => (
                  <SelectItem key={t.value} value={t.value}>
                    {t.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-1">
            <Label className="text-xs">Texto alternativo</Label>
            <Input
              placeholder="Descripción de la imagen"
              className="w-[200px]"
              value={altText}
              onChange={(e) => setAltText(e.target.value)}
            />
          </div>

          <div className="flex items-center gap-2 pb-0.5">
            <Switch
              checked={isFeatured}
              onCheckedChange={setIsFeatured}
            />
            <Label className="text-xs">Destacada</Label>
          </div>

          <Button
            onClick={handleUpload}
            disabled={uploadMutation.isPending}
          >
            {uploadMutation.isPending ? (
              <Loader2 className="size-4 animate-spin" />
            ) : (
              <Upload className="size-4" />
            )}
            Subir Imágenes
          </Button>
        </div>
      )}
    </div>
  );
}
