import { FC, useState, useRef, useEffect } from "react";
import { RiTerminalBoxLine, RiPlayLine } from "react-icons/ri";
import { cn } from "@/lib/utils";

interface TerminalProps {
  output: string;
  command: string;
  onCommandChange: (command: string) => void;
  onRunCommand: () => void;
  onRunFile?: () => void;
}

const Terminal: FC<TerminalProps> = ({
  output,
  command,
  onCommandChange,
  onRunCommand,
  onRunFile
}) => {
  const outputRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll to bottom when output changes
  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [output]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      onRunCommand();
    }
  };

  return (
    <div className="border-t border-neutral-800 h-48 bg-neutral-950">
      <div className="flex items-center justify-between px-4 py-2 bg-neutral-900 border-b border-neutral-800">
        <div className="flex items-center">
          <RiTerminalBoxLine className="mr-2" />
          <h3 className="text-sm font-medium">Terminal</h3>
        </div>
        {onRunFile && (
          <div>
            <button 
              className="text-xs px-2 py-1 rounded bg-primary text-white hover:bg-blue-700 transition-colors flex items-center"
              onClick={onRunFile}
            >
              <RiPlayLine className="mr-1" /> Run
            </button>
          </div>
        )}
      </div>
      <div className="h-[calc(100%-36px)] flex flex-col">
        <div 
          ref={outputRef} 
          className="flex-1 overflow-auto p-2 font-mono text-sm whitespace-pre-wrap"
        >
          {output ? (
            <div dangerouslySetInnerHTML={{ __html: formatTerminalOutput(output) }} />
          ) : (
            <div className="text-neutral-500">Terminal initialized. Type commands below.</div>
          )}
        </div>
        <div className="flex items-center px-2 py-1">
          <span className="text-green-500 mr-2">$</span>
          <input
            ref={inputRef}
            type="text"
            className="bg-transparent border-none outline-none flex-1 text-neutral-100 font-mono"
            placeholder="Enter command..."
            value={command}
            onChange={(e) => onCommandChange(e.target.value)}
            onKeyDown={handleKeyDown}
          />
        </div>
      </div>
    </div>
  );
};

// Helper function to format terminal output with colors
const formatTerminalOutput = (output: string): string => {
  // Add color to common terminal outputs
  return output
    .replace(/\$/g, '<span class="text-green-500">$</span>')
    .replace(/(error|Error|ERROR|failed|Failed|FAILED)/g, '<span class="text-red-500">$1</span>')
    .replace(/(warning|Warning|WARNING)/g, '<span class="text-yellow-400">$1</span>')
    .replace(/(success|Success|SUCCESS)/g, '<span class="text-green-500">$1</span>')
    .replace(/(https?:\/\/\S+)/g, '<span class="text-blue-400">$1</span>');
};

export default Terminal;
