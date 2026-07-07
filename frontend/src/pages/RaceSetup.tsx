import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"

export function RaceSetup() {
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Race Setup</h1>
        <p className="text-muted-foreground mt-2">Configure initial state for simulation.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Main Configuration */}
        <Card className="bg-[#1D1D1D] border-border/50 md:col-span-2">
          <CardHeader>
            <CardTitle className="text-lg">Event Details</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-muted-foreground">Season</label>
                <Select defaultValue="2024">
                  <SelectTrigger className="bg-[#111111] border-border/50">
                    <SelectValue placeholder="Select season" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="2024">2024</SelectItem>
                    <SelectItem value="2023">2023</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-muted-foreground">Grand Prix</label>
                <Select defaultValue="british">
                  <SelectTrigger className="bg-[#111111] border-border/50">
                    <SelectValue placeholder="Select GP" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="british">British GP</SelectItem>
                    <SelectItem value="monaco">Monaco GP</SelectItem>
                    <SelectItem value="italy">Italian GP</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-muted-foreground">Driver</label>
                <Select defaultValue="norris">
                  <SelectTrigger className="bg-[#111111] border-border/50">
                    <SelectValue placeholder="Select driver" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="norris">Lando Norris</SelectItem>
                    <SelectItem value="verstappen">Max Verstappen</SelectItem>
                    <SelectItem value="hamilton">Lewis Hamilton</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-4 border-t border-border/50">
              <div className="space-y-2">
                <label className="text-sm font-medium text-muted-foreground">Current Lap</label>
                <div className="h-10 px-3 py-2 bg-[#111111] border border-border/50 rounded-md flex items-center">
                  <span className="font-mono text-lg">37</span>
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-muted-foreground">Current Position</label>
                <div className="h-10 px-3 py-2 bg-[#111111] border border-border/50 rounded-md flex items-center text-primary font-bold">
                  P4
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-muted-foreground">Tyre Compound</label>
                <Select defaultValue="medium">
                  <SelectTrigger className="bg-[#111111] border-border/50">
                    <SelectValue placeholder="Select tyre" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="soft">Soft</SelectItem>
                    <SelectItem value="medium">Medium</SelectItem>
                    <SelectItem value="hard">Hard</SelectItem>
                    <SelectItem value="inter">Inter</SelectItem>
                    <SelectItem value="wet">Wet</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-muted-foreground">Tyre Age</label>
                <div className="h-10 px-3 py-2 bg-[#111111] border border-border/50 rounded-md flex items-center justify-between">
                  <span>12 laps</span>
                  <Badge variant="outline" className="border-warning text-warning">Degraded</Badge>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Sidebar Info */}
        <div className="space-y-6">
          <Card className="bg-[#1D1D1D] border-border/50">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Gap Info</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">To Leader</span>
                <span className="font-mono text-white">+23.8s</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Car Ahead</span>
                <span className="font-mono text-warning">+1.4s</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Car Behind</span>
                <span className="font-mono text-success">-0.8s</span>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-[#1D1D1D] border-border/50">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Weather Conditions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Air Temp</span>
                <span className="font-medium text-white">24°C</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Track Temp</span>
                <span className="font-medium text-white">38°C</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Rain Probability</span>
                <span className="font-medium text-success">0%</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Track Condition</span>
                <Badge variant="outline" className="border-success text-success bg-success/10">Dry / Grippy</Badge>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
