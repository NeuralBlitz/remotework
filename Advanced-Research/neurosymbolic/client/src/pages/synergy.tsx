import { Navigation } from "@/components/layout/Navigation";
import { SynergyGraph } from "@/components/governance/SynergyGraph";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { BrainCircuit, Cpu, Zap, Activity, Network, Layers, Share2 } from "lucide-react";
import { motion } from "framer-motion";
import { useSimulator } from "@/lib/store";
import { cn } from "@/lib/utils";

export default function SynergyEngine() {
  const { activeTokens, latency, activeModel } = useSimulator();

  return (
    <div className="min-h-screen bg-background text-foreground font-sans">
      <Navigation />
      <main className="md:pl-64 pt-16 md:pt-0 pb-24 md:pb-0 min-h-screen relative overflow-hidden">
        <div className="relative z-10 p-4 md:p-8 space-y-8">
          <header className="border-b border-white/10 pb-6">
            <h1 className="text-3xl font-display font-bold text-white tracking-tight flex items-center gap-3">
              <BrainCircuit className="text-primary" /> Synergy Engine Core
            </h1>
            <p className="text-muted-foreground mt-2 max-w-2xl font-display text-sm">
              The heart of the holistic neural architecture where systemic fusion and quantum alignment occur.
            </p>
          </header>

          <div className="grid grid-cols-12 gap-6">
            <div className="col-span-12 lg:col-span-8">
              <Card className="bg-black/40 border-primary/20 backdrop-blur-md h-[500px] relative overflow-hidden group">
                <CardHeader className="border-b border-white/10 flex flex-row justify-between items-center">
                  <div className="flex items-center gap-2">
                    <Layers className="w-4 h-4 text-primary" />
                    <CardTitle className="text-sm font-mono uppercase">Neural Fabric Visualization</CardTitle>
                  </div>
                  <div className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest">
                    Active Core: <span className="text-primary">{activeModel}</span>
                  </div>
                </CardHeader>
                <div className="flex-1 p-8">
                  <SynergyGraph />
                </div>
              </Card>
            </div>

            <div className="col-span-12 lg:col-span-4 space-y-6">
              <Card className="bg-black/40 border-white/10">
                <CardHeader className="py-3 px-4 border-b border-white/10">
                  <CardTitle className="text-xs font-mono text-primary flex items-center gap-2">
                    <Activity className="w-4 h-4" /> ENGINE TELEMETRY
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-6 space-y-6">
                  <div className="space-y-2">
                    <div className="flex justify-between text-[10px] font-mono uppercase text-muted-foreground">
                      <span>Quantum Coherence</span>
                      <span>99.98%</span>
                    </div>
                    <div className="w-full bg-white/5 h-1 rounded-full overflow-hidden">
                      <motion.div initial={{ width: 0 }} animate={{ width: "99.98%" }} className="h-full bg-primary" />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-[10px] font-mono uppercase text-muted-foreground">
                      <span>Synaptic Load</span>
                      <span>42.1%</span>
                    </div>
                    <div className="w-full bg-white/5 h-1 rounded-full overflow-hidden">
                      <motion.div initial={{ width: 0 }} animate={{ width: "42.1%" }} className="h-full bg-secondary" />
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4 pt-4">
                    <div className="p-3 bg-white/5 rounded border border-white/10 text-center">
                      <div className="text-[9px] font-mono text-muted-foreground uppercase mb-1">Latency</div>
                      <div className="text-lg font-mono text-primary">{latency}ms</div>
                    </div>
                    <div className="p-3 bg-white/5 rounded border border-white/10 text-center">
                      <div className="text-[9px] font-mono text-muted-foreground uppercase mb-1">Flux</div>
                      <div className="text-lg font-mono text-secondary">0.024</div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-primary/5 border-primary/20 p-6 space-y-4">
                <div className="flex items-center gap-3">
                   <div className="p-2 rounded bg-primary/20">
                     <Share2 className="w-5 h-5 text-primary" />
                   </div>
                   <div className="text-sm font-display font-bold text-white uppercase tracking-widest">Systemic Fusion</div>
                </div>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  Engine moves beyond simple modularity into a state of 'Systemic Fusion' by integrating advanced meta-cognitive tools for self-stabilization.
                </p>
                <button className="w-full py-2 bg-primary text-primary-foreground rounded font-display font-bold text-[10px] uppercase tracking-widest hover:brightness-110 transition-all">
                  Run Optimization
                </button>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
