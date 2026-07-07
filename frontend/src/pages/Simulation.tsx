import { useState, useRef, useEffect } from "react"
import { useLocation, useNavigate } from "react-router-dom"

import { Slider } from "@/components/ui/slider"
import { Button } from "@/components/ui/button"
import { StatCard } from "@/components/StatCard"
import { Play, ArrowLeft, Loader2, Activity, Target } from "lucide-react"
import { 
  BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer
} from 'recharts'
import { cn } from "@/lib/utils"
import { fetchCustomSimulation } from "@/lib/api"

export function Simulation() {
  const location = useLocation()
  const navigate = useNavigate()
  const resultsRef = useRef<HTMLDivElement>(null)
  
  const stateData = location.state || {}
  const raceState = stateData.raceState
  const driverCode = stateData.driverCode || "UNK"
  
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
    lap: raceState?.lap_number || "1",
    currentCompound: driverState?.current_compound || "Medium",
    tyreAge: driverState?.current_tyre_age || 0,
    position: driverState?.position ? `P${driverState.position}` : "P4",
    gapToFront: driverState?.gap_ahead ? `+${driverState.gap_ahead.toFixed(1)}s` : "+1.4s"
  }

  const [pitLap, setPitLap] = useState([parseInt(displayData.lap) + 2])
  const [nextCompound, setNextCompound] = useState("Medium")
  const [isSimulating, setIsSimulating] = useState(false)
  const [hasSimulated, setHasSimulated] = useState(false)
  const [simulationResult, setSimulationResult] = useState<any>(null)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

  const handleSimulate = async () => {
    if (isSimulating || !raceState || !driverState) return
    setIsSimulating(true)
    setErrorMessage(null)
    setHasSimulated(false)
    
    try {
      const result = await fetchCustomSimulation(
        raceState, 
        driverState, 
        pitLap[0], 
        nextCompound
      )
      setSimulationResult(result)
      setHasSimulated(true)
    } catch (err: any) {
      console.error("Failed to run custom simulation:", err)
      setErrorMessage(err.message || "An error occurred during simulation.")
    } finally {
      setIsSimulating(false)
    }
  }

  // Smooth scroll to results once they render
  useEffect(() => {
    if (hasSimulated && resultsRef.current) {
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: "smooth", block: "start" })
      }, 100)
    }
  }, [hasSimulated])

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
              Strategy Simulation <Activity className="w-6 h-6 text-purple-600 dark:text-purple-500" />
            </h1>
            <p className="text-muted-foreground mt-1">Configure parameters and evaluate optimal pit windows and race outcomes.</p>
          </div>
        </div>
        <Button 
          onClick={() => navigate('/dashboard')}
          variant="outline"
          className="hidden md:flex bg-purple-500/10 border-purple-500/30 text-purple-400 hover:bg-purple-500/20"
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

      {errorMessage && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-2xl p-6 text-center shadow-[0_0_40px_rgba(239,68,68,0.1)]">
          <Target className="w-8 h-8 text-red-500 mx-auto mb-2" />
          <h2 className="text-lg font-bold text-foreground">Simulation Failed</h2>
          <p className="text-muted-foreground">{errorMessage}</p>
        </div>
      )}

      {/* Strategy Inputs Container */}
      <div className="bg-gradient-to-br from-slate-50 to-slate-100 dark:from-[#1A1A24] dark:to-[#111116] border border-purple-500/20 rounded-3xl p-8 shadow-[0_0_50px_rgba(168,85,247,0.05)] relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-purple-500/10 blur-[100px] pointer-events-none" />
        
        <div className="relative z-10 flex flex-col lg:flex-row gap-12 items-end">
          
          <div className="flex-1 w-full space-y-6">
            <div>
              <div className="flex justify-between items-center mb-4">
                <label className="text-sm font-bold text-muted-foreground uppercase tracking-widest">Select Pit Lap</label>
                <div className="bg-purple-500/10 dark:bg-purple-500/20 text-purple-600 dark:text-purple-300 font-mono font-bold px-4 py-1 rounded-full border border-purple-500/30">
                  Lap {pitLap[0]}
                </div>
              </div>
              <Slider 
                value={pitLap} 
                onValueChange={setPitLap} 
                max={70} 
                min={parseInt(displayData.lap)} 
                step={1} 
                className="py-2 cursor-pointer" 
              />
              <div className="flex justify-between text-xs font-mono text-muted-foreground mt-2">
                <span>Lap {displayData.lap} (Now)</span>
                <span>Lap 70 (End)</span>
              </div>
            </div>
          </div>

          <div className="flex-[0.8] w-full space-y-4">
            <label className="text-sm font-bold text-muted-foreground uppercase tracking-widest block">Next Compound</label>
            <div className="flex gap-3">
              <Button 
                variant="outline" 
                onClick={() => setNextCompound("SOFT")}
                className={cn(
                  "flex-1 h-12 text-sm font-bold transition-all",
                  nextCompound === "SOFT" 
                    ? "bg-red-500 text-white border-none shadow-[0_0_20px_rgba(239,68,68,0.3)]" 
                    : "bg-white dark:bg-card border-red-500/30 text-red-500 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-500/10"
                )}
              >
                Soft
              </Button>
              <Button 
                variant="outline" 
                onClick={() => setNextCompound("MEDIUM")}
                className={cn(
                  "flex-1 h-12 text-sm font-bold transition-all",
                  nextCompound === "MEDIUM" 
                    ? "bg-yellow-500 text-black border-none shadow-[0_0_20px_rgba(234,179,8,0.3)]" 
                    : "bg-white dark:bg-card border-yellow-500/30 text-yellow-600 dark:text-yellow-400 hover:bg-yellow-50 dark:hover:bg-yellow-500/10"
                )}
              >
                Medium
              </Button>
              <Button 
                variant="outline"
                onClick={() => setNextCompound("HARD")}
                className={cn(
                  "flex-1 h-12 text-sm font-bold transition-all",
                  nextCompound === "HARD" 
                    ? "bg-slate-900 dark:bg-white text-white dark:text-black border-none shadow-[0_0_20px_rgba(0,0,0,0.3)] dark:shadow-[0_0_20px_rgba(255,255,255,0.3)]" 
                    : "bg-white dark:bg-card border-slate-300 dark:border-white/30 text-slate-900 dark:text-white hover:bg-slate-100 dark:hover:bg-white/10"
                )}
              >
                Hard
              </Button>
            </div>
          </div>

          <div className="w-full lg:w-48 shrink-0">
            <Button 
              onClick={handleSimulate} 
              disabled={isSimulating || !raceState}
              className="w-full h-14 text-base font-bold tracking-widest uppercase bg-purple-600 hover:bg-purple-500 shadow-[0_0_30px_rgba(147,51,234,0.4)] hover:shadow-[0_0_50px_rgba(147,51,234,0.6)] transition-all duration-300 rounded-xl disabled:opacity-80 disabled:cursor-not-allowed"
            >
              {isSimulating ? (
                <>
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  Processing
                </>
              ) : (
                <>
                  <Play className="w-5 h-5 mr-2 fill-current" />
                  Simulate
                </>
              )}
            </Button>
          </div>
        </div>
      </div>

      {/* Smoothly Revealed Results */}
      {hasSimulated && simulationResult && (
        <div 
          ref={resultsRef}
          className="transition-all duration-1000 ease-out space-y-12 overflow-hidden mt-12 opacity-100"
        >
          <div className="h-px w-full bg-gradient-to-r from-transparent via-purple-500/30 to-transparent" />
          
          <div className="space-y-6">
            <div className="flex items-center gap-3">
              <Activity className="w-6 h-6 text-emerald-600 dark:text-emerald-400" />
              <h2 className="text-2xl font-bold text-foreground tracking-tight">Time Loss Projection</h2>
            </div>
            
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
              <StatCard title="Expected Finish" value={simulationResult.expectedFinish} subtitle={`Median ${simulationResult.medianPosition}`} />
              <StatCard title="Rejoin Position" value={simulationResult.rejoinPosition} subtitle={`Lap ${simulationResult.pitLap}`} />
              <StatCard title="Expected Overtakes" value={simulationResult.expectedOvertakes} subtitle="High Traffic" />
              <div className="bg-card border border-border rounded-2xl p-5 flex flex-col justify-between h-full hover:bg-slate-50 dark:hover:bg-white/[0.02] transition-colors">
                <span className="text-sm font-semibold text-muted-foreground uppercase tracking-widest">Time Losses</span>
                <div className="space-y-2 mt-4">
                  <div className="flex justify-between items-center"><span className="text-sm text-muted-foreground">Pit</span><span className="font-mono text-red-500 dark:text-red-400 font-bold">{simulationResult.pitLoss}</span></div>
                  <div className="flex justify-between items-center"><span className="text-sm text-muted-foreground">Traffic</span><span className="font-mono text-yellow-600 dark:text-yellow-400 font-bold">{simulationResult.trafficLoss}</span></div>
                  <div className="flex justify-between items-center"><span className="text-sm text-muted-foreground">Degradation</span><span className="font-mono text-emerald-600 dark:text-emerald-400 font-bold">{simulationResult.degLoss}</span></div>
                </div>
              </div>
            </div>
          </div>

          {/* Monte Carlo Results */}
          <div className="space-y-6 pt-8 border-t border-border">
            <div className="flex items-center gap-3">
              <Target className="w-6 h-6 text-rose-500 dark:text-rose-400" />
              <h2 className="text-2xl font-bold text-foreground tracking-tight">Monte Carlo Stochastic Analysis</h2>
              <div className="ml-auto bg-rose-500/10 text-rose-600 dark:text-rose-400 text-xs font-bold uppercase tracking-widest px-3 py-1 rounded-full border border-rose-500/20">
                100 Iterations
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-card border border-border rounded-2xl p-6 flex flex-col justify-center items-center text-center space-y-2">
                <p className="text-sm font-semibold text-muted-foreground uppercase tracking-widest">Win Probability</p>
                <p className="text-5xl font-black text-foreground">{simulationResult.winProb}%</p>
              </div>
              <div className="bg-card border border-border rounded-2xl p-6 flex flex-col justify-center items-center text-center space-y-2 relative overflow-hidden">
                <div className="absolute inset-0 bg-purple-500/5" />
                <p className="text-sm font-semibold text-muted-foreground uppercase tracking-widest relative z-10">Podium Probability</p>
                <p className="text-5xl font-black text-purple-600 dark:text-purple-400 relative z-10">{simulationResult.podiumProb}%</p>
              </div>
              <div className="bg-card border border-border rounded-2xl p-6 flex flex-col justify-center items-center text-center space-y-2">
                <p className="text-sm font-semibold text-muted-foreground uppercase tracking-widest">Points Probability</p>
                <p className="text-5xl font-black text-emerald-600 dark:text-emerald-400">{simulationResult.pointsProb}%</p>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="bg-card border border-border rounded-3xl p-6 lg:col-span-2">
                <p className="text-sm font-bold text-muted-foreground uppercase tracking-widest mb-6">Position Probability Distribution</p>
                <div className="w-full h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={simulationResult.distribution} layout="vertical" margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
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
                        {simulationResult.distribution.map((_entry: any, index: number) => (
                          <Cell key={`cell-${index}`} fill={index < 3 ? '#7E57FF' : '#333333'} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="space-y-6">
                <StatCard title="Expected Finish" value={simulationResult.expectedFinish} />
                <StatCard title="Median Position" value={simulationResult.medianPosition} />
                <StatCard title="Standard Deviation" value={simulationResult.stdDev} subtitle="Positions" />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

