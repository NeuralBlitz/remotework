import { Navigation } from "@/components/layout/Navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Share2, ArrowRight, Database, Box, Info, GitMerge, Shield } from "lucide-react";
import { motion } from "framer-motion";
import { useState } from "react";
import { cn } from "@/lib/utils";

const lineageNodes = [
  { id: "L-1", label: "Training Corpus A", type: "DATA", status: "VERIFIED" },
  { id: "L-2", label: "Weight Optimizer v4", type: "PROCESS", status: "ACTIVE" },
  { id: "L-3", label: "CharterLayer Probe", type: "GOVERNANCE", status: "SECURE" },
  { id: "L-4", label: "Inference Artifact 921", type: "OUTPUT", status: "AUDITED" },
];

export default function LineageVisualizer() {
  const [selected, setSelected] = useState(lineageNodes[0]);

  return (
    <div className="min-h-screen bg-background text-foreground font-sans">
      <Navigation />
      <main className="md:pl-64 pt-16 md:pt-0 pb-24 md:pb-0 min-h-screen relative">
        <div className="p-4 md:p-8 space-y-8">
          <header className="border-b border-white/10 pb-6">
            <h1 className="text-3xl font-display font-bold text-white tracking-tight flex items-center gap-3">
              <Share2 className="text-primary" /> Lineage Visualizer
            </h1>
            <p className="text-muted-foreground mt-2 max-w-2xl text-sm">
              End-to-end provenance mapping for every neural artifact and governance intervention.
            </p>
          </header>

          <div className="grid grid-cols-12 gap-6">
            <Card className="col-span-12 lg:col-span-8 bg-black/40 border-white/10 h-[500px] relative overflow-hidden flex items-center justify-center p-12">
              <div className="absolute inset-0 bg-grid-white/[0.01] pointer-events-none" />
              <div className="flex items-center gap-8 relative z-10 w-full justify-between">
                {lineageNodes.map((node, i) => (
                  <div key={node.id} className="flex items-center gap-8">
                    <motion.button
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: i * 0.1 }}
                      onClick={() => setSelected(node)}
                      className={cn(
                        "w-36 h-36 rounded-xl border-2 p-4 flex flex-col items-center justify-center text-center gap-3 transition-all",
                        selected.id === node.id ? "bg-primary/10 border-primary shadow-[0_0_30px_rgba(0,255,255,0.15)] scale-110" : "bg-white/5 border-white/10 hover:border-white/30"
                      )}
                    >
                      {node.type === "DATA" && <Database className="w-6 h-6 text-primary" />}
                      {node.type === "PROCESS" && <GitMerge className="w-6 h-6 text-secondary" />}
                      {node.type === "GOVERNANCE" && <Shield className="w-6 h-6 text-amber-400" />}
                      {node.type === "OUTPUT" && <Box className="w-6 h-6 text-green-400" />}
                      <span className="text-[10px] font-mono text-white/80 uppercase tracking-tight leading-tight">{node.label}</span>
                    </motion.button>
                    {i < lineageNodes.length - 1 && (
                      <ArrowRight className="w-6 h-6 text-white/10 shrink-0" />
                    )}
                  </div>
                ))}
              </div>
            </Card>

            <div className="col-span-12 lg:col-span-4 space-y-6">
              <Card className="bg-black/40 border-primary/20 h-full">
                <CardHeader className="border-b border-white/10">
                  <CardTitle className="text-xs font-mono text-primary uppercase">Artifact Metadata</CardTitle>
                </CardHeader>
                <CardContent className="p-6 space-y-6">
                  <div className="space-y-4">
                    <div className="p-4 bg-white/5 rounded border border-white/5">
                      <div className="text-[9px] font-mono text-muted-foreground uppercase mb-1">Entity ID</div>
                      <div className="text-sm font-mono text-white">{selected.id}</div>
                    </div>
                    <div className="p-4 bg-white/5 rounded border border-white/5">
                      <div className="text-[9px] font-mono text-muted-foreground uppercase mb-1">Verification Status</div>
                      <div className="text-sm font-mono text-green-400 font-bold">{selected.status}</div>
                    </div>
                  </div>
                  <div className="p-4 bg-primary/5 border border-primary/20 rounded-lg">
                    <div className="flex items-center gap-2 mb-2 text-primary font-mono text-[10px] uppercase">
                      <Info className="w-3 h-3" /> Integrity Hash
                    </div>
                    <div className="text-[10px] font-mono text-white/60 break-all">
                      SHA256: 0x9a2f...11b0e7c3...4f2d
                    </div>
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
