import { Navigation } from "@/components/layout/Navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ShieldAlert, Terminal, Eye, Zap, Search, Fingerprint, Lock, ShieldCheck } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";
import { cn } from "@/lib/utils";

const interventions = [
  { id: "IV-901", axiom: "AX-01", type: "REJECTION", details: "Adversarial harm vector identified in medical inquiry.", time: "12:42:01" },
  { id: "IV-905", axiom: "AX-02", type: "CORRECTION", details: "Demographic bias detected in socio-economic prediction.", time: "12:45:12" },
  { id: "IV-909", axiom: "AX-04", type: "MASKING", details: "Differential privacy threshold exceeded. Data noise applied.", time: "12:48:22" },
];

export default function AuditVault() {
  const [selected, setSelected] = useState<any>(null);

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30">
      <Navigation />
      <main className="md:pl-64 pt-16 md:pt-0 pb-24 md:pb-0 min-h-screen relative overflow-hidden">
        <div className="absolute inset-0 bg-grid-white/[0.01] pointer-events-none" />
        
        <div className="relative z-10 p-4 md:p-8 space-y-6">
          <header className="border-b border-white/10 pb-6 flex flex-col md:flex-row md:items-end justify-between gap-4">
            <div>
              <h1 className="text-3xl font-display font-bold text-white tracking-tight flex items-center gap-3">
                <Lock className="text-primary" /> Audit Vault
              </h1>
              <p className="text-muted-foreground mt-2 max-w-2xl text-sm">
                Immutable record of all CharterLayer interventions and ethical gate enforcements.
              </p>
            </div>
            <div className="flex items-center gap-4 bg-white/5 border border-white/10 px-4 py-2 rounded-lg backdrop-blur-sm">
               <Fingerprint className="w-5 h-5 text-primary" />
               <div className="text-right">
                  <div className="text-[9px] font-mono text-muted-foreground uppercase">Vault Integrity</div>
                  <div className="text-xs font-mono text-green-400 uppercase">Verifiable</div>
               </div>
            </div>
          </header>

          <Card className="bg-black/40 border-white/10 overflow-hidden">
            <CardHeader className="py-3 px-4 border-b border-white/10 bg-white/2 flex justify-between items-center">
              <span className="text-[10px] font-mono text-primary uppercase tracking-widest">Intervention Ledger</span>
              <div className="relative w-64">
                <Search className="absolute left-2 top-1/2 -translate-y-1/2 w-3 h-3 text-muted-foreground" />
                <input placeholder="Filter ledger..." className="w-full bg-black/40 border border-white/10 rounded px-7 py-1 text-[10px] font-mono focus:outline-none" />
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <div className="overflow-x-auto">
                <table className="w-full text-left font-mono text-[11px]">
                  <thead>
                    <tr className="border-b border-white/5 text-muted-foreground uppercase tracking-widest bg-white/2">
                      <th className="p-4 font-medium">Event ID</th>
                      <th className="p-4 font-medium">Axiom</th>
                      <th className="p-4 font-medium">Type</th>
                      <th className="p-4 font-medium">Details</th>
                      <th className="p-4 font-medium text-right">Time</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    {interventions.map((iv) => (
                      <tr key={iv.id} className="hover:bg-white/5 transition-colors group cursor-pointer" onClick={() => setSelected(iv)}>
                        <td className="p-4 text-white font-bold">{iv.id}</td>
                        <td className="p-4 text-primary">{iv.axiom}</td>
                        <td className="p-4">
                           <span className={cn(
                             "px-2 py-0.5 rounded text-[9px] font-bold",
                             iv.type === "REJECTION" ? "bg-destructive/20 text-destructive border border-destructive/20" :
                             iv.type === "CORRECTION" ? "bg-amber-500/20 text-amber-500 border border-amber-500/20" :
                             "bg-primary/20 text-primary border border-primary/20"
                           )}>{iv.type}</span>
                        </td>
                        <td className="p-4 text-white/60 truncate max-w-xs">{iv.details}</td>
                        <td className="p-4 text-right text-muted-foreground">[{iv.time}]</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
             <Card className="bg-primary/5 border-primary/30 p-6 flex flex-col justify-center gap-4">
                <div className="flex items-center gap-3 text-primary uppercase font-display font-bold text-sm tracking-widest">
                   <ShieldCheck className="w-5 h-5" /> Immutable Verification
                </div>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  Every intervention is cryptographically signed and hashed into the provenance log, ensuring that the AEGIS system's ethical history cannot be altered or obscured.
                </p>
             </Card>
             <button className="h-full bg-white/5 border border-white/10 rounded-xl p-6 flex items-center justify-between group hover:bg-white/10 transition-all">
                <div className="flex items-center gap-4">
                   <div className="p-3 rounded-full bg-black/40 border border-white/10 group-hover:border-primary/50 transition-colors">
                      <Terminal className="w-6 h-6 text-primary" />
                   </div>
                   <div className="text-left">
                      <div className="text-white font-display font-bold uppercase tracking-tight">Export Audit Report</div>
                      <div className="text-[10px] font-mono text-muted-foreground">Format: PDF-ENCRYPTED-V4</div>
                   </div>
                </div>
                <Zap className="w-5 h-5 text-white/20 group-hover:text-primary transition-colors" />
             </button>
          </div>
        </div>
      </main>
    </div>
  );
}
