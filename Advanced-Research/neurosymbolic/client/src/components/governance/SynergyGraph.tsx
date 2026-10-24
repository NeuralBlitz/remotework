import { motion } from "framer-motion";
import { BrainCircuit } from "lucide-react";

export function SynergyGraph() {
  return (
    <div className="relative w-full h-full min-h-[300px] flex items-center justify-center overflow-hidden rounded-lg bg-black/40 border border-white/10">
      {/* Background Grid */}
      <div className="absolute inset-0 grid-bg opacity-30" />
      
      {/* Center Node */}
      <motion.div 
        className="relative z-10 w-24 h-24 rounded-full bg-black border-2 border-primary flex items-center justify-center shadow-[0_0_30px_rgba(0,255,255,0.3)]"
        animate={{ 
          boxShadow: ["0 0 30px rgba(0,255,255,0.3)", "0 0 60px rgba(0,255,255,0.5)", "0 0 30px rgba(0,255,255,0.3)"]
        }}
        transition={{ duration: 3, repeat: Infinity }}
      >
        <BrainCircuit className="w-10 h-10 text-primary" />
        <div className="absolute inset-0 rounded-full border border-primary/30 animate-ping" />
      </motion.div>

      {/* Orbiting Nodes */}
      {[0, 1, 2, 3, 4].map((i) => (
        <motion.div
          key={i}
          className="absolute w-full h-full"
          animate={{ rotate: 360 }}
          transition={{ duration: 20 + i * 5, repeat: Infinity, ease: "linear" }}
        >
          <div 
            className="absolute top-1/2 left-1/2 w-4 h-4 bg-secondary rounded-full border border-white/50"
            style={{ 
              marginTop: -8,
              marginLeft: -8,
              transform: `translateX(${100 + i * 30}px)` 
            }}
          >
             <div className="absolute inset-0 bg-secondary/50 blur-sm" />
          </div>
        </motion.div>
      ))}
      
       {/* Connecting Lines (Static SVG overlay for effect) */}
       <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-20">
         <circle cx="50%" cy="50%" r="100" stroke="currentColor" className="text-primary" fill="none" strokeDasharray="4 4" />
         <circle cx="50%" cy="50%" r="160" stroke="currentColor" className="text-secondary" fill="none" strokeWidth="0.5" />
       </svg>

       <div className="absolute bottom-4 left-4 text-xs font-mono text-primary/80">
         SYNERGY ENGINE: FUSION LEVEL 98.4%
       </div>
    </div>
  );
}
