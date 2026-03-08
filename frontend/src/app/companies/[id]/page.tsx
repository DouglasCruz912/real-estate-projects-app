"use client"

import Link from "next/link"
import { useParams, useRouter } from "next/navigation"
import { useCompany } from "@/hooks/useCompanies"
import { CompanyForm } from "@/components/companies/CompanyForm"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { ArrowLeft } from "lucide-react"

function EditCompanySkeleton() {
  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div className="flex items-center gap-4">
        <Skeleton className="size-8 rounded-lg" />
        <Skeleton className="h-8 w-48" />
      </div>
      <Card>
        <CardHeader>
          <Skeleton className="h-5 w-52" />
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="space-y-1.5">
                <Skeleton className="h-4 w-20" />
                <Skeleton className="h-8 w-full" />
              </div>
            ))}
          </div>
          <div className="space-y-1.5">
            <Skeleton className="h-4 w-20" />
            <Skeleton className="h-16 w-full" />
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default function EditCompanyPage() {
  const params = useParams()
  const router = useRouter()
  const id = Number(params.id)
  const { data: company, isLoading } = useCompany(id)

  if (isLoading) {
    return <EditCompanySkeleton />
  }

  if (!company) {
    return (
      <div className="flex flex-col items-center justify-center gap-4 py-16 text-muted-foreground">
        <p className="text-lg font-medium">Inmobiliaria no encontrada</p>
        <Button variant="outline" render={<Link href="/companies" />}>
          <ArrowLeft className="size-4" />
          Volver al listado
        </Button>
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" render={<Link href="/companies" />}>
          <ArrowLeft />
        </Button>
        <h1 className="text-2xl font-bold tracking-tight">
          Editar Inmobiliaria
        </h1>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Datos de la Inmobiliaria</CardTitle>
        </CardHeader>
        <CardContent>
          <CompanyForm
            company={company}
            onSuccess={() => router.push("/companies")}
          />
        </CardContent>
      </Card>
    </div>
  )
}
