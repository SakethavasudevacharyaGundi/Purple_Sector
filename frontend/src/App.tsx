import { useState, useEffect } from "react"
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom"
import { Layout } from "./components/layout/Layout"

import { Dashboard } from "./pages/Dashboard"
import { RaceSetup } from "./pages/RaceSetup"
import { Simulation } from "./pages/Simulation"
import { MonteCarlo } from "./pages/MonteCarlo"
import { Recommendation } from "./pages/Recommendation"
import { Historical } from "./pages/Historical"
import { EloRanking } from "./pages/EloRanking"
import { LiveRace } from "./pages/LiveRace"
import { LoadingScreen } from "./components/ui/LoadingScreen"
import { LandingPage } from "./pages/LandingPage"
// @ts-ignore
import GridScan from "./components/ui/GridScan"

function AppContent() {
  const location = useLocation();
  const [isLoading, setIsLoading] = useState(location.pathname === '/');
  const [displayLocation, setDisplayLocation] = useState(location);

  // Handle initial load on landing page
  useEffect(() => {
    if (location.pathname === '/') {
      const timeout = setTimeout(() => {
        setIsLoading(false);
      }, 1500);
      return () => clearTimeout(timeout);
    }
  }, []);

  // Trigger loading screen on page change to/from landing page
  useEffect(() => {
    if (location.pathname !== displayLocation.pathname) {
      const isLandingTransition = location.pathname === '/' || displayLocation.pathname === '/';
      
      if (isLandingTransition) {
        setIsLoading(true);
        
        // We wait for the loading screen's animation duration
        const timeout = setTimeout(() => {
          setDisplayLocation(location);
          setIsLoading(false);
        }, 1500); 

        return () => clearTimeout(timeout);
      } else {
        // Immediate transition for all other pages
        setDisplayLocation(location);
      }
    }
  }, [location, displayLocation]);

  return (
    <>
      <div className="fixed inset-0 z-[-1] pointer-events-none mix-blend-screen opacity-60">
        <GridScan
          sensitivity={0.55}
          lineThickness={1}
          linesColor="#2F293A"
          gridScale={0.1}
          scanColor="#FF9FFC"
          scanOpacity={0.4}
          enablePost={true}
          bloomIntensity={0.6}
          chromaticAberration={0.002}
          noiseIntensity={0.01}
        />
      </div>

      {isLoading && (
        <div className="fixed inset-0 z-[100] bg-slate-950">
          <LoadingScreen />
        </div>
      )}
      
      {/* 
        We hide the content during loading. 
        Note: We use 'display: none' so the DOM is preserved, but we pass displayLocation 
        so the React tree still thinks it's on the old page until loading finishes. 
      */}
      <div style={{ display: isLoading ? 'none' : 'block', height: '100%' }}>
        <Routes location={displayLocation}>
          {/* Landing Page */}
          <Route path="/" element={<LandingPage />} />
          
          {/* Main app layout routes */}
          <Route
            path="/*"
            element={
              <Layout>
                <Routes location={displayLocation}>
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/setup" element={<RaceSetup />} />
                  <Route path="/simulation" element={<Simulation />} />
                  <Route path="/monte-carlo" element={<MonteCarlo />} />
                  <Route path="/recommendation" element={<Recommendation />} />
                  <Route path="/historical" element={<Historical />} />
                  <Route path="/elo" element={<EloRanking />} />
                  <Route path="/live-race" element={<LiveRace />} />
                </Routes>
              </Layout>
            }
          />
        </Routes>
      </div>
    </>
  )
}

import { ThemeProvider } from "./components/ThemeProvider"

function App() {
  return (
    <ThemeProvider attribute="class" defaultTheme="dark" enableSystem disableTransitionOnChange>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App
