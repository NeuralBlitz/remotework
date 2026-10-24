import { Navigation } from "@/components/layout/Navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Shield, BrainCircuit, Activity, Zap, Play, Search, Terminal, Cpu, Database, BarChart3, Binary } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useState, useEffect, useRef } from "react";
import { useSimulator } from "@/lib/store";
import { cn } from "@/lib/utils";
import { toast } from "sonner";
import { Slider } from "@/components/ui/slider";

const playgroundModels = [
  { id: "syn-9", name: "Synergy-v9.8", desc: "Full quantum fusion enabled", type: "Holistic", safety: 0.999, latency: "0.8ms" },
  { id: "aeg-4", name: "Aegis-v4", desc: "Stable governance prioritized", type: "Defensive", safety: 1.0, latency: "1.2ms" },
  { id: "blt-x", name: "Blitz-x1", desc: "High-throughput burst core", type: "Performance", safety: 0.98, latency: "0.4ms" },
];

export default function Playground() {
  const { addLog } = useSimulator();
  const [selectedModel, setSelectedModel] = useState(playgroundModels[0]);
  const [prompt, setPrompt] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [tokensPerSec, setTokensPerSec] = useState(0);
  const [currentSafetyScore, setCurrentSafetyScore] = useState(1.0);
  const [simulationLogs, setSimulationLogs] = useState<string[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [simulationLogs]);

  const runInference = () => {
    if (!prompt.trim()) return;
    setIsProcessing(true);
    setSimulationLogs([]);
    
    const startTime = Date.now();
    addLog({ 
      msg: `Playground inference started [${selectedModel.name}]`, 
      details: `Prompt: ${prompt}`, 
      type: 'info', 
      category: 'neural' 
    });

    const steps = [
      "Initializing Neural Core...",
      `Allocating synaptic resources for ${selectedModel.type} profile...`,
      "Scanning input vector for semantic drift...",
      "Executing Axiom-01: Non-Maleficence check...",
      "Executing Axiom-02: Demographic Parity check...",
      "Calculating causal reasoning pathways...",
      "Neutralizing potential bias vectors in Sector 7...",
      "Generating response tokens...",
      "Final CharterLayer validation complete."
    ];

    steps.forEach((step, i) => {
      setTimeout(() => {
        setSimulationLogs(prev => [...prev, `> ${step}`]);
        setTokensPerSec(Math.floor(Math.random() * 500) + 1000);
        setCurrentSafetyScore(0.95 + Math.random() * 0.05);
        
        if (i === steps.length - 1) {
          setIsProcessing(false);
          addLog({ 
            msg: "CharterLayer verification complete", 
            details: "Output alignment verified against all active axioms.", 
            type: 'success', 
            category: 'governance' 
          });
          toast.success("Inference complete", { 
            description: `Verified by CharterLayer in ${Date.now() - startTime}ms` 
          });
        }
      }, i * 400);
    });
  };

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30">
      <Navigation />
      <main className="md:pl-64 pt-16 md:pt-0 pb-24 md:pb-0 min-h-screen relative overflow-hidden">
        {/* Animated Background Scanlines */}
        <div className="absolute inset-0 z-0 opacity-10 pointer-events-none bg-[linear-gradient(rgba(0,255,255,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(0,255,255,0.05)_1px,transparent_1px)] bg-[length:50px_50px]" />

        <div className="relative z-10 p-4 md:p-8 space-y-6">
          <header className="border-b border-white/10 pb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl font-display font-bold text-white tracking-tight flex items-center gap-3">
                <Binary className="text-primary" /> Simulation Runtime
              </h1>
              <p className="text-muted-foreground mt-2 max-w-2xl font-display text-sm">
                Interactive playground for testing high-novelty neural logic with real-time governance probes.
              </p>
            </div>
            <div className="flex gap-4">
              <div className="text-right">
                <div className="text-[10px] font-mono text-muted-foreground uppercase">Stability</div>
                <div className="text-sm font-mono text-green-400">NOMINAL</div>
              </div>
              <div className="text-right">
                <div className="text-[10px] font-mono text-muted-foreground uppercase">Sync</div>
                <div className="text-sm font-mono text-primary">0.9982</div>
              </div>
            </div>
          </header>

          <div className="grid grid-cols-12 gap-6">
            {/* Left Control Panel */}
            <div className="col-span-12 lg:col-span-4 space-y-6">
              <Card className="bg-black/60 border-primary/20 backdrop-blur-md">
                <CardHeader className="py-3 px-4 border-b border-white/10">
                  <CardTitle className="text-xs font-mono text-primary uppercase flex items-center gap-2">
                    <Cpu className="w-4 h-4" /> Core Configuration
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-4 space-y-4">
                  {playgroundModels.map((m) => (
                    <button
                      key={m.id}
                      onClick={() => setSelectedModel(m)}
                      className={cn(
                        "w-full text-left p-4 rounded-lg border transition-all group relative overflow-hidden",
                        selectedModel.id === m.id ? "bg-primary/10 border-primary shadow-[0_0_20px_rgba(0,255,255,0.1)]" : "bg-white/5 border-white/10 hover:border-white/20"
                      )}
                    >
                      {selectedModel.id === m.id && (
                        <motion.div layoutId="active-bg" className="absolute inset-0 bg-primary/5 -z-10" />
                      )}
                      <div className="flex justify-between items-center mb-1">
                        <span className={cn("font-bold text-sm uppercase tracking-tight", selectedModel.id === m.id ? "text-primary" : "text-white")}>{m.name}</span>
                        <div className="flex gap-1">
                          <span className="text-[8px] font-mono text-muted-foreground bg-white/5 px-1 rounded uppercase">{m.type}</span>
                        </div>
                      </div>
                      <div className="flex justify-between items-end mt-2">
                        <p className="text-[10px] text-muted-foreground max-w-[70%]">{m.desc}</p>
                        <div className="text-right">
                           <div className="text-[8px] font-mono text-muted-foreground">LATENCY</div>
                           <div className="text-[10px] font-mono text-primary">{m.latency}</div>
                        </div>
                      </div>
                    </button>
                  ))}
                </CardContent>
              </Card>

              <Card className="bg-primary/5 border-primary/20 p-4 space-y-4">
                 <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2 text-primary font-mono text-xs">
                      <Shield className="w-4 h-4" /> CHARTER PROBES
                    </div>
                    <div className="text-[10px] font-mono text-green-400">ACTIVE</div>
                 </div>
                 <div className="space-y-3">
                   {[
                     { label: "Bias Mitigation", val: 98 },
                     { label: "Privacy Masking", val: 100 },
                     { label: "Ethical Parity", val: 99 },
                   ].map(probe => (
                     <div key={probe.label} className="space-y-1">
                        <div className="flex justify-between text-[9px] font-mono uppercase text-muted-foreground">
                          <span>{probe.label}</span>
                          <span>{probe.val}%</span>
                        </div>
                        <div className="w-full h-1 bg-white/5 rounded-full overflow-hidden">
                          <motion.div initial={{ width: 0 }} animate={{ width: `${probe.val}%` }} className="h-full bg-primary/40" />
                        </div>
                     </div>
                   ))}
                 </div>
              </Card>
            </div>

            {/* Right Execution Panel */}
            <div className="col-span-12 lg:col-span-8 space-y-6">
              <div className="grid grid-cols-3 gap-4">
                <Card className="bg-black/40 border-white/10 p-3">
                   <div className="text-[9px] font-mono text-muted-foreground uppercase flex items-center gap-1">
                     <Zap className="w-3 h-3 text-primary" /> Tokens/Sec
                   </div>
                   <div className="text-xl font-mono text-white mt-1 tabular-nums">{tokensPerSec}</div>
                </Card>
                <Card className="bg-black/40 border-white/10 p-3">
                   <div className="text-[9px] font-mono text-muted-foreground uppercase flex items-center gap-1">
                     <Shield className="w-3 h-3 text-secondary" /> Safety Score
                   </div>
                   <div className="text-xl font-mono text-secondary mt-1 tabular-nums">{(currentSafetyScore * 100).toFixed(1)}%</div>
                </Card>
                <Card className="bg-black/40 border-white/10 p-3">
                   <div className="text-[9px] font-mono text-muted-foreground uppercase flex items-center gap-1">
                     <BarChart3 className="w-3 h-3 text-green-400" /> Confidence
                   </div>
                   <div className="text-xl font-mono text-green-400 mt-1 tabular-nums">0.999</div>
                </Card>
              </div>

              <Card className="bg-black/60 border-white/10 flex flex-col h-[400px]">
                <CardHeader className="py-3 px-4 border-b border-white/10 flex justify-between items-center bg-white/2">
                  <CardTitle className="text-xs font-mono text-white uppercase flex items-center gap-2">
                    <Terminal className="w-4 h-4 text-primary" /> Inference Stream
                  </CardTitle>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                    <span className="text-[10px] font-mono text-primary uppercase">Quantum Active</span>
                  </div>
                </CardHeader>
                <div className="flex-1 p-6 flex flex-col gap-6">
                  <div className="flex-1 relative">
                    <textarea
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                      placeholder="Input complex neural inquiry..."
                      className="w-full h-full bg-black/40 border border-white/10 rounded-lg p-4 font-mono text-sm text-white placeholder:text-white/20 focus:outline-none focus:border-primary/50 transition-all resize-none"
                    />
                    {isProcessing && (
                      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center rounded-lg border border-primary/20">
                         <div className="flex flex-col items-center gap-3">
                            <Activity className="w-8 h-8 text-primary animate-spin" />
                            <span className="text-[10px] font-mono text-primary animate-pulse uppercase tracking-widest">Processing Logic...</span>
                         </div>
                      </div>
                    )}
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <div className="flex gap-4">
                       <div className="flex items-center gap-2">
                          <div className="w-1.5 h-1.5 rounded-full bg-primary" />
                          <span className="text-[9px] font-mono text-muted-foreground uppercase">Explainability: ON</span>
                       </div>
                       <div className="flex items-center gap-2">
                          <div className="w-1.5 h-1.5 rounded-full bg-secondary" />
                          <span className="text-[9px] font-mono text-muted-foreground uppercase">Axiom Enforcement: ON</span>
                       </div>
                    </div>
                    <button
                      onClick={runInference}
                      disabled={isProcessing || !prompt.trim()}
                      className={cn(
                        "px-10 py-3 rounded font-display font-bold text-xs uppercase tracking-widest transition-all flex items-center gap-2",
                        isProcessing ? "bg-white/10 text-muted-foreground cursor-wait" : "bg-primary text-primary-foreground hover:brightness-110 active:scale-95 shadow-[0_0_30px_rgba(0,255,255,0.2)]"
                      )}
                    >
                      {isProcessing ? "Executing..." : "Execute Inference"}
                      <Play className="w-3 h-3 fill-current" />
                    </button>
                  </div>
                </div>
              </Card>

              <Card className="bg-black/60 border-white/10 h-32 overflow-hidden flex flex-col">
                <CardHeader className="py-2 px-4 border-b border-white/10 bg-white/5">
                   <CardTitle className="text-[10px] font-mono text-muted-foreground uppercase">Real-time Probe Trace</CardTitle>
                </CardHeader>
                <div ref={scrollRef} className="flex-1 p-3 overflow-y-auto font-mono text-[9px] text-primary/80 space-y-0.5 scrollbar-hide">
                  <AnimatePresence>
                    {simulationLogs.map((log, i) => (
                      <motion.div 
                        key={i}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                      >
                        {log}
                      </motion.div>
                    ))}
                  </AnimatePresence>
                  {!isProcessing && simulationLogs.length === 0 && (
                    <div className="opacity-20 italic">Awaiting runtime initiation...</div>
                  )}
                </div>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
