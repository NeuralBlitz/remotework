import { Link, useLocation } from "wouter";
import { Shield, GitBranch, Activity, Database, Settings, BrainCircuit, Eye, Menu, X, PlaySquare, Network, LayoutDashboard, Sliders, AlertTriangle, Compass, Share2, Lock } from "lucide-react";
import { cn } from "@/lib/utils";
import { useState } from "react";

const navItems = [
  { icon: LayoutDashboard, label: "Control Center", href: "/" },
  { icon: Compass, label: "Discovery Engine", href: "/discovery" },
  { icon: AlertTriangle, label: "Risk Heatmap", href: "/heatmap" },
  { icon: PlaySquare, label: "Model Playground", href: "/playground" },
  { icon: Sliders, label: "Policy Simulator", href: "/simulator" },
  { icon: Network, label: "Causal Logic", href: "/causal" },
  { icon: Share2, label: "Lineage Visualizer", href: "/lineage" },
  { icon: Lock, label: "Audit Vault", href: "/audit" },
  { icon: Shield, label: "Ethical Charter", href: "/charter" },
  { icon: GitBranch, label: "Repo Structure", href: "/repo" },
  { icon: BrainCircuit, label: "Synergy Engine", href: "/synergy" },
  { icon: Eye, label: "Epistemic Log", href: "/epistemic" },
  { icon: Database, label: "Data Provenance", href: "/data" },
  { icon: Settings, label: "Governance Config", href: "/settings" },
];

export function Navigation() {
  const [location] = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <>
      {/* Desktop Sidebar */}
      <div className="hidden md:flex w-64 border-r border-white/10 bg-card/80 backdrop-blur-xl h-screen flex-col fixed left-0 top-0 z-40">
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

        <nav className="flex-1 p-3 space-y-1 overflow-y-auto scrollbar-hide">
          {navItems.map((item) => {
            const isActive = location === item.href;
            return (
              <Link key={item.href} href={item.href}>
                <a
                  className={cn(
                    "flex items-center gap-3 px-3 py-2 rounded-md transition-all duration-200 group border border-transparent",
                    isActive
                      ? "bg-primary/10 text-primary border-primary/30"
                      : "text-muted-foreground hover:text-white hover:bg-white/5"
                  )}
                >
                  <item.icon
                    className={cn(
                      "w-4 h-4 transition-colors",
                      isActive ? "text-primary" : "text-muted-foreground group-hover:text-white"
                    )}
                  />
                  <span className="font-medium font-display tracking-wide text-[10px] uppercase italic">
                    {item.label}
                  </span>
                </a>
              </Link>
            );
          })}
        </nav>

        <div className="p-4 border-t border-white/10">
          <div className="p-3 rounded bg-black/40 border border-white/5 font-mono text-[10px] text-muted-foreground">
            <div className="flex justify-between mb-1">
              <span>SYNC</span>
              <span className="text-primary">99.9%</span>
            </div>
            <div className="w-full bg-white/10 h-1 rounded overflow-hidden">
              <div className="bg-primary h-full w-[99%]" />
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Header */}
      <div className="md:hidden fixed top-0 left-0 right-0 z-40 bg-card/80 backdrop-blur-xl border-b border-white/10">
        <div className="flex items-center justify-between p-4">
          <div className="flex items-center gap-2">
            <BrainCircuit className="w-5 h-5 text-primary" />
            <h1 className="font-display font-bold text-sm tracking-wider text-white uppercase">AEGIS.AI</h1>
          </div>
          <button onClick={() => setMobileMenuOpen(!mobileMenuOpen)} className="p-2">
            {mobileMenuOpen ? <X className="w-5 h-5 text-primary" /> : <Menu className="w-5 h-5 text-white" />}
          </button>
        </div>
        {mobileMenuOpen && (
          <nav className="border-t border-white/10 bg-black/95 max-h-[80vh] overflow-y-auto p-4 space-y-2">
            {navItems.map((item) => (
              <Link key={item.href} href={item.href}>
                <a onClick={() => setMobileMenuOpen(false)} className={cn("flex items-center gap-3 p-3 rounded", location === item.href ? "bg-primary/10 text-primary" : "text-muted-foreground")}>
                  <item.icon className="w-4 h-4" />
                  <span className="text-sm font-display uppercase italic">{item.label}</span>
                </a>
              </Link>
            ))}
          </nav>
        )}
      </div>
    </>
  );
}
