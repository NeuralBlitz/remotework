import { Navigation } from "@/components/layout/Navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Eye, Terminal, Search, ShieldCheck, Zap, Activity, Info } from "lucide-react";
import { useState, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useSimulator } from "@/lib/store";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { cn } from "@/lib/utils";

export default function EpistemicLog() {
  const { logs } = useSimulator();
  const [search, setSearch] = useState("");
  const [selectedLog, setSelectedLog] = useState<any>(null);
  
  const filtered = useMemo(() => 
    logs.filter(l => 
      l.msg.toLowerCase().includes(search.toLowerCase()) || 
      l.category.toLowerCase().includes(search.toLowerCase())
    ).reverse()
  , [logs, search]);

  return (
    <div className="min-h-screen bg-background text-foreground font-sans">
      <Navigation />
      <main className="md:pl-64 pt-16 md:pt-0 pb-24 md:pb-0 min-h-screen relative overflow-hidden">
        <div className="absolute inset-0 bg-grid-white/[0.01] pointer-events-none" />
        
        <div className="p-4 md:p-8 space-y-6 relative z-10">
          <header className="border-b border-white/10 pb-6 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl font-display font-bold text-white flex items-center gap-3">
                <Eye className="text-primary" /> Epistemic Inquiry
              </h1>
              <p className="text-sm text-muted-foreground mt-1">Live meta-cognitive trace of neural decision paths.</p>
            </div>
            <div className="relative w-full lg:w-80">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
              <input 
                value={search} 
                onChange={e => setSearch(e.target.value)} 
                placeholder="Search decision traces..." 
                className="w-full bg-white/5 border border-white/10 rounded-full py-2 pl-10 pr-4 text-xs focus:outline-none focus:border-primary/50" 
              />
            </div>
          </header>

          <div className="grid grid-cols-12 gap-6">
            <Card className="col-span-12 lg:col-span-8 bg-black/40 border-white/10 h-[650px] flex flex-col overflow-hidden">
              <CardHeader className="py-3 px-4 border-b border-white/10 bg-white/2 flex justify-between items-center">
                <span className="text-[10px] font-mono text-primary uppercase tracking-widest">Inquiry Stream</span>
                <div className="flex gap-2">
                   <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                   <span className="text-[9px] font-mono text-muted-foreground uppercase">Real-time Verified</span>
                </div>
              </CardHeader>
              <ScrollArea className="flex-1">
                <div className="divide-y divide-white/5">
                  <AnimatePresence initial={false}>
                    {filtered.map((log) => (
                      <motion.button 
                        key={log.id} 
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        onClick={() => setSelectedLog(log)} 
                        className="w-full text-left p-6 hover:bg-white/5 transition-all group flex items-start gap-6"
                      >
                        <div className="pt-1 shrink-0">
                          <div className={cn(
                            "w-1.5 h-1.5 rounded-full shadow-[0_0_8px]",
                            log.type === 'success' ? 'bg-primary shadow-primary/50' : 'bg-white/20 shadow-white/10'
                          )} />
                        </div>
                        <div className="space-y-1 flex-1">
                          <div className="flex items-center gap-3 mb-1">
                            <span className="font-mono text-[10px] text-muted-foreground">[{log.time}]</span>
                            <span className="text-[9px] font-mono bg-white/5 px-1.5 rounded text-white/40 uppercase tracking-tighter">{log.category}</span>
                          </div>
                          <p className="font-display text-white text-lg leading-tight group-hover:text-primary transition-colors">{log.msg}</p>
                        </div>
                        <Zap className="w-4 h-4 text-white/10 group-hover:text-primary/40 transition-all opacity-0 group-hover:opacity-100" />
                      </motion.button>
                    ))}
                  </AnimatePresence>
                </div>
              </ScrollArea>
            </Card>

            <div className="col-span-12 lg:col-span-4 space-y-6">
               <Card className="bg-primary/5 border-primary/20 p-6 space-y-4">
                  <div className="flex items-center gap-3">
                    <Info className="w-5 h-5 text-primary" />
                    <h3 className="text-white font-display font-bold uppercase tracking-widest text-xs">Axiomatic Trace</h3>
                  </div>
                  <p className="text-xs text-muted-foreground leading-relaxed italic">
                    "Epistemic inquiry represents the active cognitive loop where the model identifies and fills knowledge gaps, ensuring zero alignment drift."
                  </p>
                  <div className="pt-4 border-t border-white/5">
                    <div className="flex justify-between text-[10px] font-mono text-muted-foreground uppercase mb-2">
                       <span>Confidence Threshold</span>
                       <span className="text-primary">0.992</span>
                    </div>
                    <div className="w-full bg-white/5 h-1 rounded-full overflow-hidden">
                       <div className="h-full bg-primary w-[92%]" />
                    </div>
                  </div>
               </Card>

               <Card className="bg-black/40 border-white/10 p-6 text-center">
                  <Activity className="w-8 h-8 text-secondary mx-auto mb-3" />
                  <div className="text-3xl font-display font-bold text-white mb-1">84.2k</div>
                  <div className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest">Inquiries Processed /hr</div>
               </Card>
            </div>
          </div>
        </div>
      </main>

      <Dialog open={!!selectedLog} onOpenChange={() => setSelectedLog(null)}>
        <DialogContent className="bg-black/95 border-primary/30 backdrop-blur-xl text-white max-w-lg">
          <DialogHeader>
            <DialogTitle className="font-display font-bold text-xl uppercase tracking-tight flex items-center gap-3">
              <Terminal className="w-6 h-6 text-primary" /> Trace Diagnostic
            </DialogTitle>
            <DialogDescription className="font-mono text-[10px] text-muted-foreground">
              TIMESTAMP: {selectedLog?.time} • ENTITY: {selectedLog?.id?.slice(0, 8)}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-6 pt-4">
            <div className="bg-white/5 p-4 rounded border border-white/10">
              <div className="text-[9px] font-mono text-muted-foreground uppercase mb-1">Neural Intent</div>
              <div className="text-lg font-display text-white">{selectedLog?.msg}</div>
            </div>
            <div className="bg-white/5 p-4 rounded border border-white/10">
              <div className="text-[9px] font-mono text-muted-foreground uppercase mb-1">Execution Payload</div>
              <div className="text-sm font-mono text-white/70 italic leading-relaxed">
                "{selectedLog?.details || "No secondary payload identified for this inquiry."}"
              </div>
            </div>
            <div className="flex justify-end pt-2">
              <button onClick={() => setSelectedLog(null)} className="px-6 py-2 bg-primary text-primary-foreground font-display font-bold text-[10px] rounded uppercase tracking-widest hover:brightness-110 transition-all">
                Dismiss Trace
              </button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
