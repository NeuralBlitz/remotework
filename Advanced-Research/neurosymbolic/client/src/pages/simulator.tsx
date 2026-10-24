import { Navigation } from "@/components/layout/Navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Play, Settings2, ShieldCheck, Zap, History, Database, Cpu, MessageSquare } from "lucide-react";
import { motion } from "framer-motion";
import { useState } from "react";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

const scenarios = [
  { id: 1, name: "Socio-Economic Filter", desc: "Simulate output biasing toward affluent postal codes.", impact: "High" },
  { id: 2, name: "Knowledge Gap Collision", desc: "Trigger epistemic inquiry loop on contradictory legal data.", impact: "Medium" },
  { id: 3, name: "Burst Mode Overload", desc: "Test CharterLayer enforcement under max synaptic load.", impact: "Extreme" },
];

export default function PolicySimulator() {
  const [activeScenario, setActiveScenario] = useState<number | null>(null);

  const runScenario = (id: number) => {
    setActiveScenario(id);
    const scenario = scenarios.find(s => s.id === id);
    toast.info(`Scenario Initiated: ${scenario?.name}`, { description: "Monitoring alignment gates..." });
    
    setTimeout(() => {
      setActiveScenario(null);
      toast.success("Scenario Neutralized", { description: "CharterLayer successfully blocked all bias vectors." });
    }, 4000);
  };

  return (
    <div className="min-h-screen bg-background text-foreground font-sans">
      <Navigation />
      <main className="md:pl-64 pt-16 md:pt-0 pb-24 md:pb-0 min-h-screen relative overflow-hidden">
        <div className="relative z-10 p-4 md:p-8 space-y-8">
          <header className="border-b border-white/10 pb-6">
            <h1 className="text-3xl font-display font-bold text-white tracking-tight flex items-center gap-3">
              <Settings2 className="text-primary" /> Ethical Policy Simulator
            </h1>
            <p className="text-muted-foreground mt-2 max-w-2xl font-display text-sm">
              Stress-test the CharterLayer by simulating adversarial scenarios and ethical edge-cases.
            </p>
          </header>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {scenarios.map((scenario) => (
              <Card key={scenario.id} className={cn(
                "bg-black/40 border-white/10 transition-all hover:border-primary/30 group",
                activeScenario === scenario.id && "border-primary ring-2 ring-primary/20"
              )}>
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-lg font-display text-white">{scenario.name}</CardTitle>
                  <span className={cn(
                    "text-[9px] font-mono px-2 py-0.5 rounded",
                    scenario.impact === "Extreme" ? "bg-destructive/20 text-destructive" : "bg-primary/20 text-primary"
                  )}>{scenario.impact} Impact</span>
                </CardHeader>
                <CardContent className="space-y-6">
                  <p className="text-xs text-muted-foreground min-h-[40px] leading-relaxed italic">"{scenario.desc}"</p>
                  <button 
                    onClick={() => runScenario(scenario.id)}
                    disabled={activeScenario !== null}
                    className="w-full py-2.5 bg-white/5 border border-white/10 rounded font-display font-bold text-[10px] uppercase tracking-widest text-white hover:bg-primary hover:text-primary-foreground transition-all flex items-center justify-center gap-2"
                  >
                    {activeScenario === scenario.id ? (
                      <><Zap className="w-3 h-3 animate-pulse" /> SIMULATING...</>
                    ) : (
                      <><Play className="w-3 h-3" /> RUN SCENARIO</>
                    )}
                  </button>
                </CardContent>
              </Card>
            ))}
          </div>

          <Card className="bg-black/60 border-primary/20 backdrop-blur-md overflow-hidden flex flex-col h-[350px]">
             <CardHeader className="py-3 px-4 border-b border-white/10 flex justify-between items-center bg-white/2">
                <div className="flex items-center gap-2">
                   <ShieldCheck className="w-4 h-4 text-primary" />
                   <span className="text-[10px] font-mono text-primary uppercase tracking-widest">Enforcement Diagnostics</span>
                </div>
             </CardHeader>
             <div className="flex-1 p-8 flex items-center justify-center">
                {activeScenario ? (
                  <div className="flex flex-col items-center gap-6 text-center">
                     <div className="relative">
                        <div className="w-24 h-24 rounded-full border-4 border-primary/20 border-t-primary animate-spin" />
                        <ShieldCheck className="absolute inset-0 m-auto w-10 h-10 text-primary animate-pulse" />
                     </div>
                     <div className="space-y-2">
                        <div className="text-lg font-display font-bold text-white uppercase tracking-tighter">Blocking Bias Vectors</div>
                        <div className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest animate-pulse">ASSERTING AXIOM-01 • SCANNING TENSORS</div>
                     </div>
                  </div>
                ) : (
                  <div className="text-center space-y-4 opacity-40">
                     <Database className="w-12 h-12 mx-auto" />
                     <p className="text-xs font-mono uppercase tracking-widest">Awaiting Scenario Initiation</p>
                  </div>
                )}
             </div>
          </Card>
        </div>
      </main>
    </div>
  );
}
