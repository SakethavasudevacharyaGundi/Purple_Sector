import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Calendar, Flag, User, Clock, ChevronRight } from "lucide-react"
import { fetchSeasons, fetchSeasonMetadata } from "@/lib/api"

export function Dashboard() {
  const navigate = useNavigate()

  // Metadata State
  const [availableSeasons, setAvailableSeasons] = useState<number[]>([])
  const [events, setEvents] = useState<{name: string, max_laps: number}[]>([])
  const [drivers, setDrivers] = useState<{id: string, name: string}[]>([])
  
  // Form State
  const [season, setSeason] = useState("")
  const [gp, setGp] = useState("")
  const [driver, setDriver] = useState("")
  const [lap, setLap] = useState("1")

  const [isFetching, setIsFetching] = useState(false)
  const [isLoadingMetadata, setIsLoadingMetadata] = useState(true)

  // Load Seasons on mount
  useEffect(() => {
    fetchSeasons().then(data => {
      setAvailableSeasons(data)
      if (data.length > 0) {
        setSeason(data[0].toString())
      }
    }).catch(err => {
      console.error("Failed to fetch seasons:", err)
    })
  }, [])

  // Load Metadata when Season changes
  useEffect(() => {
    if (!season) return
    setIsLoadingMetadata(true)
    fetchSeasonMetadata(season).then(data => {
      setEvents(data.events)
      setDrivers(data.drivers)
      
      if (data.events.length > 0) {
        setGp(data.events[0].name)
      }
      if (data.drivers.length > 0) {
        setDriver(data.drivers[0].id)
      }
      setIsLoadingMetadata(false)
    }).catch(err => {
      console.error("Failed to fetch metadata:", err)
      setIsLoadingMetadata(false)
    })
  }, [season])

  // Adjust lap when GP changes
  useEffect(() => {
    if (!gp || events.length === 0) return
    const currentEvent = events.find(e => e.name === gp)
    if (currentEvent) {
      if (parseInt(lap) > currentEvent.max_laps) {
        setLap(currentEvent.max_laps.toString())
      }
    }
  }, [gp, events])

  const handleSimulateCustom = async () => {
    setIsFetching(true)
    try {
      const { fetchSetup } = await import('@/lib/api')
      const raceState = await fetchSetup({
        season: parseInt(season),
        gp,
        lap: parseInt(lap),
        driver
      })
      
      navigate("/simulation", { 
        state: { 
          raceState,
          driverCode: driver,
          source: "historical",
        } 
      })
    } catch (error) {
      console.error("Failed to setup race for custom simulation:", error)
      // Additional error handling could be done here
    } finally {
      setIsFetching(false)
    }
  }

  const handleSimulateStrategies = async () => {
    setIsFetching(true)
    try {
      const { fetchSetup } = await import('@/lib/api')
      const raceState = await fetchSetup({
        season: parseInt(season),
        gp,
        lap: parseInt(lap),
        driver
      })

      // Assuming driver is 3 letter acronym, we match it to driver_name or use driver mapping
      // The backend returns the driver as driver_name=4, team=UNKNOWN etc if it's the driver_number.
      // We pass the full raceState and let the Recommendation page extract what it needs.
      navigate('/recommendation', { state: { raceState, driverCode: driver } })
    } catch (error) {
      console.error("Failed to setup race:", error)
      // Fallback or error handling can go here
    } finally {
      setIsFetching(false)
    }
  }

  return (
    <div className="relative w-full min-h-[calc(100vh-4rem)] flex items-center justify-center p-6 lg:p-12">
      {/* Decorative tech rings background */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] border border-purple-500/5 rounded-full pointer-events-none" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] border border-purple-500/10 rounded-full pointer-events-none border-dashed" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] border border-purple-500/5 rounded-full pointer-events-none" />

      {/* Main UI Container */}
      <div className="relative z-10 w-full max-w-5xl mx-auto flex flex-col lg:flex-row gap-12 items-center animate-in fade-in duration-1000 slide-in-from-bottom-8">
        
        {/* Left Side: Copy */}
        <div className="text-left flex-1 space-y-6">
          <div className="inline-flex items-center gap-2 text-purple-600 dark:text-purple-400 text-sm font-bold uppercase tracking-[0.2em]">
            <span className="w-8 h-[2px] bg-purple-500/50" /> System Initialization
          </div>
          <h1 className="text-5xl md:text-7xl font-black tracking-tighter text-foreground uppercase leading-[0.9]">
            Race State <br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-500 to-indigo-600 dark:from-purple-400 dark:to-indigo-600">
              Setup
            </span>
          </h1>
          <p className="text-lg text-muted-foreground max-w-md font-light leading-relaxed">
            Configure the baseline parameters. The engine will ingest historical telemetry and compute predictive strategy deviations.
          </p>
        </div>

        {/* Right Side: Solid Dark Panel Form */}
        <div className="flex-1 w-full bg-card border border-border rounded-3xl p-8 shadow-[0_0_40px_rgba(0,0,0,0.1)] dark:shadow-[0_0_40px_rgba(0,0,0,0.5)] relative overflow-hidden">
          {/* Accent Line */}
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-purple-600 to-indigo-600" />
          
          <div className="space-y-8">
            <div className="grid grid-cols-2 gap-6">
              <div className="space-y-3">
                <label className="flex items-center gap-2 text-xs font-bold text-muted-foreground uppercase tracking-widest">
                  <Calendar className="w-4 h-4 text-muted-foreground" /> Season
                </label>
                <Select value={season} onValueChange={setSeason} disabled={isLoadingMetadata}>
                  <SelectTrigger className="h-12 bg-slate-100 dark:bg-white/[0.03] border-border text-base rounded-xl hover:bg-slate-200 dark:hover:bg-white/[0.06] transition-colors focus:ring-purple-500/50">
                    <SelectValue placeholder="Select Season" />
                  </SelectTrigger>
                  <SelectContent>
                    {availableSeasons.map(s => (
                      <SelectItem key={s} value={s.toString()}>{s} Season</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-3">
                <label className="flex items-center gap-2 text-xs font-bold text-muted-foreground uppercase tracking-widest">
                  <Flag className="w-4 h-4 text-muted-foreground" /> Event
                </label>
                <Select value={gp} onValueChange={setGp} disabled={isLoadingMetadata}>
                  <SelectTrigger className="h-12 bg-slate-100 dark:bg-white/[0.03] border-border text-base rounded-xl hover:bg-slate-200 dark:hover:bg-white/[0.06] transition-colors focus:ring-purple-500/50">
                    <SelectValue placeholder="Select Event" />
                  </SelectTrigger>
                  <SelectContent>
                    {events.map(e => (
                      <SelectItem key={e.name} value={e.name}>{e.name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-3">
                <label className="flex items-center gap-2 text-xs font-bold text-muted-foreground uppercase tracking-widest">
                  <User className="w-4 h-4 text-muted-foreground" /> Driver
                </label>
                <Select value={driver} onValueChange={setDriver} disabled={isLoadingMetadata}>
                  <SelectTrigger className="h-12 bg-slate-100 dark:bg-white/[0.03] border-border text-base rounded-xl hover:bg-slate-200 dark:hover:bg-white/[0.06] transition-colors focus:ring-purple-500/50">
                    <SelectValue placeholder="Select Driver" />
                  </SelectTrigger>
                  <SelectContent>
                    {drivers.map(d => (
                      <SelectItem key={d.id} value={d.id}>{d.name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-3">
                <label className="flex items-center gap-2 text-xs font-bold text-muted-foreground uppercase tracking-widest">
                  <Clock className="w-4 h-4 text-muted-foreground" /> Start Lap
                </label>
                <Select value={lap} onValueChange={setLap} disabled={isLoadingMetadata}>
                  <SelectTrigger className="h-12 bg-slate-100 dark:bg-white/[0.03] border-border text-base rounded-xl hover:bg-slate-200 dark:hover:bg-white/[0.06] transition-colors focus:ring-purple-500/50">
                    <SelectValue placeholder="Select Lap" />
                  </SelectTrigger>
                  <SelectContent className="max-h-60">
                    {Array.from({ length: events.find(e => e.name === gp)?.max_laps || 1 }).map((_, i) => (
                      <SelectItem key={i + 1} value={(i + 1).toString()}>Lap {i + 1}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="flex gap-4 mt-4">
              <Button 
                onClick={handleSimulateCustom} 
                className="flex-1 h-14 rounded-xl bg-slate-100 dark:bg-[#111] border border-purple-500/30 text-purple-600 dark:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-500/10 text-lg font-bold transition-all duration-300"
              >
                Simulate Custom
              </Button>
              <Button 
                onClick={handleSimulateStrategies}
                disabled={isFetching}
                className="flex-[1.5] h-14 rounded-xl bg-purple-600 hover:bg-purple-700 dark:hover:bg-purple-500 text-white text-lg font-bold shadow-[0_0_30px_rgba(147,51,234,0.1)] dark:shadow-[0_0_30px_rgba(147,51,234,0.3)] hover:shadow-[0_0_50px_rgba(147,51,234,0.5)] transition-all duration-300 group flex items-center justify-between px-6 disabled:opacity-70 disabled:cursor-not-allowed"
              >
                <span>{isFetching ? "Initializing Engine..." : "Simulate Strategies"}</span>
                <div className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center group-hover:bg-white text-white group-hover:text-purple-600 transition-colors">
                  {isFetching ? (
                     <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  ) : (
                    <ChevronRight className="w-5 h-5" />
                  )}
                </div>
              </Button>
            </div>
          </div>
        </div>

      </div>
    </div>
  )
}
