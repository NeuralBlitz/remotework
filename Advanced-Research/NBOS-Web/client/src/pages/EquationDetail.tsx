import { useEquation } from "@/hooks/use-equations";
import { CyberCard } from "@/components/CyberCard";
import { CyberButton } from "@/components/CyberButton";
import { LatexDisplay } from "@/components/LatexDisplay";
import { useRoute, Link } from "wouter";
import { ArrowLeft, Share2, Printer, Loader2, AlertTriangle } from "lucide-react";
import { motion } from "framer-motion";

export default function EquationDetail() {
  const [match, params] = useRoute("/equations/:id");
  const id = params ? parseInt(params.id) : 0;
  const { data: equation, isLoading, error } = useEquation(id);

  if (isLoading) {
    return (
      <div className="h-screen flex items-center justify-center flex-col gap-4">
        <Loader2 className="w-16 h-16 text-primary animate-spin" />
        <p className="font-mono text-primary/60 animate-pulse">DECRYPTING...</p>
      </div>
    );
  }

  if (error || !equation) {
    return (
      <div className="h-[60vh] flex flex-col items-center justify-center text-center gap-6">
        <AlertTriangle className="w-20 h-20 text-destructive/80" />
        <div>
          <h2 className="text-3xl font-display font-bold text-white mb-2">DATA CORRUPTION</h2>
          <p className="text-destructive font-mono">UNABLE TO RETRIEVE RECORD ID: {id}</p>
        </div>
        <Link href="/equations">
          <CyberButton variant="ghost">RETURN TO INDEX</CyberButton>
        </Link>
      </div>
    );
  }

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-8"
    >
      {/* Navigation & Actions */}
      <div className="flex justify-between items-center">
        <Link href="/equations">
          <button className="flex items-center gap-2 text-primary hover:text-white transition-colors font-mono text-sm uppercase tracking-wider group">
            <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
            Back to Index
          </button>
        </Link>
        <div className="flex gap-3">
          <button className="p-2 border border-primary/30 hover:bg-primary/20 text-primary transition-colors">
            <Share2 className="w-5 h-5" />
          </button>
          <button className="p-2 border border-primary/30 hover:bg-primary/20 text-primary transition-colors">
            <Printer className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Main Content Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Equation Visual */}
        <div className="lg:col-span-2 space-y-8">
          <CyberCard className="min-h-[300px] flex items-center justify-center relative overflow-hidden bg-black/60 border-primary/40 shadow-[0_0_50px_rgba(0,240,255,0.1)]">
            {/* Background Grid */}
            <div className="absolute inset-0 opacity-10" 
              style={{ 
                backgroundImage: 'linear-gradient(rgba(0, 240, 255, 0.3) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 240, 255, 0.3) 1px, transparent 1px)',
                backgroundSize: '40px 40px'
              }}
            />
            
            <div className="relative z-10 p-8 text-center">
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.5 }}
                className="text-2xl md:text-4xl text-white drop-shadow-[0_0_10px_rgba(0,240,255,0.8)]"
              >
                <LatexDisplay expression={equation.latex} block glow />
              </motion.div>
            </div>

            <div className="absolute top-4 left-4 font-mono text-xs text-primary/40">
              RENDER_MODE: HIGH_PRECISION
            </div>
          </CyberCard>

          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-display text-white mb-4 border-l-4 border-secondary pl-4">
                CONCEPTUAL <span className="text-secondary">FRAMEWORK</span>
              </h2>
              <div className="p-6 bg-white/5 border border-white/10 rounded-lg text-gray-300 leading-relaxed font-light text-lg">
                {equation.concept}
              </div>
            </div>

            <div>
              <h2 className="text-2xl font-display text-white mb-4 border-l-4 border-accent pl-4">
                DECONSTRUCTION
              </h2>
              <div className="p-6 bg-white/5 border border-white/10 rounded-lg text-gray-400 font-mono text-sm leading-loose">
                {equation.deconstruction.split('\n').map((line, i) => (
                  <p key={i} className="mb-2">
                    <span className="text-accent/60 mr-2">{`[${(i + 1).toString().padStart(2, '0')}]`}</span>
                    {line}
                  </p>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Metadata */}
        <div className="space-y-6">
          <CyberCard title="Metadata" className="border-l-4 border-l-primary">
            <div className="space-y-4">
              <MetaRow label="Designation Code" value={equation.code} />
              <MetaRow label="Category" value={equation.category} />
              <MetaRow label="Complexity Class" value="Type IV" />
              <MetaRow label="Discovery Date" value="2142.08.15" />
              <MetaRow label="Status" value="VERIFIED" highlight />
            </div>
          </CyberCard>

          <CyberCard title="Usage Metrics">
            <div className="h-40 flex items-end gap-2 px-2 pb-2">
              {[40, 70, 45, 90, 60, 80, 50, 75, 60, 95].map((h, i) => (
                <motion.div 
                  key={i}
                  className="flex-1 bg-secondary/40 hover:bg-secondary/80 transition-colors cursor-crosshair relative group"
                  initial={{ height: 0 }}
                  animate={{ height: `${h}%` }}
                  transition={{ delay: i * 0.05 + 0.5, duration: 1 }}
                >
                   <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 text-[10px] text-white opacity-0 group-hover:opacity-100 font-mono">
                     {h}%
                   </div>
                </motion.div>
              ))}
            </div>
            <p className="text-xs text-center font-mono text-muted-foreground mt-4">
              GLOBAL COMPUTATIONAL LOAD (24H)
            </p>
          </CyberCard>
        </div>

      </div>
    </motion.div>
  );
}

function MetaRow({ label, value, highlight = false }: { label: string, value: string, highlight?: boolean }) {
  return (
    <div className="flex justify-between items-center py-2 border-b border-white/5 last:border-0">
      <span className="text-xs font-mono text-muted-foreground uppercase">{label}</span>
      <span className={`font-medium ${highlight ? 'text-primary text-glow font-bold' : 'text-white'}`}>
        {value}
      </span>
    </div>
  );
}
