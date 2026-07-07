import { useEffect, useState } from "react"
import { Trophy, TrendingUp, TrendingDown, Minus, Loader2 } from "lucide-react"
import { fetchElo } from "@/lib/api"

export function EloRanking() {
  const [drivers, setDrivers] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchElo()
      .then(data => {
        setDrivers(data)
        setLoading(false)
      })
      .catch(err => {
        console.error("Failed to fetch ELO:", err)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="w-full min-h-[50vh] flex items-center justify-center">
        <Loader2 className="w-10 h-10 animate-spin text-purple-600" />
      </div>
    )
  }
  return (
    <div className="w-full max-w-5xl mx-auto py-12 px-6 animate-in fade-in duration-1000">
      <div className="flex items-center gap-4 mb-8">
        <div className="w-12 h-12 rounded-2xl bg-purple-500/20 flex items-center justify-center border border-purple-500/30">
          <Trophy className="w-6 h-6 text-purple-400" />
        </div>
        <div>
          <h1 className="text-4xl font-bold tracking-tight text-foreground">Driver Elo Rankings</h1>
          <p className="text-muted-foreground mt-1">Current dynamic performance ratings across the grid</p>
        </div>
      </div>

      <div className="bg-card/80 backdrop-blur-xl border border-border rounded-3xl overflow-hidden shadow-2xl">
        <div className="grid grid-cols-12 gap-4 p-6 border-b border-border text-sm font-semibold text-muted-foreground uppercase tracking-widest">
          <div className="col-span-1 text-center">Rank</div>
          <div className="col-span-4">Driver</div>
          <div className="col-span-4">Team</div>
          <div className="col-span-2 text-right">Elo Score</div>
          <div className="col-span-1 text-center">Trend</div>
        </div>

        <div className="divide-y divide-border">
          {drivers.map((driver, index) => (
            <div 
              key={driver.id}
              className="grid grid-cols-12 gap-4 p-6 items-center hover:bg-slate-100 dark:hover:bg-white/[0.02] transition-colors"
            >
              <div className="col-span-1 text-center font-mono text-lg text-muted-foreground">
                {index + 1}
              </div>
              <div className="col-span-4 font-bold text-foreground text-lg flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-slate-200 dark:bg-white/10 flex items-center justify-center text-xs text-muted-foreground font-mono">
                  {driver.id}
                </div>
                {driver.name}
              </div>
              <div className="col-span-4 text-muted-foreground">
                {driver.team}
              </div>
              <div className="col-span-2 text-right font-mono text-xl font-bold text-purple-600 dark:text-purple-400">
                {driver.elo}
              </div>
              <div className="col-span-1 flex justify-center">
                {driver.trend === 'up' && <TrendingUp className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />}
                {driver.trend === 'down' && <TrendingDown className="w-5 h-5 text-rose-600 dark:text-rose-400" />}
                {driver.trend === 'same' && <Minus className="w-5 h-5 text-slate-400 dark:text-slate-500" />}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
