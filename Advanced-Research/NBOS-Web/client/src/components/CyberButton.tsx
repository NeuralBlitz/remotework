import { ButtonHTMLAttributes, forwardRef } from "react";
import { cn } from "@/lib/utils";

interface CyberButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger" | "ghost";
  size?: "sm" | "md" | "lg";
  glitch?: boolean;
}

export const CyberButton = forwardRef<HTMLButtonElement, CyberButtonProps>(
  ({ className, variant = "primary", size = "md", glitch = false, children, ...props }, ref) => {
    
    const variants = {
      primary: "bg-primary/10 border-primary text-primary hover:bg-primary hover:text-black hover:shadow-[0_0_20px_rgba(0,240,255,0.6)]",
      secondary: "bg-secondary/10 border-secondary text-secondary hover:bg-secondary hover:text-white hover:shadow-[0_0_20px_rgba(188,19,254,0.6)]",
      danger: "bg-destructive/10 border-destructive text-destructive hover:bg-destructive hover:text-white hover:shadow-[0_0_20px_rgba(255,0,0,0.6)]",
      ghost: "border-transparent text-primary/60 hover:text-primary hover:bg-primary/5",
    };

    const sizes = {
      sm: "h-8 px-4 text-xs",
      md: "h-12 px-6 text-sm",
      lg: "h-14 px-8 text-base tracking-widest",
    };

    return (
      <button
        ref={ref}
        className={cn(
          "relative border overflow-hidden transition-all duration-200 uppercase font-mono font-bold tracking-wider clip-path-slant group",
          variants[variant],
          sizes[size],
          className
        )}
        {...props}
      >
        <span className="relative z-10 flex items-center gap-2 justify-center">
          {children}
        </span>
        
        {/* Hover scanline effect */}
        <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-[-100%] transition-transform duration-500 ease-in-out z-0" />
        
        {/* Glitch decoration lines */}
        {glitch && (
          <>
            <div className="absolute top-0 left-[-100%] w-full h-[2px] bg-white opacity-50 group-hover:animate-scan-fast" />
            <div className="absolute bottom-0 right-[-100%] w-full h-[2px] bg-white opacity-50 group-hover:animate-scan-fast-reverse" />
          </>
        )}
      </button>
    );
  }
);

CyberButton.displayName = "CyberButton";
