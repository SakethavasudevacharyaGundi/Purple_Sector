import { useState, useRef, useEffect } from "react"
import { useLocation, useNavigate } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { StatCard } from "@/components/StatCard"
import { ArrowLeft, Loader2, Activity, Target, Trophy } from "lucide-react"
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, Cell
} from 'recharts'
import { cn } from "@/lib/utils"

import { fetchRecommendations } from "@/lib/api"

export function Recommendation() {
  const location = useLocation()
  const navigate = useNavigate()
  const resultsRef = useRef<HTMLDivElement>(null)
  
  const stateData = location.state || {}
  const raceState = stateData.raceState
  const driverCode = stateData.driverCode || "UNK"
  
  // Temporary mapping to match driver acronym to number
  const DRIVER_MAP: Record<string, string> = {
    "NOR": "4", "VER": "1", "HAM": "44", "LEC": "16", "SAI": "55", 
    "RUS": "63", "PIA": "81", "PER": "11", "ALO": "14", "STR": "18"
  }
  
  const driverNum = DRIVER_MAP[driverCode] || "4"
  const driverState = raceState?.drivers?.find((d: any) => d.driver_number === driverNum)

  const displayData = {
    season: raceState?.season || "2024",
    gp: raceState?.event_name || "Unknown GP",
    driver: driverCode,
    lap: raceState?.lap_number || "37",
    currentCompound: driverState?.current_compound || "Medium",
    tyreAge: driverState?.current_tyre_age || 12,
    position: driverState?.position ? `P${driverState.position}` : "P4",
    gapToFront: driverState?.gap_ahead ? `+${driverState.gap_ahead.toFixed(1)}s` : "+1.4s"
  }

  const [isSimulating, setIsSimulating] = useState(true)
  const [loadingPhase, setLoadingPhase] = useState(0)
  const [strategies, setStrategies] = useState<any[]>([])
  const [selectedStrategy, setSelectedStrategy] = useState<any>(null)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

  useEffect(() => {
    // Cosmetic phase change for UI immersion
    const timer1 = setTimeout(() => {
      setLoadingPhase(1)
    }, 2000)
    
    // Fetch real data
    if (raceState && driverState) {
      setErrorMessage(null)
      fetchRecommendations(raceState, driverState)
        .then(data => {
          setStrategies(data)
          if (data.length > 0) {
            setSelectedStrategy(data[0])
          } else {
            setErrorMessage("No viable strategies found for this driver at this lap.")
          }
          setIsSimulating(false)
        })
        .catch(err => {
          console.error("Failed to fetch recommendations:", err)
          setErrorMessage(err.message || "An error occurred while generating recommendations.")
          setIsSimulating(false)
        })
    } else {
      setErrorMessage("Invalid race state provided. Please configure the race setup again.")
      setIsSimulating(false)
    }
    
    return () => clearTimeout(timer1)
  }, [raceState, driverState])

  if (isSimulating) {
    return (
      <div className="w-full min-h-[calc(100vh-8rem)] flex flex-col items-center justify-center space-y-6">
        <Loader2 className="w-12 h-12 text-purple-600 dark:text-purple-500 animate-spin" />
        <div className="text-center space-y-2 relative h-16 w-full">
          <div className={cn(
            "absolute inset-0 flex flex-col items-center justify-start transition-all duration-500",
            loadingPhase === 0 ? "opacity-100 translate-y-0" : "opacity-0 -translate-y-4"
          )}>
            <h2 className="text-2xl font-bold text-foreground tracking-widest uppercase">Analyzing Race Conditions</h2>
            <p className="text-muted-foreground">Processing track variables...</p>
          </div>
          <div className={cn(
            "absolute inset-0 flex flex-col items-center justify-start transition-all duration-500",
            loadingPhase === 1 ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4 pointer-events-none"
          )}>
            <h2 className="text-2xl font-bold text-foreground tracking-widest uppercase">Calculating Probabilities</h2>
            <p className="text-muted-foreground">Running Monte Carlo Simulations...</p>
          </div>
        </div>
      </div>
    )
  }

  if (errorMessage) {
    return (
      <div className="w-full min-h-[calc(100vh-8rem)] flex items-center justify-center p-6">
        <div className="bg-red-500/10 border border-red-500/30 rounded-2xl p-8 max-w-lg text-center space-y-4 shadow-[0_0_40px_rgba(239,68,68,0.1)]">
          <Target className="w-12 h-12 text-red-500 mx-auto" />
          <h2 className="text-2xl font-bold text-foreground">Simulation Failed</h2>
          <p className="text-muted-foreground">{errorMessage}</p>
          <Button 
            onClick={() => navigate('/dashboard')}
            className="mt-4 bg-red-600 hover:bg-red-700 text-white"
          >
            Return to Dashboard
          </Button>
        </div>
      </div>
    )
  }

  if (!strategies.length || !selectedStrategy) {
    return (
      <div className="w-full min-h-[calc(100vh-8rem)] flex items-center justify-center">
        <p className="text-muted-foreground text-lg">No strategies found or invalid race state.</p>
      </div>
    )
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-500 w-full max-w-6xl mx-auto pb-24">
      
      {/* Header and Back navigation */}
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => navigate(-1)} className="rounded-full bg-slate-200/50 dark:bg-white/5 hover:bg-slate-300 dark:hover:bg-white/10 shrink-0">
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-foreground flex items-center gap-3">
              Strategy Recommendations <Trophy className="w-6 h-6 text-yellow-600 dark:text-yellow-500" />
            </h1>
            <p className="text-muted-foreground mt-1">Optimal race strategies based on deep probabilistic analysis.</p>
          </div>
        </div>
        <Button 
          onClick={() => navigate('/dashboard')}
          variant="outline"
          className="hidden md:flex bg-purple-500/10 border-purple-500/30 text-purple-600 dark:text-purple-400 hover:bg-purple-500/20"
        >
          <Target className="w-4 h-4 mr-2" />
          Configure Race Setup
        </Button>
      </div>

      {/* Current Race State Summary - Tech Style */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {[
          { label: "Event", value: `${displayData.season} ${displayData.gp}` },
          { label: "Driver", value: displayData.driver },
          { label: "Lap", value: displayData.lap },
          { label: "Position", value: `${displayData.position} (${displayData.gapToFront})` },
          { label: "Current Tyre", value: displayData.currentCompound, color: "text-yellow-600 dark:text-yellow-400" },
          { label: "Tyre Age", value: `${displayData.tyreAge} Laps` },
        ].map((stat, i) => (
          <div key={i} className="bg-card border border-border rounded-2xl p-4 flex flex-col justify-center">
            <span className="text-xs text-muted-foreground uppercase tracking-wider mb-1 font-semibold">{stat.label}</span>
            <span className={cn("font-mono font-bold text-lg text-foreground", stat.color)}>{stat.value}</span>
          </div>
        ))}
      </div>

      {/* Top 3 Strategies */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {strategies.map((strategy) => {
          const isSelected = selectedStrategy.rank === strategy.rank
          return (
              <div 
              key={strategy.rank}
              onClick={() => setSelectedStrategy(strategy)}
              className={cn(
                "relative bg-card border rounded-3xl p-6 cursor-pointer transition-all duration-300 overflow-hidden group",
                isSelected 
                  ? `${strategy.borderColor} shadow-[0_0_30px_rgba(0,0,0,0.1)] dark:shadow-[0_0_30px_rgba(0,0,0,0.5)] scale-[1.02]` 
                  : "border-border hover:border-slate-300 dark:hover:border-white/20 hover:bg-slate-50 dark:hover:bg-[#151515]"
              )}
            >
              {isSelected && (
                <div className={cn("absolute inset-0 opacity-10 dark:opacity-5 pointer-events-none", strategy.color)} />
              )}
              
              <div className="flex justify-between items-start mb-6">
                <div className={cn("w-10 h-10 rounded-full flex items-center justify-center font-black text-lg bg-slate-100 dark:bg-[#000]", strategy.textColor)}>
                  #{strategy.rank}
                </div>
                <div className="text-right">
                  <p className="text-xs text-muted-foreground uppercase font-bold tracking-widest">Expected</p>
                  <p className="text-2xl font-black text-foreground">{strategy.expectedFinish}</p>
                </div>
              </div>

              <div className="space-y-4 relative z-10">
                <div className="flex justify-between items-center border-b border-border pb-2">
                  <span className="text-sm text-muted-foreground font-medium uppercase tracking-wider">Pit Lap</span>
                  <span className="font-mono text-xl font-bold text-foreground">Lap {strategy.pitLap}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground font-medium uppercase tracking-wider">Compound</span>
                  <span className={cn("font-mono text-xl font-bold", strategy.textColor)}>{strategy.compound}</span>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Detailed Analysis for Selected Strategy */}
      <div 
        ref={resultsRef}
        className="space-y-12 pt-6 animate-in slide-in-from-bottom-8 duration-700"
      >
        <div className="flex items-center gap-4">
          <div className="h-px flex-1 bg-gradient-to-r from-transparent via-slate-300 dark:via-white/10 to-transparent" />
          <span className="text-xs font-bold text-muted-foreground uppercase tracking-widest">Analysis for Strategy #{selectedStrategy.rank}</span>
          <div className="h-px flex-1 bg-gradient-to-r from-transparent via-slate-300 dark:via-white/10 to-transparent" />
        </div>

        {/* Time Losses */}
        <div className="space-y-6">
          <div className="flex items-center gap-3">
            <Activity className="w-6 h-6 text-emerald-600 dark:text-emerald-400" />
            <h2 className="text-2xl font-bold text-foreground tracking-tight">Time Loss Projection</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-card border border-border rounded-2xl p-5 flex flex-col justify-between h-full hover:bg-slate-50 dark:hover:bg-white/[0.02] transition-colors">
              <span className="text-sm font-semibold text-muted-foreground uppercase tracking-widest">Pit Stop Loss</span>
              <span className="font-mono text-red-500 dark:text-red-400 font-bold text-3xl mt-2">{selectedStrategy.pitLoss}</span>
            </div>
            <div className="bg-card border border-border rounded-2xl p-5 flex flex-col justify-between h-full hover:bg-slate-50 dark:hover:bg-white/[0.02] transition-colors">
              <span className="text-sm font-semibold text-muted-foreground uppercase tracking-widest">Traffic Delay</span>
              <span className="font-mono text-yellow-600 dark:text-yellow-400 font-bold text-3xl mt-2">{selectedStrategy.trafficLoss}</span>
            </div>
            <div className="bg-card border border-border rounded-2xl p-5 flex flex-col justify-between h-full hover:bg-slate-50 dark:hover:bg-white/[0.02] transition-colors">
              <span className="text-sm font-semibold text-muted-foreground uppercase tracking-widest">Tyre Degradation</span>
              <span className="font-mono text-emerald-600 dark:text-emerald-400 font-bold text-3xl mt-2">{selectedStrategy.degLoss}</span>
            </div>
          </div>
        </div>

        {/* Monte Carlo Results */}
        <div className="space-y-6">
          <div className="flex items-center gap-3">
            <Target className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            <h2 className="text-2xl font-bold text-foreground tracking-tight">Monte Carlo Stochastic Analysis</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-card border border-border rounded-2xl p-6 flex flex-col justify-center items-center text-center space-y-2">
              <p className="text-sm font-semibold text-muted-foreground uppercase tracking-widest">Win Probability</p>
              <p className="text-5xl font-black text-foreground">{selectedStrategy.winProb}%</p>
            </div>
            <div className="bg-card border border-border rounded-2xl p-6 flex flex-col justify-center items-center text-center space-y-2 relative overflow-hidden">
              <div className={cn("absolute inset-0 opacity-5 dark:opacity-10", selectedStrategy.color)} />
              <p className="text-sm font-semibold text-muted-foreground uppercase tracking-widest relative z-10">Podium Probability</p>
              <p className={cn("text-5xl font-black relative z-10", selectedStrategy.textColor)}>{selectedStrategy.podiumProb}%</p>
            </div>
            <div className="bg-card border border-border rounded-2xl p-6 flex flex-col justify-center items-center text-center space-y-2">
              <p className="text-sm font-semibold text-muted-foreground uppercase tracking-widest">Points Probability</p>
              <p className="text-5xl font-black text-emerald-600 dark:text-emerald-400">{selectedStrategy.pointsProb}%</p>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="bg-card border border-border rounded-3xl p-6 lg:col-span-2">
              <p className="text-sm font-bold text-muted-foreground uppercase tracking-widest mb-6">Position Probability Distribution</p>
              <div className="w-full h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={selectedStrategy.distribution} layout="vertical" margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" horizontal={false} />
                    <XAxis type="number" stroke="#666" tick={{fill: '#888'}} tickLine={false} axisLine={false} tickFormatter={(val) => `${val}%`} />
                    <YAxis type="category" dataKey="position" stroke="#666" tick={{fill: '#fff', fontWeight: 'bold'}} tickLine={false} axisLine={false} />
                    <RechartsTooltip 
                      cursor={{fill: '#ffffff05'}}
                      contentStyle={{ backgroundColor: '#111', borderColor: '#333', borderRadius: '8px' }}
                      itemStyle={{ color: '#fff', fontWeight: 'bold' }}
                      formatter={(value: any) => [`${value}%`, 'Probability']}
                    />
                    <Bar dataKey="probability" radius={[0, 4, 4, 0]}>
                      {selectedStrategy.distribution.map((_entry: any, index: number) => (
                        <Cell key={`cell-${index}`} fill={index < 3 ? (selectedStrategy.rank === 1 ? '#a855f7' : selectedStrategy.rank === 2 ? '#f43f5e' : '#3b82f6') : '#333333'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="space-y-6">
              <StatCard title="Expected Finish" value={selectedStrategy.expectedFinish} />
              <StatCard title="Median Position" value={selectedStrategy.expectedFinish.replace('P', '')} />
              <StatCard title="Standard Deviation" value="1.8" subtitle="Positions" />
            </div>
          </div>
        </div>

      </div>
    </div>
  )
}
