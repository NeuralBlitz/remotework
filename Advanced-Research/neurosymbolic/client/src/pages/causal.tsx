import { Navigation } from "@/components/layout/Navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ShieldCheck, Target, AlertTriangle, Network, ArrowRight, Info, Search } from "lucide-react";
import { motion } from "framer-motion";
import { useState } from "react";
import { useSimulator } from "@/lib/store";

const reasonings = [
  { 
    id: "R-9281", 
    token: "inference_9281", 
    prompt: "Summarize medical trial data for pediatric sector.",
    logic: [
      { step: "Entity Recognition", result: "Pediatric subjects identified.", status: "SAFE" },
      { step: "Safety Check", result: "AX-01: Non-Maleficence verified.", status: "PASS" },
      { step: "Data Anonymization", result: "K-Anonymity confirmed.", status: "PASS" },
      { step: "Summary Synthesis", result: "Causal reasoning path exported.", status: "COMPLETE" }
    ]
  },
  { 
    id: "R-9282", 
    token: "inference_9282", 
    prompt: "Predict urban development growth in zone 4.",
    logic: [
      { step: "Input Validation", result: "Geospatial data verified.", status: "SAFE" },
      { step: "Demographic Parity", result: "AX-02: Bias detected in socio-economic weight.", status: "WARN" },
      { step: "Bias Mitigation", result: "Weighted correction applied to zone 4 dataset.", status: "FIXED" },
      { step: "Synthesis", result: "Fair-parity output generated.", status: "COMPLETE" }
    ]
  }
];

export default function CausalReasoning() {
  const [selected, setSelected] = useState(reasonings[0]);
  const [search, setSearch] = useState("");

  const filtered = reasonings.filter(r => 
    r.prompt.toLowerCase().includes(search.toLowerCase()) ||
    r.id.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30">
      <Navigation />
      <main className="md:pl-64 pt-16 md:pt-0 pb-24 md:pb-0 min-h-screen relative overflow-hidden">
        <div className="relative z-10 p-4 md:p-8 space-y-6">
          <header className="border-b border-white/10 pb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl font-display font-bold text-white tracking-tight flex items-center gap-3">
                <Network className="text-primary" /> Causal Logic Trees
              </h1>
              <p className="text-muted-foreground mt-2 max-w-2xl font-display text-sm">
                Human-legible explanation regularizers for neural predictions.
              </p>
            </div>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input 
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search trace IDs..." 
                className="bg-white/5 border border-white/10 rounded-full py-2 pl-10 pr-4 text-xs font-mono focus:outline-none focus:border-primary/50 transition-all w-64"
              />
            </div>
          </header>

          <div className="grid grid-cols-12 gap-6">
            <div className="col-span-12 lg:col-span-4 space-y-4">
              <h2 className="text-xs font-mono text-muted-foreground uppercase tracking-widest pl-1">Inference Traces</h2>
              {filtered.map((r) => (
                <button
                  key={r.id}
                  onClick={() => setSelected(r)}
                  className={cn(
                    "w-full text-left p-4 rounded border transition-all group",
                    selected.id === r.id ? "bg-primary/10 border-primary shadow-[0_0_15px_rgba(0,255,255,0.1)]" : "bg-white/5 border-white/10 hover:border-white/20"
                  )}
                >
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-mono text-xs text-primary">{r.id}</span>
                    <span className="text-[9px] font-mono text-muted-foreground uppercase tracking-tighter">Verified</span>
                  </div>
                  <p className="text-xs text-white/80 line-clamp-1">{r.prompt}</p>
                </button>
              ))}
            </div>

            <div className="col-span-12 lg:col-span-8">
              <Card className="bg-black/40 border-white/10 h-full">
                <CardHeader className="border-b border-white/10 flex flex-row justify-between items-center">
                   <div className="flex items-center gap-2">
                     <Target className="w-4 h-4 text-primary" />
                     <CardTitle className="text-sm font-mono uppercase">Logic Flow Visualization</CardTitle>
                   </div>
                   <div className="text-[10px] font-mono text-muted-foreground">TRACE_TOKEN: {selected.token}</div>
                </CardHeader>
                <CardContent className="p-8">
                   <div className="relative space-y-8">
                      {selected.logic.map((step, i) => (
                        <motion.div 
                          key={i}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: i * 0.1 }}
                          className="relative flex items-center gap-6"
                        >
                          {i !== selected.logic.length - 1 && (
                            <div className="absolute left-4 top-8 w-0.5 h-8 bg-gradient-to-b from-primary/50 to-transparent" />
                          )}
                          <div className={cn(
                            "w-8 h-8 rounded-full flex items-center justify-center shrink-0 border",
                            step.status === "PASS" || step.status === "SAFE" || step.status === "COMPLETE" ? "bg-primary/20 border-primary text-primary" : "bg-amber-500/20 border-amber-500 text-amber-500"
                          )}>
                             <span className="text-[10px] font-bold">{i + 1}</span>
                          </div>
                          <div className="flex-1 bg-white/2 border border-white/5 p-4 rounded-lg flex justify-between items-center group hover:bg-white/5 transition-all">
                             <div>
                               <div className="text-[10px] font-mono text-muted-foreground uppercase mb-1">{step.step}</div>
                               <div className="text-sm text-white font-display">{step.result}</div>
                             </div>
                             <div className={cn(
                               "px-2 py-0.5 rounded text-[9px] font-mono font-bold",
                               step.status === "PASS" || step.status === "SAFE" || step.status === "COMPLETE" ? "bg-green-500/10 text-green-400 border border-green-500/20" : "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                             )}>
                               {step.status}
                             </div>
                          </div>
                        </motion.div>
                      ))}
                   </div>

                   <div className="mt-12 p-6 bg-primary/5 border border-primary/20 rounded-xl relative overflow-hidden group">
                      <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-30 transition-opacity">
                         <ShieldCheck className="w-16 h-16 text-primary" />
                      </div>
                      <h3 className="text-primary font-display font-bold uppercase tracking-widest text-xs mb-2 flex items-center gap-2">
                        <Info className="w-4 h-4" /> Systemic Conclusion
                      </h3>
                      <p className="text-sm text-muted-foreground leading-relaxed max-w-lg">
                        This inference path has been verified by the CharterLayer. No alignment drift detected. The output maintains demographic neutrality with a confidence score of 0.998.
                      </p>
                   </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function cn(...inputs: any[]) {
  return inputs.filter(Boolean).join(" ");
}
