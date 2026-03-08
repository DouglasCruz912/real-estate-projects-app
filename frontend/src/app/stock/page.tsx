"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Package, ArrowRight } from "lucide-react";

export default function StockPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center p-6">
      <Package className="size-16 mb-6 text-muted-foreground opacity-40" />
      <h1 className="text-2xl font-bold tracking-tight mb-2">
        Stock de Unidades
      </h1>
      <p className="text-muted-foreground mb-6 max-w-md">
        Selecciona un proyecto para ver y gestionar su stock de unidades.
      </p>
      <Button nativeButton={false} render={<Link href="/projects" />}>
        <ArrowRight className="size-4" />
        Ir a Proyectos
      </Button>
    </div>
  );
}
