import { Navigation } from "@/components/layout/Navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Settings, Shield, Lock, Bell, Cpu, Zap, Search, ChevronRight, Power, Sliders, AlertCircle } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";
import { useSimulator } from "@/lib/store";
import { cn } from "@/lib/utils";
import { toast } from "sonner";
import { Switch } from "@/components/ui/switch";
import { Slider } from "@/components/ui/slider";

interface ConfigItem {
  id: string;
  title: string;
  icon: any;
  desc: string;
  status: string;
  enabled: boolean;
  value: number;
}

export default function GovernanceConfig() {
  const { activeModel, setActiveModel, activeMode, setActiveMode } = useSimulator();
  const [search, setSearch] = useState("");
  const [configs, setConfigs] = useState<ConfigItem[]>([
    { id: "charter", title: "Charter Constraints", icon: Shield, desc: "Axiomatic alignment gates for neural output.", status: "STRICT", enabled: true, value: 95 },
    { id: "privacy", title: "Privacy Protocols", icon: Lock, desc: "Differential privacy epsilon budget management.", status: "ACTIVE", enabled: true, value: 82 },
    { id: "risk", title: "Risk Thresholds", icon: Bell, desc: "Sensitivity for automated drift detection.", status: "MODERATE", enabled: false, value: 45 },
    { id: "synergy", title: "Synergy Resonance", icon: Cpu, desc: "Inter-module coherence and fusion level.", status: "OPTIMIZED", enabled: true, value: 88 },
  ]);

  const toggleConfig = (id: string) => {
    setConfigs(prev => prev.map(c => 
      c.id === id ? { ...c, enabled: !c.enabled } : c
    ));
    const config = configs.find(c => c.id === id);
    toast.info(`${config?.title} ${!config?.enabled ? 'Activated' : 'Deactivated'}`);
  };

  const updateValue = (id: string, val: number[]) => {
    setConfigs(prev => prev.map(c => 
      c.id === id ? { ...c, value: val[0] } : c
    ));
  };

  const filtered = configs.filter(s => 
    s.title.toLowerCase().includes(search.toLowerCase()) || 
    s.desc.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30">
      <Navigation />
      <main className="md:pl-64 pt-16 md:pt-0 pb-24 md:pb-0 min-h-screen relative overflow-hidden">
        {/* Decorative Grid */}
        <div className="absolute inset-0 bg-grid-white/[0.02] bg-[length:32px_32px] pointer-events-none" />
        
        <div className="relative z-10 p-4 md:p-8 space-y-6">
          <header className="border-b border-white/10 pb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl font-display font-bold text-white tracking-tight flex items-center gap-3">
                <Settings className="text-primary" /> Governance Configuration
              </h1>
              <p className="text-muted-foreground mt-2 max-w-2xl font-display text-sm">
                Fine-tune the 'Governance-as-Code' engine parameters and active neural limiters.
              </p>
            </div>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input 
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search parameters..." 
                className="bg-white/5 border border-white/10 rounded-full py-2 pl-10 pr-4 text-xs font-mono focus:outline-none focus:border-primary/50 transition-all w-full md:w-64"
              />
            </div>
          </header>

          <div className="grid grid-cols-12 gap-6">
            {/* Core Runtimes */}
            <Card className="col-span-12 bg-black/40 border-primary/20 backdrop-blur-md">
              <CardHeader className="py-3 px-4 border-b border-white/10 flex justify-between items-center">
                <CardTitle className="text-xs font-mono text-primary flex items-center gap-2">
                  <Sliders className="w-4 h-4" /> ACTIVE RUNTIME DEPLOYMENT
                </CardTitle>
                <div className="text-[10px] font-mono text-green-400 flex items-center gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                  STABLE_DEPLOY
                </div>
              </CardHeader>
              <CardContent className="p-6 grid grid-cols-1 md:grid-cols-2 gap-8">
                 <div className="space-y-4">
                    <label className="text-[10px] font-mono text-muted-foreground uppercase tracking-[0.2em] block">Inference Architecture</label>
                    <div className="grid grid-cols-1 gap-2">
                       {["Synergy-v9.8-Quantum", "Aegis-v4-Stable", "Blitz-x1-Pro"].map(m => (
                         <button 
                           key={m}
                           onClick={() => { setActiveModel(m); toast.success(`Core Shift: ${m}`); }}
                           className={cn(
                             "w-full text-left px-4 py-3 rounded border font-mono text-sm transition-all flex justify-between items-center group",
                             activeModel === m ? "bg-primary/10 border-primary text-primary" : "bg-white/2 border-white/5 text-muted-foreground hover:bg-white/5"
                           )}
                         >
                           <span>{m}</span>
                           <ChevronRight className={cn("w-4 h-4 transition-transform", activeModel === m ? "translate-x-0" : "-translate-x-2 opacity-0 group-hover:opacity-100 group-hover:translate-x-0")} />
                         </button>
                       ))}
                    </div>
                 </div>
                 <div className="space-y-4">
                    <label className="text-[10px] font-mono text-muted-foreground uppercase tracking-[0.2em] block">Ethical Mode</label>
                    <div className="grid grid-cols-2 gap-2">
                       {["Holistic", "Restricted", "Debug", "Burst"].map(m => (
                         <button 
                           key={m}
                           onClick={() => { setActiveMode(m); toast.success(`Inference Mode: ${m}`); }}
                           className={cn(
                             "text-center px-4 py-3 rounded border font-mono text-xs transition-all",
                             activeMode === m ? "bg-secondary/10 border-secondary text-secondary" : "bg-white/2 border-white/5 text-muted-foreground hover:bg-white/5"
                           )}
                         >
                           {m}
                         </button>
                       ))}
                    </div>
                 </div>
              </CardContent>
            </Card>

            {/* Config Cards */}
            {filtered.map((s, i) => (
              <motion.div
                key={s.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="col-span-12 md:col-span-6"
              >
                <Card className={cn(
                  "bg-black/40 border-white/10 hover:border-primary/30 transition-all group overflow-hidden relative h-full",
                  !s.enabled && "opacity-60 grayscale-[0.5]"
                )}>
                  {!s.enabled && (
                    <div className="absolute top-3 right-3 z-20">
                      <div className="flex items-center gap-1.5 px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/20 text-[9px] font-mono text-amber-500">
                        <AlertCircle className="w-3 h-3" /> BYPASSED
                      </div>
                    </div>
                  )}
                  <CardHeader className="flex flex-row items-center justify-between pb-2">
                    <div className="flex items-center gap-3">
                      <div className={cn(
                        "p-2 rounded transition-all",
                        s.enabled ? "bg-primary/10 text-primary" : "bg-white/5 text-muted-foreground"
                      )}>
                        <s.icon className="w-5 h-5" />
                      </div>
                      <div>
                        <CardTitle className="text-lg font-display text-white">{s.title}</CardTitle>
                        <div className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest">{s.status}</div>
                      </div>
                    </div>
                    <Switch 
                      checked={s.enabled} 
                      onCheckedChange={() => toggleConfig(s.id)}
                      className="data-[state=checked]:bg-primary"
                    />
                  </CardHeader>
                  <CardContent className="space-y-6 pt-2">
                    <p className="text-xs text-muted-foreground font-display leading-relaxed">{s.desc}</p>
                    
                    <div className="space-y-3">
                       <div className="flex justify-between text-[9px] font-mono uppercase">
                          <span className="text-muted-foreground">Calibration Strength</span>
                          <span className={s.enabled ? "text-primary" : "text-muted-foreground"}>{s.value}%</span>
                       </div>
                       <Slider 
                         value={[s.value]} 
                         onValueChange={(val) => updateValue(s.id, val)}
                         disabled={!s.enabled}
                         max={100} 
                         step={1}
                         className={cn("[&_[role=slider]]:h-3 [&_[role=slider]]:w-3", s.enabled ? "[&_[role=slider]]:bg-primary" : "[&_[role=slider]]:bg-muted")}
                       />
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>

          {/* Global Deploy CTA */}
          <div className="sticky bottom-6 z-20 md:bottom-8">
            <Card className="bg-primary/10 border-primary/30 backdrop-blur-xl p-6 flex flex-col md:flex-row items-center justify-between gap-6 shadow-[0_0_50px_rgba(0,0,0,0.5)] border-t-primary/50">
              <div className="flex items-center gap-5">
                <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center border border-primary/30 shadow-[0_0_15px_rgba(0,255,255,0.2)]">
                  <Zap className="text-primary w-6 h-6 animate-pulse" />
                </div>
                <div>
                  <h3 className="text-white font-display font-bold text-lg tracking-tight uppercase">Push Systemic Fusion</h3>
                  <p className="text-xs text-muted-foreground font-mono">HASH: 0x9a2f...11b0 • ACTIVE_NODES: 1,284</p>
                </div>
              </div>
              <button 
                onClick={() => {
                  toast.success("SYSTEMIC FUSION DEPLOYED", { 
                    description: "Global synchronization complete across 1,284 inference nodes.",
                    duration: 5000
                  });
                }}
                className="w-full md:w-auto bg-primary text-primary-foreground px-10 py-4 rounded-md font-display font-bold text-xs uppercase tracking-[0.2em] hover:scale-[1.02] active:scale-95 transition-all shadow-[0_0_20px_rgba(0,255,255,0.3)] flex items-center justify-center gap-3"
              >
                <Power className="w-4 h-4" />
                Deploy Global Config
              </button>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}
