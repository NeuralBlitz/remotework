import { Navigation } from "@/components/layout/Navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { GitBranch, Folder, FileCode, Search, ShieldCheck } from "lucide-react";
import { motion } from "framer-motion";
import { useState } from "react";

const structure = [
  { name: "src/engine", type: "dir", desc: "Core Synergy Engine modules" },
  { name: "src/governance", type: "dir", desc: "CharterLayer and Axiomatic Gates" },
  { name: "src/epistemic", type: "dir", desc: "Active Epistemic Inquiry tools" },
  { name: "src/probes", type: "dir", desc: "Bias detection and mitigation probes" },
  { name: "charter.json", type: "file", desc: "Hard-coded ethical constraints" },
  { name: "synergy.config.ts", type: "file", desc: "Systemic Fusion parameters" },
  { name: "provenance.log", type: "file", desc: "End-to-end data history" },
];

export default function RepoStructure() {
  const [search, setSearch] = useState("");

  const filtered = structure.filter(s => 
    s.name.toLowerCase().includes(search.toLowerCase()) || 
    s.desc.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30">
      <Navigation />
      <main className="md:pl-64 pt-16 md:pt-0 pb-24 md:pb-0 min-h-screen relative">
        <div className="relative z-10 p-4 md:p-8 space-y-6">
          <header className="border-b border-white/10 pb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl font-display font-bold text-white tracking-tight flex items-center gap-3">
                <GitBranch className="text-primary" /> Repository Structure
              </h1>
              <p className="text-muted-foreground mt-2 max-w-2xl font-display text-sm">
                The technical blueprint of the AEGIS.AI governance fabric.
              </p>
            </div>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input 
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search file structure..." 
                className="bg-white/5 border border-white/10 rounded-full py-2 pl-10 pr-4 text-xs font-mono focus:outline-none focus:border-primary/50 transition-all w-full md:w-64"
              />
            </div>
          </header>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <Card className="bg-black/40 border-primary/20 backdrop-blur-md lg:col-span-2">
              <CardHeader className="border-b border-white/10">
                <CardTitle className="text-xs font-mono text-primary flex items-center gap-2">
                  <Search className="w-4 h-4" /> BROWSE SOURCE TREE
                </CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                <div className="divide-y divide-white/5 font-mono text-sm">
                  {filtered.map((item, i) => (
                    <motion.div 
                      key={item.name}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.05 }}
                      className="p-4 flex items-center justify-between hover:bg-white/5 transition-colors group cursor-pointer"
                    >
                      <div className="flex items-center gap-3">
                        {item.type === "dir" ? (
                          <Folder className="w-4 h-4 text-primary opacity-70" />
                        ) : (
                          <FileCode className="w-4 h-4 text-secondary opacity-70" />
                        )}
                        <span className="text-white group-hover:text-primary transition-colors">{item.name}</span>
                      </div>
                      <span className="text-[10px] text-muted-foreground uppercase tracking-widest bg-white/5 px-2 py-0.5 rounded">{item.desc}</span>
                    </motion.div>
                  ))}
                  {filtered.length === 0 && (
                    <div className="p-8 text-center text-muted-foreground italic">No modules match your search query.</div>
                  )}
                </div>
              </CardContent>
            </Card>

            <div className="space-y-6">
              <Card className="bg-primary/5 border-primary/30 backdrop-blur-md h-full">
                <CardHeader>
                  <CardTitle className="text-sm font-mono text-primary flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4" /> REPOSITORY MANIFEST
                  </CardTitle>
                </CardHeader>
                <CardContent className="text-xs text-muted-foreground space-y-6">
                  <div className="p-4 bg-black/40 rounded border border-white/10 font-mono space-y-4">
                    <div>
                      <div className="text-white mb-1 uppercase tracking-widest text-[10px]">Architecture Type</div>
                      <div className="text-primary font-bold">Holistic Neural Mesh</div>
                    </div>
                    <div>
                      <div className="text-white mb-1 uppercase tracking-widest text-[10px]">Governance Style</div>
                      <div className="text-secondary font-bold">Axiomatic-as-Code</div>
                    </div>
                  </div>
                  <p className="leading-relaxed">
                    This structure is designed to enforce systemic fusion across the entire lifecycle, ensuring that ethical constraints are not external documents but active components of the neural fabric.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
