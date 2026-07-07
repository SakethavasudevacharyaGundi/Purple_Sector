import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from 'next-themes';
import { 
  X, ChevronRight, Activity, BrainCircuit, 
  LineChart, Database, Cpu, Layers, BarChart3, Flag, 
  Zap, ArrowRight, Mail, Network, Code
} from 'lucide-react';
import { cn } from '../lib/utils';
// @ts-ignore
import GridMotion from '../components/ui/GridMotion';
// @ts-ignore
import FlowingMenu from '../components/ui/FlowingMenu';
// @ts-ignore
import GlitchText from '../components/ui/GlitchText';

import { AnimatedThemeToggler } from '@/components/ui/animated-theme-toggler';

import img1 from '../assets/1.avif';
import img2 from '../assets/2.avif';
import img3 from '../assets/3.avif';
import img4 from '../assets/4.avif';
import img5 from '../assets/5.avif';
import img6 from '../assets/6.avif';
import img7 from '../assets/7.avif';
import img8 from '../assets/8.avif';
import img9 from '../assets/9.avif';
import img10 from '../assets/10.avif';
import img11 from '../assets/11.avif';
import img12 from '../assets/12.avif';
import img13 from '../assets/13.avif';

const f1Images = [
  img1, img2, img3, img4, img5, img6, img7, img8, img9, img10, img11, img12, img13
];

const navItems = [
  { link: '/dashboard', text: 'Simulator', image: img10 },
  { link: '#problem', text: 'The Problem', image: img5 },
  { link: '#how-it-works', text: 'How It Works', image: img7 },
  { link: '#tech', text: 'Technology', image: img12 }
];

export function LandingPage() {
  const { resolvedTheme } = useTheme();
  const isDark = resolvedTheme === 'dark';
  const [navOpen, setNavOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [activeSection, setActiveSection] = useState(0);

  // Handle scroll for nav background using the main container
  // We'll attach onScroll directly to the main div since it's the scrolling container now.
  useEffect(() => {
    // keeping the useEffect clean, scroll logic moved to onScroll
  }, []);

  // Lock body scroll when nav is open
  useEffect(() => {
    if (navOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => { document.body.style.overflow = 'unset'; }
  }, [navOpen]);

  return (
    <div 
      id="scroll-container"
      className="h-screen overflow-y-auto overflow-x-hidden snap-y snap-mandatory bg-background text-foreground selection:bg-purple-500/30 font-sans scroll-smooth no-scrollbar"
      onScroll={(e) => {
        const scrollTop = e.currentTarget.scrollTop;
        setScrolled(scrollTop > 50);
        const sectionIndex = Math.round(scrollTop / window.innerHeight);
        setActiveSection(sectionIndex);
      }}
    >
      
      {/* --- GLOBAL BACKGROUND --- */}
      <div className="fixed inset-0 z-0 opacity-40 pointer-events-none">
        <GridMotion items={Array.from({ length: 28 }, (_, i) => f1Images[i % 13])} gradientColor={isDark ? "black" : "white"} />
      </div>
      
      {/* --- SIDE NAVIGATION INDICATOR --- */}
      <div className="fixed right-6 top-1/2 -translate-y-1/2 z-50 hidden md:flex flex-col items-center gap-2 bg-slate-200/50 dark:bg-white/10 backdrop-blur-md p-2 rounded-full border border-border">
        {[0, 1, 2, 3, 4].map((index) => (
          <button 
            key={index}
            onClick={() => {
              const container = document.getElementById('scroll-container');
              if (container) {
                container.scrollTo({ top: index * window.innerHeight, behavior: 'smooth' });
              }
            }}
            className={cn(
              "w-6 h-6 rounded flex items-center justify-center transition-all duration-300",
              activeSection === index ? "bg-white/20 shadow-sm" : "hover:bg-white/10"
            )}
            aria-label={`Scroll to section ${index + 1}`}
          >
            <div className={cn(
              "w-1.5 h-1.5 rounded-full transition-all duration-300",
              activeSection === index ? "bg-purple-400" : "bg-purple-700/60"
            )} />
          </button>
        ))}
      </div>
      
      {/* --- NAVIGATION --- */}
      <nav className={cn(
        "fixed top-0 left-0 right-0 z-50 transition-all duration-300 px-6 md:px-12 py-6 flex items-center justify-between",
        scrolled ? "bg-background/80 backdrop-blur-md border-b border-border" : "bg-transparent"
      )}>
        <div className="flex items-center gap-2 z-50 relative">
          <Link to="/" className="text-xl font-bold tracking-tighter text-foreground hover:text-purple-500 dark:hover:text-purple-400 transition-colors">
            p.sect
          </Link>
        </div>

        <div className="flex items-center gap-4 z-50 relative">
          <AnimatedThemeToggler />

        {/* Hamburger */}
        <button 
          onClick={() => setNavOpen(!navOpen)}
          className="z-50 relative p-2 -mr-2 text-foreground hover:text-purple-500 dark:hover:text-purple-400 transition-colors group"
          aria-label="Toggle Navigation"
        >
          {navOpen ? (
            <X className="w-6 h-6" />
          ) : (
            <div className="flex flex-col gap-[5px] items-end justify-center w-6 h-6">
              <span className="block w-6 h-[2px] bg-current transition-transform origin-right group-hover:scale-x-110"></span>
              <span className="block w-5 h-[2px] bg-current transition-transform origin-right group-hover:scale-x-125"></span>
              <span className="block w-4 h-[2px] bg-current transition-transform origin-right group-hover:scale-x-150"></span>
            </div>
          )}
        </button>
        </div>
      </nav>

      {/* Full Page Nav Overlay */}
      <div className={cn(
        "fixed inset-0 z-40 bg-background transition-all duration-500 ease-[cubic-bezier(0.22,1,0.36,1)] flex flex-col justify-center",
        navOpen ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none translate-y-8"
      )}>
        <div className="flex-1 w-full mt-24 pb-32">
          <FlowingMenu 
            items={navItems} 
            onItemClick={() => setNavOpen(false)}
            textColor={isDark ? "#ffffff" : "#000000"}
            bgColor="transparent"
            marqueeBgColor="#7E57FF"
            marqueeTextColor="#ffffff"
            borderColor={isDark ? "rgba(255, 255, 255, 0.1)" : "rgba(0, 0, 0, 0.1)"}
          />
        </div>
        <div className="absolute bottom-12 left-12 md:left-24 right-12 flex justify-between items-end pt-8 pointer-events-none z-50">
          <div className="text-sm text-slate-500 pointer-events-auto">
            Purple Sector © 2026 <br/>
            Open Source Intelligence
          </div>
          <div className="flex gap-4 pointer-events-auto">
            <a href="#" className="text-slate-500 hover:text-white transition-colors relative z-50">GitHub</a>
            <a href="#" className="text-slate-500 hover:text-white transition-colors relative z-50">Documentation</a>
          </div>
        </div>
      </div>

      {/* --- SECTION 1: HERO --- */}
      <section className="snap-start relative h-screen w-full flex flex-col items-center justify-center overflow-hidden">
        <div className={cn(
          "max-w-5xl mx-auto text-center z-10 flex flex-col items-center px-6 transition-all duration-1000 ease-[cubic-bezier(0.22,1,0.36,1)]",
          activeSection === 0 ? "opacity-100 translate-y-0 scale-100" : "opacity-0 translate-y-16 scale-95 blur-sm"
        )}>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-purple-500/30 bg-purple-500/10 text-purple-300 text-sm font-medium mb-8">
            <Zap className="w-4 h-4" /> v2.0 Decision Engine Live
          </div>
          
          <GlitchText
            speed={1.2}
            enableShadows={true}
            enableOnHover={true}
            className="text-6xl sm:text-7xl md:text-9xl font-bold tracking-tighter text-foreground mb-6 leading-[1.1]"
          >
            Purple Sector
          </GlitchText>
          <h2 className="text-2xl md:text-4xl font-light text-foreground/80 mb-8 max-w-3xl leading-tight">
            An AI Decision Support System for Formula One Strategy.
          </h2>
          <p className="text-lg text-muted-foreground mb-12 max-w-2xl leading-relaxed">
            Simulate pit strategies, predict race outcomes, evaluate probabilities, 
            and explore race strategy using machine learning and Monte Carlo simulation.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 items-center">
            <Link 
              to="/dashboard"
              className="px-8 py-4 bg-foreground text-background font-semibold rounded-full hover:bg-foreground/90 transition-colors flex items-center gap-2 group"
            >
              Start Simulation 
              <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>
        </div>
      </section>

      {/* --- SECTION 2: THE PROBLEM & SOLUTION --- */}
      <section id="problem" className="snap-start relative min-h-screen w-full flex flex-col justify-center px-6 pt-28 pb-12 border-t border-border bg-background/80 backdrop-blur-md overflow-hidden">
        <div className={cn(
          "max-w-7xl mx-auto w-full transition-all duration-1000 delay-100 ease-[cubic-bezier(0.22,1,0.36,1)]",
          activeSection === 1 ? "opacity-100 translate-x-0" : "opacity-0 -translate-x-16 blur-sm"
        )}>
          <div className="grid lg:grid-cols-2 gap-20 items-center">
            {/* Problem Side */}
            <div>
              <h2 className="text-4xl md:text-5xl font-semibold tracking-tight text-foreground mb-6">
                Every pit stop changes the race.
              </h2>
              <p className="text-xl text-muted-foreground mb-12 leading-relaxed">
                A single pit stop can decide a Grand Prix. Teams continuously evaluate 
                multiple variables before making a strategic decision.
              </p>
              
              <div className="flex flex-col gap-4 pl-4 border-l-2 border-slate-200 dark:border-slate-800">
                {['Tyre degradation', 'Traffic & Track position', 'Pit window timing', 'Safety Car probability', 'Weather conditions'].map((item, i) => (
                  <div key={i} className="flex items-center gap-3 text-foreground/80">
                    <div className="w-2 h-2 rounded-full bg-slate-300 dark:bg-slate-700" />
                    {item}
                  </div>
                ))}
              </div>
              
              <div className="mt-12 p-8 bg-slate-100/50 dark:bg-slate-900/50 rounded-2xl border border-border backdrop-blur-sm">
                <p className="text-sm text-muted-foreground uppercase tracking-widest font-semibold mb-2">The Ultimate Question</p>
                <p className="text-3xl font-bold text-foreground">Should we pit now?</p>
              </div>
            </div>

            {/* Solution Side */}
            <div className="flex flex-col gap-6">
              <div className="mb-6">
                <h3 className="text-2xl text-purple-600 dark:text-purple-400 font-medium mb-2">Our Solution</h3>
                <h4 className="text-3xl text-foreground font-semibold tracking-tight">Purple Sector makes race strategy measurable.</h4>
              </div>

              {/* Solution Cards */}
              <div className="grid gap-4">
                {[
                  {
                    icon: <Activity className="w-6 h-6 text-purple-600 dark:text-purple-400" />,
                    title: "Strategy Simulation",
                    desc: "Simulate any pit stop strategy in real-time before making a critical race decision."
                  },
                  {
                    icon: <BrainCircuit className="w-6 h-6 text-purple-600 dark:text-purple-400" />,
                    title: "Machine Learning",
                    desc: "Five predictive models estimate pit loss, traffic, tyre degradation, overtakes, and rejoin position."
                  },
                  {
                    icon: <LineChart className="w-6 h-6 text-purple-600 dark:text-purple-400" />,
                    title: "Monte Carlo",
                    desc: "Thousands of simulations estimate uncertainty instead of producing a single, brittle prediction."
                  }
                ].map((card, i) => (
                  <div key={i} className="p-6 rounded-2xl bg-slate-100/50 dark:bg-white/[0.02] border border-border hover:border-slate-300 dark:hover:border-white/10 hover:bg-slate-200/50 dark:hover:bg-white/[0.04] transition-all group flex gap-5">
                    <div className="mt-1 p-3 rounded-lg bg-white dark:bg-black/50 border border-border shadow-sm dark:shadow-none">
                      {card.icon}
                    </div>
                    <div>
                      <h5 className="text-xl font-semibold text-foreground mb-2">{card.title}</h5>
                      <p className="text-muted-foreground leading-relaxed">{card.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* --- SECTION 3: HOW IT WORKS & ENGINE --- */}
      <section id="how-it-works" className="snap-start relative min-h-screen w-full flex flex-col justify-center px-6 pt-28 pb-12 border-t border-border bg-background/60 backdrop-blur-md overflow-hidden">
        {/* Subtle background grid */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_50%,#000_70%,transparent_100%)] pointer-events-none" />
        
        <div className={cn(
          "max-w-7xl mx-auto relative z-10 w-full transition-all duration-1000 delay-100 ease-[cubic-bezier(0.22,1,0.36,1)]",
          activeSection === 2 ? "opacity-100 translate-y-0" : "opacity-0 translate-y-16 blur-sm"
        )}>
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-semibold tracking-tight text-foreground mb-6">
              Powered by a complete machine learning pipeline.
            </h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              This isn't a toy. It's a robust decision intelligence engine built on years of historical data.
            </p>
          </div>

          {/* Workflow Diagram */}
          <div className="grid md:grid-cols-4 gap-4 mb-16 relative">
            {/* Connecting lines for desktop */}
            <div className="hidden md:block absolute top-1/2 left-0 w-full h-[2px] bg-gradient-to-r from-purple-500/0 via-purple-500/50 to-purple-500/0 -translate-y-1/2 z-0" />
            
            {[
              { title: "Current Race", desc: "Live telemetry and state", icon: <Flag className="w-5 h-5" /> },
              { title: "Generate Strategies", desc: "Explore pit windows", icon: <Layers className="w-5 h-5" /> },
              { title: "Simulate Outcomes", desc: "Predict degradation", icon: <Cpu className="w-5 h-5" /> },
              { title: "Recommend", desc: "Best expected finish", icon: <BarChart3 className="w-5 h-5" /> },
            ].map((step, i) => (
              <div key={i} className="relative z-10 p-6 rounded-2xl bg-card border border-border shadow-2xl flex flex-col items-center text-center group">
                <div className="w-12 h-12 rounded-full bg-slate-100 dark:bg-slate-900 border border-border flex items-center justify-center text-slate-500 dark:text-slate-300 mb-4 group-hover:text-purple-600 dark:group-hover:text-purple-400 group-hover:border-purple-500/50 transition-colors">
                  {step.icon}
                </div>
                <h4 className="text-lg font-semibold text-foreground mb-2">{step.title}</h4>
                <p className="text-sm text-muted-foreground">{step.desc}</p>
              </div>
            ))}
          </div>

          {/* Pipeline */}
          <div className="max-w-4xl mx-auto bg-slate-50/50 dark:bg-white/[0.02] border border-border rounded-3xl p-8 md:p-12">
            <h3 className="text-lg uppercase tracking-widest font-semibold text-muted-foreground mb-12 text-center">Data Pipeline</h3>
            <div className="flex flex-wrap justify-center gap-3">
              {['FastF1 Data', 'Feature Engineering', 'Machine Learning', 'ELO Driver Ratings', 'Strategy Simulator', 'Monte Carlo', 'Recommendation Engine'].map((tag, i, arr) => (
                <React.Fragment key={i}>
                  <div className="px-4 py-2 rounded-lg bg-white dark:bg-black border border-border text-foreground/80 font-mono text-sm shadow-sm flex items-center gap-2">
                    <Database className="w-3 h-3 text-purple-600 dark:text-purple-500" />
                    {tag}
                  </div>
                  {i < arr.length - 1 && (
                    <div className="hidden sm:flex items-center text-slate-400 dark:text-slate-700">
                      <ChevronRight className="w-4 h-4" />
                    </div>
                  )}
                </React.Fragment>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* --- SECTION 4: FEATURES, TECH --- */}
      <section id="tech" className="snap-start relative min-h-screen w-full flex flex-col justify-center px-6 pt-28 pb-12 border-t border-border bg-background/70 backdrop-blur-lg overflow-hidden">
        <div className={cn(
          "max-w-7xl mx-auto w-full transition-all duration-1000 delay-100 ease-[cubic-bezier(0.22,1,0.36,1)]",
          activeSection === 3 ? "opacity-100 scale-100" : "opacity-0 scale-95 blur-sm"
        )}>
          
          {/* Key Features Grid */}
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
            {[
              { t: "Race State Builder", d: "Create any race scenario." },
              { t: "Strategy Simulator", d: "Predict the effect of different pit windows." },
              { t: "Monte Carlo Analysis", d: "Estimate podium, points and win probabilities." },
              { t: "Historical Validation", d: "Evaluate predictions against previous Formula One races." },
              { t: "Driver ELO", d: "Performance ratings built from every race since 2018." },
              { t: "Explainable AI", d: "Break every prediction into pit loss, traffic, overtakes and degradation." }
            ].map((f, i) => (
              <div key={i} className="p-8 rounded-2xl bg-card border border-border hover:bg-slate-100 dark:hover:bg-slate-900 transition-colors">
                <h5 className="text-lg font-semibold text-foreground mb-2">{f.t}</h5>
                <p className="text-muted-foreground text-sm leading-relaxed">{f.d}</p>
              </div>
            ))}
          </div>

          {/* Example / Concrete Value */}
          <div className="max-w-4xl mx-auto flex flex-col md:flex-row items-center gap-8 md:gap-16 mb-16 p-8 md:p-12 rounded-3xl bg-purple-500/5 dark:bg-purple-900/10 border border-purple-500/20">
            <div className="flex-1 space-y-4 font-mono text-sm">
              <div className="text-muted-foreground mb-2 uppercase tracking-widest text-xs">Current Race State</div>
              <div className="flex justify-between border-b border-border pb-2"><span className="text-muted-foreground">Grand Prix</span><span className="text-foreground">British GP</span></div>
              <div className="flex justify-between border-b border-border pb-2"><span className="text-muted-foreground">Driver</span><span className="text-foreground">Lando Norris</span></div>
              <div className="flex justify-between border-b border-border pb-2"><span className="text-muted-foreground">Position</span><span className="text-foreground">P2</span></div>
              <div className="flex justify-between border-b border-border pb-2"><span className="text-muted-foreground">Lap</span><span className="text-foreground">38</span></div>
              <div className="flex justify-between"><span className="text-muted-foreground">Tyre Age</span><span className="text-yellow-600 dark:text-yellow-500">Medium (18 laps)</span></div>
            </div>
            
            <div className="flex items-center justify-center">
              <ArrowRight className="w-8 h-8 text-purple-600 dark:text-purple-500 hidden md:block" />
              <ArrowRight className="w-8 h-8 text-purple-600 dark:text-purple-500 md:hidden rotate-90" />
            </div>

            <div className="flex-1 space-y-4 font-mono text-sm bg-white dark:bg-black p-6 rounded-xl border border-border shadow-2xl relative overflow-hidden">
              <div className="absolute top-0 left-0 w-1 h-full bg-green-500" />
              <div className="text-muted-foreground mb-2 uppercase tracking-widest text-xs">Purple Sector Recommendation</div>
              <div className="flex justify-between border-b border-border pb-2"><span className="text-muted-foreground">Strategy</span><span className="text-foreground font-bold">Pit Lap 40</span></div>
              <div className="flex justify-between border-b border-border pb-2"><span className="text-muted-foreground">Compound</span><span className="text-foreground">Hard</span></div>
              <div className="flex justify-between border-b border-border pb-2"><span className="text-muted-foreground">Exp. Finish</span><span className="text-foreground">P2</span></div>
              <div className="flex justify-between"><span className="text-muted-foreground">Podium Prob.</span><span className="text-green-600 dark:text-green-400 font-bold">82%</span></div>
            </div>
          </div>

          {/* Technology */}
          <div className="text-center">
            <h3 className="text-sm font-semibold text-muted-foreground tracking-widest uppercase mb-8">Built With</h3>
            <div className="flex flex-wrap justify-center items-center gap-8 md:gap-16 opacity-60 grayscale hover:grayscale-0 transition-all duration-500">
              {['Python', 'FastAPI', 'Scikit-learn', 'FastF1', 'React', 'TypeScript', 'TailwindCSS'].map((tech) => (
                <span key={tech} className="text-xl font-bold font-sans text-foreground/80">{tech}</span>
              ))}
            </div>
          </div>

        </div>
      </section>

      {/* --- SECTION 5: CTA & FOOTER --- */}
      <section className="snap-start relative min-h-screen w-full flex flex-col justify-center px-6 pt-28 border-t border-border bg-background/80 backdrop-blur-xl overflow-hidden">
        <div className={cn(
          "max-w-7xl mx-auto w-full h-full flex flex-col justify-between pt-24 pb-8 transition-all duration-1000 delay-100 ease-[cubic-bezier(0.22,1,0.36,1)]",
          activeSection === 4 ? "opacity-100 translate-y-0" : "opacity-0 translate-y-16 blur-sm"
        )}>
          {/* Call to Action */}
          <div className="text-center bg-slate-100/50 dark:bg-white/[0.02] border border-border rounded-[3rem] p-12 md:p-24 relative overflow-hidden mt-auto mb-auto">
            <div className="absolute inset-0 bg-gradient-to-t from-purple-500/10 dark:from-purple-900/20 to-transparent" />
            <div className="relative z-10 w-full max-w-4xl mx-auto">
              <h2 className="text-4xl md:text-5xl font-bold tracking-tight text-foreground mb-6">
                About the Developer
              </h2>
              <p className="text-lg md:text-xl text-muted-foreground mb-12 max-w-2xl mx-auto leading-relaxed">
                Hi, I'm <strong>Sakethavasudev</strong>. I'm a passionate AI systems architect and full-stack developer dedicated to building intelligent, data-driven applications. Purple Sector represents the intersection of my love for Formula One strategy and cutting-edge machine learning.
              </p>
              
              <div className="flex flex-col sm:flex-row items-center justify-center gap-6 w-full mb-8">
                <a 
                  href="mailto:sakethavasudev@gmail.com" 
                  className="flex items-center justify-center gap-3 w-full sm:w-auto px-8 py-4 bg-slate-200/50 dark:bg-white/5 border border-border rounded-2xl hover:bg-purple-500/10 hover:border-purple-500/30 transition-all group"
                >
                  <Mail className="w-5 h-5 text-purple-600 dark:text-purple-400 group-hover:scale-110 transition-transform" />
                  <span className="font-medium text-foreground">Email Me</span>
                </a>
                
                <a 
                  href="https://linkedin.com/in/sakethavasudev" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center justify-center gap-3 w-full sm:w-auto px-8 py-4 bg-slate-200/50 dark:bg-white/5 border border-border rounded-2xl hover:bg-blue-500/10 hover:border-blue-500/30 transition-all group"
                >
                  <Network className="w-5 h-5 text-blue-600 dark:text-blue-400 group-hover:scale-110 transition-transform" />
                  <span className="font-medium text-foreground">LinkedIn</span>
                </a>

                <a 
                  href="https://github.com/SakethavasudevacharyaGundi" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center justify-center gap-3 w-full sm:w-auto px-8 py-4 bg-slate-200/50 dark:bg-white/5 border border-border rounded-2xl hover:bg-slate-300 dark:hover:bg-white/10 transition-all group"
                >
                  <Code className="w-5 h-5 text-slate-800 dark:text-slate-300 group-hover:scale-110 transition-transform" />
                  <span className="font-medium text-foreground">GitHub</span>
                </a>
              </div>
            </div>
          </div>

          {/* Footer (now inside Section 5) */}
          <footer className="border-t border-border pt-8 mt-12 w-full flex flex-col md:flex-row justify-between items-center gap-6">
            <div className="flex items-center gap-2">
              <span className="text-xl font-bold text-foreground tracking-tighter">p.sect</span>
              <span className="text-border">|</span>
              <span className="text-muted-foreground text-sm">Decision Support System</span>
            </div>
            
            <div className="flex gap-8 text-sm font-medium text-muted-foreground">
              <a href="#" className="hover:text-foreground transition-colors">GitHub</a>
              <a href="#" className="hover:text-foreground transition-colors">LinkedIn</a>
              <a href="#" className="hover:text-foreground transition-colors">Documentation</a>
              <a href="#" className="hover:text-foreground transition-colors">License</a>
            </div>
          </footer>
        </div>
      </section>

    </div>
  );
}

export default LandingPage;
