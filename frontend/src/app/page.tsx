"use client";

import Link from "next/link";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Building2,
  FolderKanban,
  Package,
  TrendingUp,
  Plus,
  ArrowRight,
} from "lucide-react";
import { useCompanies } from "@/hooks/useCompanies";
import { useProjects } from "@/hooks/useProjects";

export default function DashboardPage() {
  const { data: companies, isLoading: loadingCompanies } = useCompanies({
    limit: 1,
  });
  const { data: projectsData, isLoading: loadingProjects } = useProjects({
    limit: 100,
  });

  const totalCompanies = Array.isArray(companies) ? companies.length : 0;

  const projects = projectsData?.projects ?? (Array.isArray(projectsData) ? projectsData : []);
  const totalProjects = projectsData?.total ?? projects.length;
  const activeProjects = projects.filter(
    (p) => p.is_active && p.state !== "cancelled" && p.state !== "completed"
  ).length;

  const stats = [
    {
      title: "Inmobiliarias",
      value: loadingCompanies ? null : totalCompanies.toString(),
      description: "Empresas registradas",
      icon: Building2,
      href: "/companies",
      color: "text-blue-600",
      bg: "bg-blue-50",
    },
    {
      title: "Proyectos Activos",
      value: loadingProjects ? null : activeProjects.toString(),
      description: `${totalProjects} proyectos en total`,
      icon: FolderKanban,
      href: "/projects",
      color: "text-emerald-600",
      bg: "bg-emerald-50",
    },
    {
      title: "Total Proyectos",
      value: loadingProjects ? null : totalProjects.toString(),
      description: "En la plataforma",
      icon: Package,
      href: "/projects",
      color: "text-violet-600",
      bg: "bg-violet-50",
    },
    {
      title: "En Venta",
      value: loadingProjects
        ? null
        : projects
            .filter((p) => p.state === "sale" || p.state === "pre_sale")
            .length.toString(),
      description: "Proyectos en preventa/venta",
      icon: TrendingUp,
      href: "/projects?state=sale",
      color: "text-amber-600",
      bg: "bg-amber-50",
    },
  ];

  const quickActions = [
    {
      title: "Nueva Inmobiliaria",
      description: "Registrar una empresa inmobiliaria",
      href: "/companies/new",
      icon: Building2,
    },
    {
      title: "Nuevo Proyecto",
      description: "Crear un proyecto inmobiliario",
      href: "/projects/new",
      icon: FolderKanban,
    },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Dashboard</h1>
        <p className="text-sm text-muted-foreground">
          Resumen general de la plataforma
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Link key={stat.title} href={stat.href}>
            <Card className="transition-shadow hover:shadow-md cursor-pointer">
              <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-sm font-medium text-muted-foreground">
                    {stat.title}
                  </CardTitle>
                  <div className={`rounded-lg p-2 ${stat.bg}`}>
                    <stat.icon className={`size-4 ${stat.color}`} />
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {stat.value === null ? (
                  <Skeleton className="h-8 w-16" />
                ) : (
                  <p className="text-3xl font-bold">{stat.value}</p>
                )}
                <CardDescription className="mt-1">
                  {stat.description}
                </CardDescription>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>

      <div>
        <h2 className="text-lg font-semibold mb-4">Accesos Rápidos</h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {quickActions.map((action) => (
            <Link key={action.title} href={action.href}>
              <Card className="transition-all hover:shadow-md hover:border-primary/20 cursor-pointer group">
                <CardContent className="flex items-center gap-4 p-6">
                  <div className="rounded-lg bg-primary/10 p-3">
                    <action.icon className="size-5 text-primary" />
                  </div>
                  <div className="flex-1">
                    <p className="font-medium">{action.title}</p>
                    <p className="text-sm text-muted-foreground">
                      {action.description}
                    </p>
                  </div>
                  <ArrowRight className="size-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
                </CardContent>
              </Card>
            </Link>
          ))}

          <Link href="/projects">
            <Card className="transition-all hover:shadow-md hover:border-primary/20 cursor-pointer group">
              <CardContent className="flex items-center gap-4 p-6">
                <div className="rounded-lg bg-primary/10 p-3">
                  <Package className="size-5 text-primary" />
                </div>
                <div className="flex-1">
                  <p className="font-medium">Gestionar Stock</p>
                  <p className="text-sm text-muted-foreground">
                    Selecciona un proyecto para ver su stock
                  </p>
                </div>
                <ArrowRight className="size-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
              </CardContent>
            </Card>
          </Link>
        </div>
      </div>

      {!loadingProjects && projects.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold">Proyectos Recientes</h2>
            <Link href="/projects">
              <Button variant="ghost" size="sm">
                Ver todos <ArrowRight className="ml-1 size-4" />
              </Button>
            </Link>
          </div>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {projects.slice(0, 6).map((project) => (
              <Link key={project.id} href={`/projects/${project.id}`}>
                <Card className="transition-shadow hover:shadow-md cursor-pointer">
                  <CardHeader className="pb-2">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-sm font-medium truncate">
                        {project.name}
                      </CardTitle>
                      <span
                        className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${
                          project.state === "sale" || project.state === "pre_sale"
                            ? "bg-green-100 text-green-700"
                            : project.state === "construction"
                            ? "bg-orange-100 text-orange-700"
                            : project.state === "delivered" || project.state === "completed"
                            ? "bg-purple-100 text-purple-700"
                            : project.state === "cancelled"
                            ? "bg-red-100 text-red-700"
                            : "bg-gray-100 text-gray-700"
                        }`}
                      >
                        {project.state}
                      </span>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground">
                      {[project.city, project.region]
                        .filter(Boolean)
                        .join(", ") || "Sin ubicación"}
                    </p>
                    {project.price_from && (
                      <p className="text-sm font-medium mt-1">
                        Desde {project.price_from.toLocaleString()}{" "}
                        {project.currency}
                      </p>
                    )}
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
