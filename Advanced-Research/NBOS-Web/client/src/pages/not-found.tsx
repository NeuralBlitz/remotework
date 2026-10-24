import { Link } from "wouter";
import { CyberButton } from "@/components/CyberButton";
import { AlertTriangle } from "lucide-react";

export default function NotFound() {
  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-background p-4 relative overflow-hidden">
      {/* Background glitch effect */}
      <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20" />
      
      <div className="relative z-10 text-center space-y-8 max-w-md w-full p-8 border border-destructive/30 bg-black/80 backdrop-blur-md">
        <div className="flex justify-center">
          <AlertTriangle className="w-24 h-24 text-destructive animate-pulse" />
        </div>
        
        <div className="space-y-2">
          <h1 className="text-6xl font-display font-black text-white tracking-tighter">
            4<span className="text-destructive animate-pulse">0</span>4
          </h1>
          <p className="text-xl font-mono text-destructive uppercase tracking-widest">
            SECTOR NOT FOUND
          </p>
        </div>

        <p className="text-muted-foreground font-mono text-sm leading-relaxed">
          The coordinates you entered correspond to a null-void region. 
          Reality has not yet propagated to this sector.
        </p>

        <div className="pt-4">
          <Link href="/">
            <CyberButton variant="danger" className="w-full">
              INITIATE EMERGENCY JUMP
            </CyberButton>
          </Link>
        </div>
      </div>
    </div>
  );
}
