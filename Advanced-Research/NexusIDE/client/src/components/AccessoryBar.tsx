import { FC } from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

interface AccessoryBarProps {
  onInsert: (text: string) => void;
  className?: string;
}

const symbols = ["{", "}", "(", ")", "[", "]", ";", "<", ">", "/", "=", "\"", "'", ":"];

const AccessoryBar: FC<AccessoryBarProps> = ({ onInsert, className }) => {
  return (
    <div className={cn(
      "flex items-center space-x-1 overflow-x-auto p-2 bg-neutral-900 border-t border-neutral-800 scrollbar-hide no-scrollbar",
      className
    )}>
      {symbols.map((symbol) => (
        <Button
          key={symbol}
          variant="ghost"
          size="sm"
          className="h-8 w-8 min-w-[32px] p-0 text-neutral-300 hover:text-white hover:bg-neutral-800"
          onClick={() => onInsert(symbol)}
        >
          {symbol}
        </Button>
      ))}
      <Button
        variant="ghost"
        size="sm"
        className="h-8 px-2 text-xs text-neutral-300 hover:text-white hover:bg-neutral-800"
        onClick={() => onInsert("\t")}
      >
        TAB
      </Button>
    </div>
  );
};

export default AccessoryBar;
