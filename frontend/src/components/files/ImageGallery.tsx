"use client";

import { useState } from "react";
import type { ProjectImage } from "@/types/file";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
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
import { Star, X, ImageIcon } from "lucide-react";

interface ImageGalleryProps {
  images: ProjectImage[];
  isLoading: boolean;
  onDelete: (id: number) => void;
}

export function ImageGallery({
  images,
  isLoading,
  onDelete,
}: ImageGalleryProps) {
  const [failedUrls, setFailedUrls] = useState<Set<string>>(new Set());

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="aspect-[4/3] w-full rounded-lg" />
        ))}
      </div>
    );
  }

  if (images.length === 0) {
    return (
      <div className="flex flex-col items-center gap-3 py-16 text-muted-foreground">
        <ImageIcon className="size-12" />
        <p className="text-sm">No hay imágenes</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {images.map((image) => (
        <div
          key={image.id}
          className="group relative overflow-hidden rounded-lg border bg-muted/30"
        >
          <div className="relative aspect-[4/3]">
            {!failedUrls.has(image.url) ? (
              <img
                src={image.url}
                alt={image.alt_text || image.filename}
                className="size-full object-cover"
                onError={() =>
                  setFailedUrls((prev) => new Set(prev).add(image.url))
                }
              />
            ) : (
              <div className="flex size-full items-center justify-center bg-muted">
                <ImageIcon className="size-10 text-muted-foreground" />
              </div>
            )}
            {image.is_featured && (
              <div className="absolute top-2 left-2">
                <Star className="size-5 fill-yellow-400 text-yellow-400 drop-shadow" />
              </div>
            )}
          </div>

          <div className="flex items-center justify-between gap-2 p-3">
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-medium">{image.filename}</p>
            </div>
            <div className="flex shrink-0 items-center gap-2">
              <Badge variant="secondary">{image.image_type}</Badge>
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
                  <X className="size-3.5" />
                </AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>Eliminar imagen</AlertDialogTitle>
                    <AlertDialogDescription>
                      ¿Estás seguro de que deseas eliminar &quot;{image.filename}&quot;?
                      Esta acción no se puede deshacer.
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel>Cancelar</AlertDialogCancel>
                    <AlertDialogAction
                      variant="destructive"
                      onClick={() => onDelete(image.id)}
                    >
                      Eliminar
                    </AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
