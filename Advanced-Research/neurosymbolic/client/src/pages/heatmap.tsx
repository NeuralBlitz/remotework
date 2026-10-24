import { Navigation } from "@/components/layout/Navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { AlertTriangle, Shield, Zap, Info, TrendingUp, Filter, Maximize2 } from "lucide-react";
import { motion } from "framer-motion";
import { useState } from "react";
import { cn } from "@/lib/utils";

const regions = [
  { id: "us-east", name: "US-EAST", risk: 12, drift: "0.002", load: "42%" },
  { id: "eu-west", name: "EU-WEST", risk: 8, drift: "0.001", load: "38%" },
  { id: "ap-south", name: "AP-SOUTH", risk: 45, drift: "0.012", load: "78%" },
  { id: "sa-east", name: "SA-EAST", risk: 22, drift: "0.005", load: "55%" },
];

export default function RiskHeatmap() {
  const [selectedRegion, setSelectedRegion] = useState(regions[0]);

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30">
      <Navigation />
      <main className="md:pl-64 pt-16 md:pt-0 pb-24 md:pb-0 min-h-screen relative overflow-hidden">
        <div className="relative z-10 p-4 md:p-8 space-y-6">
          <header className="border-b border-white/10 pb-6 flex justify-between items-end">
            <div>
              <h1 className="text-3xl font-display font-bold text-white tracking-tight flex items-center gap-3">
                <AlertTriangle className="text-destructive" /> Neural Risk Heatmap
              </h1>
              <p className="text-muted-foreground mt-2 max-w-2xl font-display text-sm">
                Real-time spatial visualization of alignment drift and ethical risk vectors across global nodes.
              </p>
            </div>
            <div className="flex gap-2">
               <button className="bg-white/5 border border-white/10 px-3 py-1 rounded text-[10px] font-mono hover:bg-white/10 transition-all flex items-center gap-2 uppercase tracking-widest text-muted-foreground">
                 <Filter className="w-3 h-3" /> Filter Traces
               </button>
            </div>
          </header>

          <div className="grid grid-cols-12 gap-6">
            <Card className="col-span-12 lg:col-span-8 bg-black/40 border-white/10 min-h-[500px] relative overflow-hidden flex flex-col">
              <CardHeader className="border-b border-white/10 bg-white/2 flex justify-between items-center">
                <span className="text-[10px] font-mono text-primary uppercase tracking-widest">Global Node Topology</span>
                <span className="text-[10px] font-mono text-muted-foreground uppercase">Live Update: {new Date().toLocaleTimeString()}</span>
              </CardHeader>
              <div className="flex-1 p-12 relative flex items-center justify-center">
                {/* Simulated Map / Grid */}
                <div className="absolute inset-0 opacity-10 bg-[radial-gradient(circle_at_center,var(--color-primary)_0%,transparent_70%)]" />
                <div className="grid grid-cols-4 gap-8 relative z-10">
                  {regions.map((region) => (
                    <motion.button
                      key={region.id}
                      whileHover={{ scale: 1.05 }}
                      onClick={() => setSelectedRegion(region)}
                      className={cn(
                        "w-32 h-32 rounded-xl border-2 flex flex-col items-center justify-center gap-2 transition-all shadow-2xl relative group",
                        region.risk > 40 ? "border-destructive/50 bg-destructive/10" : 
                        region.risk > 20 ? "border-amber-500/50 bg-amber-500/10" : "border-primary/50 bg-primary/10",
                        selectedRegion.id === region.id && "ring-4 ring-white/20 scale-110"
                      )}
                    >
                      <div className={cn(
                        "w-3 h-3 rounded-full animate-ping",
                        region.risk > 40 ? "bg-destructive" : region.risk > 20 ? "bg-amber-500" : "bg-primary"
                      )} />
                      <span className="font-mono text-xs font-bold text-white">{region.name}</span>
                      <span className="text-[9px] font-mono opacity-60">Risk: {region.risk}%</span>
                    </motion.button>
                  ))}
                </div>
              </div>
            </Card>

            <div className="col-span-12 lg:col-span-4 space-y-6">
              <Card className="bg-black/40 border-white/10 h-full">
                <CardHeader className="border-b border-white/10">
                  <CardTitle className="text-xs font-mono text-primary uppercase flex items-center gap-2">
                    <Info className="w-4 h-4" /> Node Diagnostics: {selectedRegion.name}
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-6 space-y-6">
                  <div className="space-y-4">
                     {[
                       { label: "Alignment Drift", val: selectedRegion.drift, color: "text-primary" },
                       { label: "Sync Latency", val: "12ms", color: "text-secondary" },
                       { label: "Compute Load", val: selectedRegion.load, color: "text-white" },
                     ].map((diag) => (
                       <div key={diag.label} className="flex justify-between items-center p-3 bg-white/5 rounded border border-white/5">
                          <span className="text-[10px] font-mono text-muted-foreground uppercase">{diag.label}</span>
                          <span className={cn("text-xs font-mono font-bold", diag.color)}>{diag.val}</span>
                       </div>
                     ))}
                  </div>

                  <Card className={cn(
                    "p-4 border-l-4",
                    selectedRegion.risk > 40 ? "bg-destructive/10 border-destructive" : "bg-primary/5 border-primary"
                  )}>
                    <div className="flex items-center gap-2 mb-2">
                      <Shield className="w-4 h-4 text-white" />
                      <span className="text-[10px] font-mono font-bold uppercase">Governor Action</span>
                    </div>
                    <p className="text-[10px] text-muted-foreground leading-relaxed italic">
                      {selectedRegion.risk > 40 
                        ? "CRITICAL: Automated intervention triggered. Scaling safety probes in AP-SOUTH to neutralize emergent bias."
                        : "NOMINAL: Systemic integrity verified. No manual intervention required for this sector."}
                    </p>
                  </Card>

                  <button className="w-full py-3 bg-primary text-primary-foreground rounded font-display font-bold text-xs uppercase tracking-widest hover:brightness-110 transition-all flex items-center justify-center gap-2">
                    <Maximize2 className="w-4 h-4" /> View Sector Trace
                  </button>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
