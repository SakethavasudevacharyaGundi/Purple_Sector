
import { cn } from '../../lib/utils';

interface LoadingScreenProps {
  className?: string;
}

export function LoadingScreen({ className }: LoadingScreenProps) {
  const streaks = Array.from({ length: 120 }).map(() => {
    const top = Math.random() * 100; 
    const height = Math.random() < 0.8 ? 1 : 2 + Math.random() * 2;
    const length = 50 + Math.random() * 200; 
    const isPink = Math.random() > 0.6;
    const opacity = 0.3 + Math.random() * 0.7;

    const color = isPink
      ? 'from-transparent via-pink-500/80 to-pink-300'
      : 'from-transparent via-white/80 to-white';

    return { top, height, length, color, opacity };
  });

  return (
    <div
      className={cn(
        'relative w-full h-screen overflow-hidden flex flex-col items-center justify-center bg-slate-950',
        className
      )}
    >
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-indigo-900 via-purple-950 to-slate-950 opacity-90" />

      {/* 
        Horizontal Text Band Container
        By removing the fixed heights and using flex, this container's height 
        will exactly match the height of the h1 text inside it.
      */}
      <div className="relative w-full flex items-center justify-center overflow-hidden">
        
        <h1
          className="relative z-20 text-7xl sm:text-8xl md:text-9xl font-black italic tracking-tighter leading-none text-transparent bg-clip-text bg-gradient-to-r from-white via-white to-pink-100 select-none drop-shadow-[0_0_15px_rgba(255,255,255,0.4)]"
          style={{ fontFamily: "'Inter', 'Outfit', system-ui, sans-serif" }}
        >
          P.Sect
        </h1>

        <div 
          className="absolute top-0 bottom-0 w-[100vw] z-30 pointer-events-none"
          style={{
            // Sped up from 1.8s to 1.2s
            animation: `light-sweep 1.2s cubic-bezier(0.1, 0, 0.9, 1) 0.3s forwards`,
            transform: 'translateX(-100vw)', 
            willChange: 'transform',
          }}
        >
          <div className="absolute top-0 bottom-0 right-0 w-[4px] bg-white/40 blur-[4px] shadow-[0_0_40px_#fff,0_0_80px_#fbcfe8]" />

          {streaks.map((streak, i) => (
            <div
              key={i}
              className={`absolute right-0 bg-gradient-to-r ${streak.color}`}
              style={{
                top: `${streak.top}%`,
                height: `${streak.height}px`,
                width: `${streak.length}vw`,
                opacity: streak.opacity,
                filter: 'blur(0.5px)',
                borderTopRightRadius: '9999px',
                borderBottomRightRadius: '9999px',
              }}
            />
          ))}
        </div>
      </div>

      <style>{`
        @keyframes light-sweep {
          0% {
            transform: translateX(-100vw);
          }
          100% {
            transform: translateX(350vw); 
          }
        }
      `}</style>
    </div>
  );
}

export default LoadingScreen;
