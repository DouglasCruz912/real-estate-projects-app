"use client";

import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useProject } from "@/hooks/useProjects";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardAction,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { ProjectForm } from "@/components/projects/ProjectForm";
import { ArrowLeft, Package, FolderOpen } from "lucide-react";

export default function EditProjectPage() {
  const params = useParams();
  const router = useRouter();
  const id = Number(params.id);
  const { data: project, isLoading } = useProject(id);

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" render={<Link href="/projects" />}>
          <ArrowLeft className="size-4" />
        </Button>
        <h1 className="text-2xl font-bold tracking-tight">
          Editar Proyecto
        </h1>
        <div className="ml-auto flex gap-2">
          <Button
            variant="outline"
            size="sm"
            render={<Link href={`/projects/${id}/stock`} />}
          >
            <Package className="size-4" />
            Stock
          </Button>
          <Button
            variant="outline"
            size="sm"
            render={<Link href={`/projects/${id}/files`} />}
          >
            <FolderOpen className="size-4" />
            Archivos
          </Button>
        </div>
      </div>

      {isLoading ? (
        <Card>
          <CardHeader>
            <Skeleton className="h-6 w-48" />
          </CardHeader>
          <CardContent className="space-y-4">
            <Skeleton className="h-10 w-full" />
            <div className="grid grid-cols-2 gap-4">
              {Array.from({ length: 6 }).map((_, i) => (
                <Skeleton key={i} className="h-10 w-full" />
              ))}
            </div>
          </CardContent>
        </Card>
      ) : project ? (
        <Card>
          <CardHeader>
            <CardTitle>{project.name}</CardTitle>
            <CardAction>
              <span className="text-sm text-muted-foreground">
                ID: {project.id}
              </span>
            </CardAction>
          </CardHeader>
          <CardContent>
            <ProjectForm
              project={project}
              onSuccess={() => router.push("/projects")}
            />
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardContent className="py-12 text-center text-muted-foreground">
            Proyecto no encontrado.
          </CardContent>
        </Card>
      )}
    </div>
  );
}
