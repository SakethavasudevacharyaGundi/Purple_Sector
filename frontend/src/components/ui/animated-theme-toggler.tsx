import * as React from "react"
import { useTheme } from "next-themes"
import { Moon, Sun } from "lucide-react"

export function AnimatedThemeToggler() {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = React.useState(false)

  React.useEffect(() => {
    setMounted(true)
  }, [])

  const toggleTheme = (event: React.MouseEvent<HTMLButtonElement>) => {
    const isDark = theme === "dark"
    const nextTheme = isDark ? "light" : "dark"

    // Fallback for browsers that don't support View Transitions
    if (!document.startViewTransition) {
      setTheme(nextTheme)
      return
    }

    // Get the click position to use as the center of the transition circle
    const x = event.clientX
    const y = event.clientY

    const endRadius = Math.hypot(
      Math.max(x, innerWidth - x),
      Math.max(y, innerHeight - y)
    )

    const transition = document.startViewTransition(() => {
      setTheme(nextTheme)
    })

    transition.ready.then(() => {
      const clipPath = [
        `circle(0px at ${x}px ${y}px)`,
        `circle(${endRadius}px at ${x}px ${y}px)`,
      ]

      document.documentElement.animate(
        {
          clipPath: isDark ? [...clipPath].reverse() : clipPath,
        },
        {
          duration: 500,
          easing: "ease-in-out",
          pseudoElement: isDark
            ? "::view-transition-old(root)"
            : "::view-transition-new(root)",
        }
      )
    })
  }

  if (!mounted) {
    return <div className="w-10 h-10" />
  }

  return (
    <button
      onClick={toggleTheme}
      className="relative flex items-center justify-center w-10 h-10 rounded-full transition-colors hover:bg-slate-200 dark:hover:bg-slate-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-purple-500"
      aria-label="Toggle theme"
    >
      <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-transform duration-500 dark:-rotate-90 dark:scale-0 text-slate-800" />
      <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-transform duration-500 dark:rotate-0 dark:scale-100 text-slate-200" />
    </button>
  )
}
