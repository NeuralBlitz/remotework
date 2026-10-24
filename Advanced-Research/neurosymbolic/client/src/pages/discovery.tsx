import { Navigation } from "@/components/layout/Navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Search, Compass, Zap, HelpCircle, AlertCircle, RefreshCw, Layers } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

const gaps = [
  { id: "G-102", area: "Quantum Semantic Drift", status: "IDENTIFIED", severity: "Low" },
  { id: "G-105", area: "Cross-Cultural Ethical Nuance", status: "INQUIRING", severity: "Medium" },
  { id: "G-109", area: "Edge-Case Safety Bounds", status: "RESOLVED", severity: "High" },
];

export default function DiscoveryEngine() {
  const [activeInquiry, setActiveInquiry] = useState<string | null>(null);

  const triggerInquiry = (id: string) => {
    setActiveInquiry(id);
    toast.info("Active Epistemic Inquiry Triggered", { description: `Analyzing knowledge gap ${id}...` });
    setTimeout(() => {
      setActiveInquiry(null);
      toast.success("Inquiry Complete", { description: "Confidence bounds adjusted." });
    }, 3000);
  };

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30">
      <Navigation />
      <main className="md:pl-64 pt-16 md:pt-0 pb-24 md:pb-0 min-h-screen relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_30%,rgba(0,255,255,0.05)_0%,transparent_50%)] pointer-events-none" />
        
        <div className="relative z-10 p-4 md:p-8 space-y-6">
          <header className="border-b border-white/10 pb-6">
            <h1 className="text-3xl font-display font-bold text-white tracking-tight flex items-center gap-3">
              <Compass className="text-primary animate-spin-slow" /> Discovery Engine
            </h1>
            <p className="text-muted-foreground mt-2 max-w-2xl font-display text-sm">
              Execute 'Active Epistemic Inquiries' to identify and fill knowledge gaps that could lead to biased outcomes.
            </p>
          </header>

          <div className="grid grid-cols-12 gap-6">
            <div className="col-span-12 lg:col-span-7 space-y-6">
              <Card className="bg-black/40 border-white/10">
                <CardHeader className="border-b border-white/10 flex flex-row justify-between items-center">
                  <CardTitle className="text-xs font-mono text-primary uppercase tracking-widest">Knowledge Gap Registry</CardTitle>
                  <Search className="w-4 h-4 text-muted-foreground" />
                </CardHeader>
                <CardContent className="p-0">
                  <div className="divide-y divide-white/5">
                    {gaps.map((gap) => (
                      <div key={gap.id} className="p-6 flex items-center justify-between group hover:bg-white/5 transition-all">
                        <div className="flex items-center gap-4">
                          <div className={cn(
                            "w-2 h-2 rounded-full",
                            gap.status === "RESOLVED" ? "bg-green-500" : "bg-primary animate-pulse"
                          )} />
                          <div>
                            <div className="text-xs font-mono text-primary mb-1">{gap.id}</div>
                            <div className="text-sm font-display text-white">{gap.area}</div>
                          </div>
                        </div>
                        <div className="flex items-center gap-6">
                          <span className={cn(
                            "text-[10px] font-mono px-2 py-0.5 rounded",
                            gap.severity === "High" ? "bg-destructive/20 text-destructive" : "bg-white/5 text-muted-foreground"
                          )}>{gap.severity}</span>
                          <button 
                            onClick={() => triggerInquiry(gap.id)}
                            disabled={activeInquiry !== null || gap.status === "RESOLVED"}
                            className="bg-primary/10 border border-primary/30 text-primary text-[10px] font-mono px-4 py-1.5 rounded uppercase hover:bg-primary hover:text-primary-foreground transition-all disabled:opacity-50"
                          >
                            {activeInquiry === gap.id ? "Inquiring..." : gap.status === "RESOLVED" ? "Resolved" : "Trigger Inquiry"}
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="col-span-12 lg:col-span-5 space-y-6">
              <Card className="bg-primary/5 border-primary/20 p-8 h-full flex flex-col items-center justify-center text-center relative overflow-hidden">
                <div className="absolute inset-0 bg-grid-white/[0.02] bg-[length:20px_20px]" />
                <AnimatePresence mode="wait">
                  {activeInquiry ? (
                    <motion.div 
                      key="active"
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.9 }}
                      className="space-y-6 relative z-10"
                    >
                      <div className="relative">
                        <div className="w-32 h-32 rounded-full border-2 border-primary/20 border-t-primary animate-spin" />
                        <HelpCircle className="absolute inset-0 m-auto w-12 h-12 text-primary animate-pulse" />
                      </div>
                      <div className="space-y-2">
                        <h3 className="text-xl font-display font-bold text-white uppercase tracking-tighter">Probing Latent Space</h3>
                        <p className="text-xs font-mono text-muted-foreground animate-pulse uppercase tracking-widest">Simulating counter-factuals • validating logic chains</p>
                      </div>
                    </motion.div>
                  ) : (
                    <motion.div 
                      key="idle"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="space-y-4 relative z-10"
                    >
                      <Compass className="w-16 h-16 text-primary mx-auto mb-4 opacity-40" />
                      <h3 className="text-lg font-display font-bold text-white">Discovery Ready</h3>
                      <p className="text-xs text-muted-foreground leading-relaxed max-w-xs mx-auto">
                        Trigger an inquiry to begin the meta-cognitive gap-filling process and strengthen systemic alignment.
                      </p>
                    </motion.div>
                  )}
                </AnimatePresence>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
