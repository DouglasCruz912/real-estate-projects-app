"use client";

import { useRouter } from "next/navigation";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ProjectForm } from "@/components/projects/ProjectForm";
import { ArrowLeft } from "lucide-react";

export default function NewProjectPage() {
  const router = useRouter();

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" render={<Link href="/projects" />}>
          <ArrowLeft className="size-4" />
        </Button>
        <h1 className="text-2xl font-bold tracking-tight">Nuevo Proyecto</h1>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Crear proyecto</CardTitle>
        </CardHeader>
        <CardContent>
          <ProjectForm onSuccess={() => router.push("/projects")} />
        </CardContent>
      </Card>
    </div>
  );
}
