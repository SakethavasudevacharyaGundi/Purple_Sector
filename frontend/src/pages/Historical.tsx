import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Slider } from "@/components/ui/slider"
import { Play, SkipBack, SkipForward } from "lucide-react"
import { Button } from "@/components/ui/button"

export function Historical() {
  const [lap, setLap] = useState(34)
  const maxLaps = 78

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Historical Replay</h1>
          <p className="text-muted-foreground mt-2 text-lg text-primary">2023 Monaco GP</p>
        </div>
      </div>

      <Card className="bg-card border-border">
        <CardContent className="p-8 space-y-8">
          
          <div className="flex items-center gap-6">
            <span className="font-mono text-muted-foreground whitespace-nowrap">Lap 1</span>
            <Slider 
              value={[lap]} 
              onValueChange={(val) => setLap(val[0])} 
              max={maxLaps} 
              min={1} 
              step={1} 
              className="flex-1" 
            />
            <span className="font-mono text-muted-foreground whitespace-nowrap">Lap {maxLaps}</span>
          </div>

          <div className="flex justify-center items-center gap-4">
            <Button variant="outline" size="icon" className="bg-slate-100 dark:bg-[#111111] border-border rounded-full h-12 w-12 hover:bg-slate-200 dark:hover:bg-[#2a2a2a]">
              <SkipBack className="h-5 w-5" />
            </Button>
            <Button size="icon" className="bg-primary hover:bg-primary/90 text-primary-foreground rounded-full h-16 w-16 shadow-lg shadow-primary/20">
              <Play className="h-6 w-6 ml-1" />
            </Button>
            <Button variant="outline" size="icon" className="bg-slate-100 dark:bg-[#111111] border-border rounded-full h-12 w-12 hover:bg-slate-200 dark:hover:bg-[#2a2a2a]">
              <SkipForward className="h-5 w-5" />
            </Button>
          </div>

        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="bg-card border-border">
          <CardHeader>
            <CardTitle className="text-lg flex justify-between">
              <span>Current Status</span>
              <span className="text-primary font-mono">Lap {lap}</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between items-center py-2 border-b border-border">
              <span className="text-muted-foreground">Leader</span>
              <span className="font-bold text-foreground">VER</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-border">
              <span className="text-muted-foreground">Weather</span>
              <span className="font-bold text-blue-500 dark:text-blue-400">Rain Approaching</span>
            </div>
            <div className="flex justify-between items-center py-2">
              <span className="text-muted-foreground">Track Condition</span>
              <span className="font-bold text-warning">Damp</span>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-card border-border">
          <CardHeader>
            <CardTitle className="text-lg">Key Events</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className={`p-3 rounded-md bg-slate-100 dark:bg-[#111111] border-l-4 ${lap >= 20 ? 'border-primary' : 'border-muted opacity-50'}`}>
              <span className="text-sm font-mono text-muted-foreground block mb-1">Lap 20</span>
              <span className="text-foreground font-medium">SAI pits for Hard tyres</span>
            </div>
            <div className={`p-3 rounded-md bg-slate-100 dark:bg-[#111111] border-l-4 ${lap >= 33 ? 'border-warning' : 'border-muted opacity-50'}`}>
              <span className="text-sm font-mono text-muted-foreground block mb-1">Lap 33</span>
              <span className="text-foreground font-medium">Rain reported at Turn 3</span>
            </div>
            <div className={`p-3 rounded-md bg-slate-100 dark:bg-[#111111] border-l-4 ${lap >= 54 ? 'border-blue-500' : 'border-muted opacity-50'}`}>
              <span className="text-sm font-mono text-muted-foreground block mb-1">Lap 54</span>
              <span className="text-foreground font-medium">VER pits for Inters</span>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
