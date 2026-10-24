import { Link, useLocation } from "wouter";
import { LayoutDashboard, Variable, Network, Activity } from "lucide-react";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/equations", label: "Equations", icon: Variable },
  { href: "/simulation", label: "Simulation", icon: Network },
];

export function Navigation() {
  const [location] = useLocation();

  return (
    <nav className="fixed left-0 top-0 bottom-0 w-20 md:w-64 bg-black/80 backdrop-blur-xl border-r border-primary/20 z-50 flex flex-col">
      <div className="p-6 border-b border-primary/20">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-primary rounded-none shadow-[0_0_15px_var(--primary)] animate-pulse" />
          <h1 className="hidden md:block font-display font-bold text-xl tracking-tighter text-white">
            OMEGA<span className="text-primary">PRIME</span>
          </h1>
        </div>
      </div>

      <div className="flex-1 py-8 flex flex-col gap-2 px-3">
        {NAV_ITEMS.map((item) => {
          const isActive = location === item.href;
          const Icon = item.icon;
          
          return (
            <Link 
              key={item.href} 
              href={item.href}
              className={cn(
                "flex items-center gap-4 px-4 py-3 transition-all duration-300 group relative overflow-hidden",
                isActive 
                  ? "text-primary bg-primary/10 border-r-2 border-primary" 
                  : "text-muted-foreground hover:text-white hover:bg-white/5"
              )}
            >
              <Icon className={cn("w-5 h-5", isActive && "drop-shadow-[0_0_8px_rgba(0,240,255,0.8)]")} />
              <span className="hidden md:block font-mono text-sm tracking-wider uppercase">
                {item.label}
              </span>
              
              {isActive && (
                <div className="absolute inset-0 bg-gradient-to-r from-primary/0 via-primary/5 to-primary/0 animate-scan-slow pointer-events-none" />
              )}
            </Link>
          );
        })}
      </div>

      <div className="p-4 border-t border-primary/20">
        <div className="flex items-center gap-3 text-xs font-mono text-muted-foreground">
          <Activity className="w-4 h-4 text-green-500 animate-pulse" />
          <span className="hidden md:inline">SYSTEM ONLINE</span>
        </div>
        <div className="mt-2 text-[10px] text-primary/40 hidden md:block font-mono">
          V.9.0.4.2 :: GENESIS
        </div>
      </div>
    </nav>
  );
}
