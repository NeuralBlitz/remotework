import { Navigation } from "@/components/layout/Navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Database, Search, ShieldCheck, History } from "lucide-react";
import { motion } from "framer-motion";
import { useState } from "react";
import { useSimulator, type LogEntry } from "@/lib/store";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";

export default function DataProvenance() {
  const { logs } = useSimulator();
  const [search, setSearch] = useState("");
  const [selectedLog, setSelectedLog] = useState<LogEntry | null>(null);

  const dataLogs = logs.filter(l => l.category === 'data' || l.category === 'neural');
  const filtered = dataLogs.filter(l => 
    l.msg.toLowerCase().includes(search.toLowerCase()) ||
    l.details?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30">
      <Navigation />
      <main className="md:pl-64 pt-16 md:pt-0 pb-24 md:pb-0 min-h-screen relative">
        <div className="relative z-10 p-4 md:p-8 space-y-6">
          <header className="border-b border-white/10 pb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl font-display font-bold text-white tracking-tight flex items-center gap-3">
                <Database className="text-primary" /> Data Provenance
              </h1>
              <p className="text-muted-foreground mt-2 max-w-2xl font-display text-sm">
                Real-time traceability for all NeuralBlitz artifacts.
              </p>
            </div>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input 
                type="text" 
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search hashes & sources..." 
                className="bg-white/5 border border-white/10 rounded-full py-2 pl-10 pr-4 text-xs font-mono focus:outline-none focus:border-primary/50 transition-all w-full md:w-64"
              />
            </div>
          </header>

          <Card className="bg-black/40 border-primary/20 backdrop-blur-md">
            <CardHeader className="border-b border-white/10">
              <CardTitle className="text-sm font-mono text-primary flex items-center gap-2">
                <History className="w-4 h-4" /> TRACEABILITY STREAM
              </CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <div className="overflow-x-auto">
                <table className="w-full text-left font-mono text-xs">
                  <thead>
                    <tr className="border-b border-white/5 text-muted-foreground uppercase tracking-widest bg-white/2">
                      <th className="p-4 font-medium">Timestamp</th>
                      <th className="p-4 font-medium">Artifact ID</th>
                      <th className="p-4 font-medium">Event</th>
                      <th className="p-4 font-medium text-right">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    {filtered.reverse().map((log) => (
                      <motion.tr 
                        key={log.id}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        onClick={() => setSelectedLog(log as LogEntry)}
                        className="hover:bg-white/5 transition-colors group cursor-pointer"
                      >
                        <td className="p-4 text-muted-foreground whitespace-nowrap">[{log.time}]</td>
                        <td className="p-4 text-primary font-bold">0x{log.id.slice(2, 10)}...</td>
                        <td className="p-4 text-white opacity-80">{log.msg}</td>
                        <td className="p-4 text-right">
                           <ShieldCheck className="w-4 h-4 text-green-400 inline" />
                        </td>
                      </motion.tr>
                    ))}
                    {filtered.length === 0 && (
                      <tr>
                        <td colSpan={4} className="p-8 text-center text-muted-foreground italic">No matching provenance records found.</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>

      <Dialog open={!!selectedLog} onOpenChange={() => setSelectedLog(null)}>
        <DialogContent className="bg-black border-primary/30 text-white">
          <DialogHeader>
            <DialogTitle className="text-primary font-mono uppercase">Artifact Provenance Details</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
             <div className="p-3 bg-white/5 rounded border border-white/10">
                <div className="text-[10px] text-muted-foreground uppercase mb-1">Source Artifact</div>
                <div className="text-sm font-mono">{selectedLog?.msg}</div>
             </div>
             <div className="p-3 bg-white/5 rounded border border-white/10">
                <div className="text-[10px] text-muted-foreground uppercase mb-1">Integrity Details</div>
                <div className="text-xs font-mono text-white/70">{selectedLog?.details || "Standard integrity check passed."}</div>
             </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
