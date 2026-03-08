"use client"

import Link from "next/link"
import { useRouter } from "next/navigation"
import { CompanyForm } from "@/components/companies/CompanyForm"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowLeft } from "lucide-react"

export default function NewCompanyPage() {
  const router = useRouter()

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" render={<Link href="/companies" />}>
          <ArrowLeft />
        </Button>
        <h1 className="text-2xl font-bold tracking-tight">
          Nueva Inmobiliaria
        </h1>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Datos de la Inmobiliaria</CardTitle>
        </CardHeader>
        <CardContent>
          <CompanyForm onSuccess={() => router.push("/companies")} />
        </CardContent>
      </Card>
    </div>
  )
}
