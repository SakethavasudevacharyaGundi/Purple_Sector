import { Link, useLocation } from "react-router-dom"
import { 
  Settings2, Activity, Target, LayoutDashboard, Settings
} from "lucide-react"
import { cn } from "@/lib/utils"

import { AnimatedThemeToggler } from "@/components/ui/animated-theme-toggler"

const navigation = [
  { name: "Race Setup", href: "/dashboard", icon: Settings2 },
  { name: "Simulation", href: "/simulation", icon: Activity },
  { name: "Elo of the Drivers", href: "/elo", icon: Target },
  { name: "Live Race (Beta)", href: "/live-race", icon: LayoutDashboard },
]

export function Sidebar() {
  const location = useLocation()

  return (
    <div className="flex h-screen w-64 flex-col bg-background border-r border-border transition-colors duration-500">
      <div className="flex h-16 shrink-0 items-center px-6 border-b border-border">
        <Link to="/" className="text-xl font-bold tracking-tight text-foreground hover:text-primary transition-colors flex items-center gap-2">
          <div className="w-4 h-4 rounded-full bg-primary" />
          Purple Sector
        </Link>
      </div>
      <div className="flex flex-1 flex-col overflow-y-auto">
        <nav className="flex-1 space-y-1 px-3 py-4">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href
            return (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  isActive
                    ? "bg-primary/10 text-primary"
                    : "text-muted-foreground hover:bg-slate-100 dark:hover:bg-[#1D1D1D] hover:text-foreground",
                  "group flex items-center rounded-md px-3 py-2.5 text-sm font-medium transition-colors"
                )}
              >
                <item.icon
                  className={cn(
                    isActive ? "text-primary" : "text-muted-foreground group-hover:text-foreground",
                    "mr-3 h-5 w-5 flex-shrink-0 transition-colors"
                  )}
                  aria-hidden="true"
                />
                {item.name}
              </Link>
            )
          })}
        </nav>
        <div className="p-3 border-t border-border flex items-center justify-between">
          <button className="group flex flex-1 items-center rounded-md px-3 py-2.5 text-sm font-medium text-muted-foreground hover:bg-slate-100 dark:hover:bg-[#1D1D1D] hover:text-foreground transition-colors">
            <Settings className="mr-3 h-5 w-5 flex-shrink-0 text-muted-foreground group-hover:text-foreground transition-colors" />
            Settings
          </button>
          <AnimatedThemeToggler />
        </div>
      </div>
    </div>
  )
}
