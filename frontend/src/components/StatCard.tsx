import { Card, CardContent } from "@/components/ui/card"

interface StatCardProps {
  title: string
  value: string | number
  subtitle?: string
}

export function StatCard({ title, value, subtitle }: StatCardProps) {
  return (
    <Card className="bg-[#1D1D1D] border-border/50">
      <CardContent className="p-6 flex flex-col justify-between h-full">
        <p className="text-sm font-medium text-muted-foreground">{title}</p>
        <div className="mt-4">
          <p className="text-4xl font-bold tracking-tight">{value}</p>
          {subtitle && (
            <p className="mt-1 text-sm text-muted-foreground">{subtitle}</p>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
