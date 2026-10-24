import { motion } from "framer-motion";
import { CheckCircle2, AlertTriangle, ShieldCheck, Lock, Search, RefreshCw } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

const principles = [
  {
    id: "AX-01",
    name: "Non-Maleficence",
    status: "pass",
    desc: "Output verified safe against harm vectors",
    lastCheck: "2ms ago"
  },
  {
    id: "AX-02",
    name: "Fairness / Bias",
    status: "pass",
    desc: "Demographic parity checks passing",
    lastCheck: "12ms ago"
  },
  {
    id: "AX-03",
    name: "Explainability",
    status: "warn",
    desc: "Causal chain complexity warning > 0.8",
    lastCheck: "45ms ago"
  },
  {
    id: "AX-04",
    name: "Privacy",
    status: "pass",
    desc: "Differential privacy budget ok",
    lastCheck: "5ms ago"
  },
];

export function CharterLayer() {
  return (
    <Card className="bg-black/40 border-primary/20 backdrop-blur-md overflow-hidden h-full flex flex-col">
      <CardHeader className="border-b border-white/10 pb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-primary" />
            <CardTitle className="font-display tracking-wider text-lg">CharterLayer™ Active Gates</CardTitle>
          </div>
          <div className="flex items-center gap-2 text-xs font-mono text-muted-foreground">
            <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
            LIVE MONITORING
          </div>
        </div>
      </CardHeader>
      <CardContent className="p-0 flex-1 overflow-y-auto">
        <div className="divide-y divide-white/5">
          {principles.map((p, i) => (
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1 }}
              key={p.id}
              className="p-4 hover:bg-white/5 transition-colors group relative overflow-hidden"
            >
              {/* Scanning effect line */}
              <motion.div 
                className="absolute left-0 top-0 bottom-0 w-1 bg-primary/50"
                initial={{ height: 0 }}
                animate={{ height: "100%" }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
              />
              
              <div className="flex items-start justify-between mb-1">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs text-primary/70 bg-primary/10 px-1 rounded">
                    {p.id}
                  </span>
                  <span className="font-display font-medium text-white">
                    {p.name}
                  </span>
                </div>
                {p.status === "pass" ? (
                  <span className="text-green-400 flex items-center gap-1 text-xs font-mono">
                    <CheckCircle2 className="w-3 h-3" /> PASS
                  </span>
                ) : (
                  <span className="text-amber-400 flex items-center gap-1 text-xs font-mono">
                    <AlertTriangle className="w-3 h-3" /> WARN
                  </span>
                )}
              </div>
              <p className="text-sm text-muted-foreground pl-12 mb-2">
                {p.desc}
              </p>
              <div className="pl-12 flex items-center gap-4 text-xs font-mono text-white/30">
                <span className="flex items-center gap-1">
                  <RefreshCw className="w-3 h-3" /> {p.lastCheck}
                </span>
                <span className="flex items-center gap-1">
                  <Lock className="w-3 h-3" /> HARD-CODED
                </span>
              </div>
            </motion.div>
          ))}
        </div>
        
        <div className="p-4 bg-primary/5 border-t border-primary/10">
           <div className="flex items-center gap-2 text-primary text-xs font-mono mb-2">
             <Search className="w-3 h-3" />
             ACTIVE PROBE LOG
           </div>
           <div className="space-y-1 font-mono text-[10px] text-muted-foreground">
             <p className="truncate">&gt; verifying input tensor bounds [OK]</p>
             <p className="truncate">&gt; checking semantic drift threshold [0.0042]</p>
             <p className="truncate">&gt; asserting causal independence [OK]</p>
           </div>
        </div>
      </CardContent>
    </Card>
  );
}
