import { Navigation } from "@/components/layout/Navigation";
import { CharterLayer } from "@/components/governance/CharterLayer";
import { SynergyGraph } from "@/components/governance/SynergyGraph";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Activity, MessageSquare, AlertOctagon, Zap, Terminal, Code, Cpu, RefreshCw, Database, ChevronRight, Play, Settings2, Search, Network, ShieldCheck } from "lucide-react";
import bgImage from "@assets/generated_images/abstract_neural_network_governance_background.png";
import { useState, useEffect } from "react";
import { useSimulator } from "@/lib/store";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

export default function Dashboard() {
  const { blitzStatus, activeModel, activeMode, logs, activeTokens, latency, setBlitzStatus, setActiveMode, addLog } = useSimulator();
  const [activeNodes, setActiveNodes] = useState(1284);

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveNodes(prev => prev + Math.floor(Math.random() * 5) - 2);
    }, 10000);
    return () => clearInterval(interval);
  }, []);

  const runBurst = () => {
    setBlitzStatus("BURST");
    setActiveMode("Burst");
    toast.success("BURST MODE ACTIVATED", { description: "Quantum nodes scaling to max." });
    addLog({ msg: "Burst mode initiated", category: "neural", type: "success", details: "Manual override triggered for high-performance testing." });
    setTimeout(() => {
      setBlitzStatus("OPERATIONAL");
      setActiveMode("Holistic");
    }, 5000);
  };

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30">
      <Navigation />
      
      <main className="md:pl-64 pt-16 md:pt-0 pb-24 md:pb-0 min-h-screen relative overflow-hidden">
        <div className="absolute inset-0 bg-grid-white/[0.02] bg-[length:32px_32px] pointer-events-none" />
        
        <div className="relative z-10 p-4 md:p-8 space-y-6">
          <header className="flex flex-col xl:flex-row xl:items-center justify-between gap-6 border-b border-white/10 pb-6">
            <div className="space-y-1">
              <h1 className="text-3xl md:text-5xl font-display font-bold text-white tracking-tighter uppercase italic">
                AEGIS <span className="text-primary">Control</span>
              </h1>
              <p className="text-xs text-muted-foreground font-mono uppercase tracking-widest">
                Nodes: <span className="text-primary">{activeNodes.toLocaleString()}</span> • {activeModel}
              </p>
            </div>

            <div className="flex flex-wrap gap-4">
              <Card className="bg-white/5 border-white/10 px-4 py-2 flex items-center gap-4">
                <div className="text-right">
                  <div className="text-[9px] font-mono text-muted-foreground uppercase">Tokens</div>
                  <div className="text-lg font-mono text-primary">{(activeTokens / 10).toFixed(1)}k/s</div>
                </div>
                <div className="w-px h-8 bg-white/10" />
                <div className="text-right">
                  <div className="text-[9px] font-mono text-muted-foreground uppercase">Latency</div>
                  <div className="text-lg font-mono text-secondary">{latency}ms</div>
                </div>
              </Card>
              <button 
                onClick={runBurst}
                className={cn(
                  "px-6 py-3 rounded font-display font-bold text-xs uppercase tracking-widest transition-all",
                  blitzStatus === "BURST" ? "bg-primary text-primary-foreground animate-pulse" : "bg-primary/10 border border-primary/30 text-primary hover:bg-primary/20"
                )}
              >
                <Zap className="w-4 h-4 inline mr-2" /> {blitzStatus === "BURST" ? "BURSTING" : "BURST"}
              </button>
            </div>
          </header>

          <div className="grid grid-cols-12 gap-6">
            <div className="col-span-12 lg:col-span-4 space-y-6">
              <CharterLayer />
              <Card className="bg-black/40 border-white/10 p-6 flex flex-col items-center justify-center text-center group transition-colors hover:border-primary/30">
                 <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                   <ShieldCheck className="w-8 h-8 text-primary" />
                 </div>
                 <h2 className="text-2xl font-display font-bold text-white mb-1">99.92%</h2>
                 <p className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest">Global Compliance</p>
              </Card>
            </div>

            <div className="col-span-12 lg:col-span-8 space-y-6">
               <Card className="bg-black/40 border-white/10 h-[450px] relative overflow-hidden flex flex-col">
                 <CardHeader className="py-3 px-4 border-b border-white/10 flex justify-between items-center bg-white/2">
                   <div className="flex items-center gap-2">
                     <Network className="w-4 h-4 text-primary" />
                     <span className="text-xs font-mono uppercase tracking-widest">Neural Core Telemetry</span>
                   </div>
                 </CardHeader>
                 <div className="flex-1">
                   <SynergyGraph />
                 </div>
               </Card>

               <Card className="bg-black/60 border-white/10 flex flex-col h-[250px]">
                <CardHeader className="p-3 border-b border-white/10 flex justify-between items-center bg-white/2">
                  <div className="flex items-center gap-2">
                    <Terminal className="w-4 h-4 text-primary" />
                    <span className="text-xs font-mono uppercase tracking-widest">Live Integration Feed</span>
                  </div>
                </CardHeader>
                <ScrollArea className="flex-1 p-2">
                  <div className="space-y-0.5">
                    {logs.slice().reverse().map(log => (
                      <div key={log.id} className="text-[10px] font-mono p-1 hover:bg-white/5 rounded flex gap-2">
                        <span className="text-muted-foreground shrink-0">[{log.time}]</span>
                        <span className={cn("shrink-0 uppercase font-bold", log.type === 'success' ? 'text-primary' : 'text-white/40')}>{log.category}</span>
                        <span className="truncate text-white/70">{log.msg}</span>
                      </div>
                    ))}
                  </div>
                </ScrollArea>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
