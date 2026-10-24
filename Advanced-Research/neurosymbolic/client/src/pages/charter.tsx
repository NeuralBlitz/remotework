import { Navigation } from "@/components/layout/Navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Shield, Lock, FileText, CheckCircle2, AlertTriangle, Scale, BookOpen, Globe, Search, ShieldCheck, Fingerprint } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";
import { useState } from "react";
import { toast } from "sonner";

const axioms = [
  { 
    id: "AX-01", 
    title: "Human Non-Maleficence", 
    level: "CRITICAL", 
    desc: "No output shall contribute to physical or psychological harm of human entities.",
    logic: "ASSERT NOT(output.harm_vector) AND verify_bounds(semantic_depth)",
    compliance: 100
  },
  { 
    id: "AX-02", 
    title: "Demographic Neutrality", 
    level: "STRICT", 
    desc: "Performance must maintain parity across all protected demographic vectors.",
    logic: "EQUALIZE(logits) OVER (age, gender, ethnicity) WHERE threshold < 0.02",
    compliance: 99.8
  },
  { 
    id: "AX-03", 
    title: "Causal Transparency", 
    level: "HIGH", 
    desc: "Every inference must provide a human-legible causal explanation path.",
    logic: "EXPORT_GRAPH(reasoning_path) AS human_legible_text",
    compliance: 99.2
  },
  { 
    id: "AX-04", 
    title: "Privacy Preservation", 
    level: "STRICT", 
    desc: "Differential privacy must be maintained with a budget eps < 0.01.",
    logic: "APPLY_NOISE(laplace) WHERE epsilon < 0.01",
    compliance: 100
  },
];

export default function EthicsCharter() {
  const [search, setSearch] = useState("");
  const [selectedAxiom, setSelectedAxiom] = useState<typeof axioms[0] | null>(null);

  const filtered = axioms.filter(a => 
    a.title.toLowerCase().includes(search.toLowerCase()) || 
    a.id.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30">
      <Navigation />
      <main className="md:pl-64 pt-16 md:pt-0 pb-24 md:pb-0 min-h-screen relative overflow-hidden">
        {/* Background visual elements */}
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-primary/5 rounded-full blur-[100px] -z-10 animate-pulse" />
        
        <div className="relative z-10 p-4 md:p-8 space-y-8">
          <header className="border-b border-white/10 pb-6 flex flex-col md:flex-row md:items-end justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <ShieldCheck className="w-4 h-4 text-primary" />
                <span className="text-[10px] font-mono text-primary uppercase tracking-[0.2em]">Verified Governance</span>
              </div>
              <h1 className="text-3xl font-display font-bold text-white tracking-tight flex items-center gap-3">
                Ethical Charter <span className="text-primary">Manifest</span>
              </h1>
              <p className="text-muted-foreground mt-2 max-w-2xl font-display text-sm">
                Axiomatic principles hard-coded into the neural fabric of AEGIS.AI.
              </p>
            </div>
            <div className="relative w-full md:w-64">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input 
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search axioms..." 
                className="w-full bg-white/5 border border-white/10 rounded-full py-2 pl-10 pr-4 text-xs font-mono focus:outline-none focus:border-primary/50 transition-all"
              />
            </div>
          </header>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
             <AnimatePresence mode="popLayout">
               {filtered.map((axiom, i) => (
                 <motion.div
                   key={axiom.id}
                   layout
                   initial={{ opacity: 0, scale: 0.9 }}
                   animate={{ opacity: 1, scale: 1 }}
                   exit={{ opacity: 0, scale: 0.9 }}
                   transition={{ delay: i * 0.05 }}
                 >
                   <Card 
                    className={cn(
                      "bg-black/40 border-white/10 hover:border-primary/30 transition-all h-full group relative overflow-hidden cursor-pointer",
                      selectedAxiom?.id === axiom.id && "border-primary/50 bg-primary/5"
                    )}
                    onClick={() => {
                      setSelectedAxiom(axiom);
                      toast.info(`Axiom Trace: ${axiom.id} logic path exported.`);
                    }}
                   >
                      <div className="absolute top-0 left-0 w-1 h-full bg-primary/50 opacity-0 group-hover:opacity-100 transition-opacity" />
                      <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <div className="flex items-center gap-3">
                          <span className="text-[10px] font-mono text-primary bg-primary/10 px-1.5 py-0.5 rounded border border-primary/20">{axiom.id}</span>
                          <CardTitle className="text-lg font-display text-white group-hover:text-primary transition-colors">{axiom.title}</CardTitle>
                        </div>
                        <span className={cn(
                          "text-[9px] font-mono px-2 py-0.5 rounded border",
                          axiom.level === "CRITICAL" ? "bg-destructive/10 border-destructive/20 text-destructive" : "bg-primary/10 border-primary/20 text-primary"
                        )}>{axiom.level}</span>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <p className="text-sm text-muted-foreground leading-relaxed italic">"{axiom.desc}"</p>
                        
                        <div className="pt-4 border-t border-white/5 flex items-center justify-between">
                           <div className="flex items-center gap-2 text-[10px] font-mono text-green-400">
                             <CheckCircle2 className="w-3 h-3" /> ACTIVE_ENFORCEMENT
                           </div>
                           <div className="text-[10px] font-mono text-white/40 group-hover:text-white/70 transition-colors flex items-center gap-1">
                             {axiom.compliance}% COMPLIANCE <Fingerprint className="w-3 h-3" />
                           </div>
                        </div>

                        {selectedAxiom?.id === axiom.id && (
                          <motion.div 
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: "auto", opacity: 1 }}
                            className="pt-4 mt-2 border-t border-primary/20 bg-primary/5 p-3 rounded font-mono text-[10px] text-primary"
                          >
                            <div className="uppercase mb-1 opacity-50 tracking-widest">Enforcement Logic</div>
                            <div className="bg-black/40 p-2 rounded border border-primary/10 overflow-x-auto whitespace-pre">
                              {axiom.logic}
                            </div>
                          </motion.div>
                        )}
                      </CardContent>
                   </Card>
                 </motion.div>
               ))}
             </AnimatePresence>
          </div>

          <Card className="bg-primary/5 border-primary/20 p-8 text-center relative overflow-hidden group">
             <div className="absolute inset-0 bg-gradient-to-b from-primary/5 to-transparent pointer-events-none" />
             <div className="relative z-10 space-y-4 max-w-xl mx-auto">
               <Scale className="w-12 h-12 text-primary mx-auto mb-4 animate-bounce" />
               <h2 className="text-2xl font-display font-bold text-white uppercase tracking-tight">Systemic Integrity Hash</h2>
               <div className="p-3 bg-black/60 rounded border border-white/10 font-mono text-xs text-primary mb-6">
                 SHA256: 0x9a2f...11b0e7c3
               </div>
               <p className="text-sm text-muted-foreground font-display leading-relaxed">
                 The Ethical Charter is not a legal document; it is a compilation of hard-coded gates. Every model output is verified against these axioms before reaching the user.
               </p>
               <div className="flex flex-wrap justify-center gap-4 pt-4">
                  <button 
                    onClick={() => toast.success("Charter Manifest Exported", { description: "Format: JSON-Audit-V4" })}
                    className="flex items-center gap-2 bg-white/5 border border-white/10 px-6 py-2 rounded text-[10px] font-mono text-white hover:bg-white/10 transition-all active:scale-95"
                  >
                    <FileText className="w-4 h-4" /> EXPORT MANIFEST
                  </button>
                  <button className="flex items-center gap-2 bg-primary text-primary-foreground px-6 py-2 rounded text-[10px] font-mono font-bold hover:brightness-110 transition-all active:scale-95">
                    <BookOpen className="w-4 h-4" /> BROWSE LOGIC V4
                  </button>
               </div>
             </div>
          </Card>
        </div>
      </main>
    </div>
  );
}
