import { ReactNode } from "react";
import { cn } from "@/lib/utils";

interface CyberCardProps {
  children: ReactNode;
  className?: string;
  title?: string;
  code?: string;
  active?: boolean;
}

export function CyberCard({ children, className, title, code, active = false }: CyberCardProps) {
  return (
    <div className={cn(
      "cyber-card p-6 flex flex-col h-full",
      active && "border-primary shadow-[0_0_20px_rgba(0,240,255,0.2)]",
      className
    )}>
      {(title || code) && (
        <div className="flex justify-between items-start mb-4 border-b border-primary/20 pb-2">
          {title && (
            <h3 className={cn("text-lg font-bold text-primary truncate", active && "text-glow")}>
              {title}
            </h3>
          )}
          {code && (
            <span className="font-mono text-xs text-secondary bg-secondary/10 px-2 py-1 border border-secondary/30">
              {code}
            </span>
          )}
        </div>
      )}
      <div className="relative z-10 flex-grow">
        {children}
      </div>
      
      {/* Decorative corner accents */}
      <div className="absolute top-0 right-0 p-1">
        <div className="w-2 h-2 bg-primary/30" />
      </div>
      <div className="absolute bottom-0 left-0 p-1">
        <div className="w-2 h-2 bg-primary/30" />
      </div>
    </div>
  );
}
