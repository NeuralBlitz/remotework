import { Link, useLocation } from "wouter";
import { Shield, GitBranch, Activity, Database, Settings, BrainCircuit, Eye } from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
  { icon: Shield, label: "Charter Monitor", href: "/" },
  { icon: GitBranch, label: "Repo Structure", href: "/repo" },
  { icon: BrainCircuit, label: "Synergy Engine", href: "/synergy" },
  { icon: Eye, label: "Epistemic Log", href: "/epistemic" },
  { icon: Database, label: "Data Provenance", href: "/data" },
  { icon: Settings, label: "Governance Config", href: "/settings" },
];

export function AppSidebar() {
  const [location] = useLocation();

  return (
    <div className="w-64 border-r border-white/10 bg-card/80 backdrop-blur-xl h-screen flex flex-col fixed left-0 top-0 z-50">
      <div className="p-6 border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-primary/20 border border-primary flex items-center justify-center">
            <BrainCircuit className="w-5 h-5 text-primary" />
          </div>
          <h1 className="font-display font-bold text-lg tracking-wider text-white">
            AEGIS<span className="text-primary">.AI</span>
          </h1>
        </div>
        <p className="text-xs text-muted-foreground mt-2 font-mono">
          System Status: <span className="text-green-400">NOMINAL</span>
        </p>
      </div>

      <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
        {navItems.map((item) => {
          const isActive = location === item.href;
          return (
            <Link key={item.href} href={item.href}>
              <a
                className={cn(
                  "flex items-center gap-3 px-4 py-3 rounded-md transition-all duration-200 group border border-transparent",
                  isActive
                    ? "bg-primary/10 text-primary border-primary/30 shadow-[0_0_10px_rgba(0,255,255,0.1)]"
                    : "text-muted-foreground hover:text-white hover:bg-white/5"
                )}
              >
                <item.icon
                  className={cn(
                    "w-5 h-5 transition-colors",
                    isActive ? "text-primary" : "text-muted-foreground group-hover:text-white"
                  )}
                />
                <span className="font-medium font-display tracking-wide text-sm">
                  {item.label}
                </span>
              </a>
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-white/10">
        <div className="p-3 rounded bg-black/40 border border-white/5 font-mono text-xs text-muted-foreground">
          <div className="flex justify-between mb-1">
            <span>CPU</span>
            <span className="text-primary">42%</span>
          </div>
          <div className="w-full bg-white/10 h-1 rounded overflow-hidden">
            <div className="bg-primary h-full w-[42%]" />
          </div>
          <div className="flex justify-between mt-2 mb-1">
            <span>MEM</span>
            <span className="text-secondary">68%</span>
          </div>
          <div className="w-full bg-white/10 h-1 rounded overflow-hidden">
            <div className="bg-secondary h-full w-[68%]" />
          </div>
        </div>
      </div>
    </div>
  );
}
