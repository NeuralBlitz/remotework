import { useState, useRef, useEffect } from "react";
import { useSimulateGenesis } from "@/hooks/use-equations";
import { CyberButton } from "@/components/CyberButton";
import { CyberCard } from "@/components/CyberCard";
import { motion, AnimatePresence } from "framer-motion";
import { Terminal, Play, RefreshCw, AlertCircle } from "lucide-react";

export default function Simulation() {
  const { mutate: runSimulation, isPending, data } = useSimulateGenesis();
  const [logs, setLogs] = useState<string[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Mock logging effect for visuals
  useEffect(() => {
    if (data?.logs) {
      let i = 0;
      const interval = setInterval(() => {
        if (i < data.logs.length) {
          setLogs(prev => [...prev, data.logs[i]]);
          i++;
        } else {
          clearInterval(interval);
        }
      }, 500); // Slow type effect
      return () => clearInterval(interval);
    }
  }, [data]);

  // Auto scroll logs
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  const handleStart = () => {
    setLogs([]);
    runSimulation();
  };

  return (
    <div className="h-[calc(100vh-140px)] flex flex-col gap-6">
      <div className="flex justify-between items-center border-b border-primary/20 pb-6">
        <div>
          <h1 className="text-4xl font-display font-bold text-white mb-2">
            COSMIC <span className="text-accent">GENESIS</span> PROTOCOL
          </h1>
          <p className="font-mono text-primary/60">
            // VISUALIZER V1.0 // CAUTION: REALITY DISTORTION POSSIBLE
          </p>
        </div>
        <div className="flex gap-4">
          <CyberButton 
            variant="primary" 
            onClick={handleStart} 
            disabled={isPending}
            className="w-48"
          >
            {isPending ? (
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <Play className="w-4 h-4 mr-2" />
            )}
            {isPending ? "COMPUTING..." : "INITIATE"}
          </CyberButton>
        </div>
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-8 min-h-0">
        {/* Visualizer Area */}
        <div className="lg:col-span-2 relative bg-black border border-primary/30 overflow-hidden">
          <div className="absolute inset-0 grid-bg opacity-20 pointer-events-none" />
          
          <div className="absolute inset-0 flex items-center justify-center">
            {isPending || (data && logs.length < (data?.logs?.length || 0)) ? (
              <SimulationVisualizer active={true} />
            ) : logs.length > 0 ? (
               <div className="text-center">
                 <motion.div 
                   initial={{ scale: 0 }}
                   animate={{ scale: 1 }}
                   className="w-32 h-32 rounded-full border-4 border-primary shadow-[0_0_50px_var(--primary)] mx-auto mb-4 bg-white"
                 />
                 <h3 className="text-2xl font-display text-white">SIMULATION COMPLETE</h3>
               </div>
            ) : (
              <div className="text-center text-muted-foreground/50">
                <div className="w-24 h-24 border border-dashed border-current rounded-full mx-auto mb-4 animate-spin-slow" />
                <p className="font-mono tracking-widest">AWAITING INPUT</p>
              </div>
            )}
          </div>
          
          {/* Overlay Stats */}
          <div className="absolute top-4 right-4 text-right font-mono text-xs text-primary/80">
            <div>FRAME_TIME: 16.6ms</div>
            <div>NODES: {isPending ? "CALCULATING..." : "IDLE"}</div>
          </div>
        </div>

        {/* Terminal Output */}
        <div className="flex flex-col h-full min-h-0">
          <CyberCard title="System Logs" className="flex-1 flex flex-col min-h-0 bg-black/80">
            <div 
              ref={scrollRef}
              className="flex-1 overflow-y-auto font-mono text-xs space-y-2 pr-2 scrollbar-thin scrollbar-thumb-primary/20 scrollbar-track-transparent"
            >
              <div className="text-muted-foreground italic mb-4">
                // Console ready...
              </div>
              
              <AnimatePresence>
                {logs.map((log, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="flex gap-2"
                  >
                    <span className="text-primary/50">[{new Date().toLocaleTimeString()}]</span>
                    <span className={log.includes("ERROR") ? "text-destructive" : "text-white/80"}>
                      {log.startsWith(">") ? <span className="text-accent mr-2">➜</span> : null}
                      {log.replace(">", "")}
                    </span>
                  </motion.div>
                ))}
              </AnimatePresence>
              
              {isPending && (
                <div className="animate-pulse text-primary">_</div>
              )}
            </div>
            
            <div className="mt-4 pt-4 border-t border-white/10 flex gap-2">
              <Terminal className="w-4 h-4 text-primary" />
              <input 
                type="text" 
                disabled
                placeholder="Terminal access restricted..." 
                className="bg-transparent border-none outline-none text-xs font-mono text-muted-foreground w-full"
              />
            </div>
          </CyberCard>
        </div>
      </div>
    </div>
  );
}

function SimulationVisualizer({ active }: { active: boolean }) {
  // Simple purely CSS/framer visualizer for effect
  return (
    <div className="relative w-64 h-64">
      {/* Central Core */}
      <motion.div 
        animate={{ 
          rotate: 360,
          scale: [1, 1.1, 1]
        }}
        transition={{ 
          rotate: { duration: 10, repeat: Infinity, ease: "linear" },
          scale: { duration: 2, repeat: Infinity }
        }}
        className="absolute inset-0 border-2 border-primary rounded-full opacity-50"
      />
      
      {/* Orbital Rings */}
      {[1, 2, 3].map((i) => (
        <motion.div
          key={i}
          animate={{ rotate: -360 }}
          transition={{ duration: 15 / i, repeat: Infinity, ease: "linear" }}
          className="absolute inset-0 border border-secondary/30 rounded-full"
          style={{ margin: `${i * 20}px` }}
        >
          <div className="w-2 h-2 bg-secondary rounded-full absolute -top-1 left-1/2 shadow-[0_0_10px_var(--secondary)]" />
        </motion.div>
      ))}

      {/* Particle Field */}
      <div className="absolute inset-0 flex items-center justify-center">
        <motion.div 
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 0.5, repeat: Infinity }}
          className="w-4 h-4 bg-white rounded-full blur-sm"
        />
      </div>
    </div>
  );
}
