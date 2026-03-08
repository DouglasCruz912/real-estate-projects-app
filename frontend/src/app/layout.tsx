import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { QueryProvider } from "@/providers/QueryProvider"
import { AppShell } from "@/components/layout/AppShell"
import { Toaster } from "@/components/ui/sonner"

const inter = Inter({
  variable: "--font-sans",
  subsets: ["latin"],
})

export const metadata: Metadata = {
  title: "Real Estate Projects",
  description: "Gestión de proyectos inmobiliarios",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="es">
      <body className={`${inter.variable} antialiased`}>
        <QueryProvider>
          <AppShell>{children}</AppShell>
          <Toaster />
        </QueryProvider>
      </body>
    </html>
  )
}
