import { Radio, AlertCircle } from "lucide-react"

export function LiveRace() {
  return (
    <div className="w-full min-h-[calc(100vh-8rem)] flex items-center justify-center p-6 animate-in fade-in duration-1000">
      <div className="text-center max-w-2xl mx-auto space-y-8">
        <div className="relative inline-flex items-center justify-center w-24 h-24 rounded-full bg-purple-500/10 border border-purple-500/20 mb-4">
          <div className="absolute inset-0 rounded-full border border-purple-500/50 animate-ping opacity-20" />
          <Radio className="w-10 h-10 text-purple-400" />
        </div>
        
        <h1 className="text-5xl md:text-6xl font-bold tracking-tighter text-white">
          Live Race Telemetry
        </h1>
        
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm font-semibold uppercase tracking-widest">
          <AlertCircle className="w-4 h-4" /> Beta Version
        </div>

        <p className="text-xl text-slate-400 font-light leading-relaxed">
          The real-time telemetry streaming and live strategy recommendation engine is currently in closed beta. 
          We are calibrating the live data ingestion pipeline to ensure sub-millisecond latency.
        </p>

        <div className="pt-8">
          <div className="h-1 w-48 bg-gradient-to-r from-transparent via-purple-500/50 to-transparent mx-auto rounded-full opacity-50" />
        </div>
      </div>
    </div>
  )
}
