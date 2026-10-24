import { createContext, useContext, useState, ReactNode, useEffect } from "react";
import { apiRequest } from "@/lib/queryClient";
import { useToast } from "@/hooks/use-toast";

// Context interface
interface TerminalContextType {
  output: string;
  command: string;
  isLoading: boolean;
  sessionId: number | null;
  setCommand: (command: string) => void;
  runCommand: () => Promise<void>;
  clearTerminal: () => Promise<void>;
  appendOutput: (text: string) => void;
}

// Create context
const TerminalContext = createContext<TerminalContextType | undefined>(undefined);

// Provider component
export const TerminalProvider = ({ children }: { children: ReactNode }) => {
  const [output, setOutput] = useState<string>("");
  const [command, setCommand] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [sessionId, setSessionId] = useState<number | null>(null);
  const { toast } = useToast();

  // Mock user ID for demo - in a real app, this would come from auth
  const userId = 1;

  // Initialize terminal session
  useEffect(() => {
    initTerminal();
  }, []);

  // Listen for terminal output events
  useEffect(() => {
    const handleTerminalOutput = (event: CustomEvent) => {
      const { command, output, isError } = event.detail;
      const formattedOutput = isError
        ? `$ ${command}\n\x1B[31m${output}\x1B[0m\n`
        : `$ ${command}\n${output}\n`;
      
      appendOutput(formattedOutput);
    };
    
    document.addEventListener('terminal-output', handleTerminalOutput as EventListener);
    
    return () => {
      document.removeEventListener('terminal-output', handleTerminalOutput as EventListener);
    };
  }, []);

  // Initialize terminal
  const initTerminal = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`/api/terminal/${userId}`);
      
      if (!response.ok) {
        throw new Error(`Failed to initialize terminal: ${response.statusText}`);
      }
      
      const data = await response.json();
      setSessionId(data.id);
      setOutput(data.output || "Terminal initialized.\n");
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      toast({
        title: "Error",
        description: `Failed to initialize terminal: ${message}`,
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Run command
  const runCommand = async () => {
    if (!command.trim() || !sessionId) return;
    
    try {
      setIsLoading(true);
      
      // Append command to output immediately
      const cmdOutput = `$ ${command}\n`;
      appendOutput(cmdOutput);
      
      const response = await apiRequest("POST", "/api/terminal/command", {
        command,
        sessionId
      });
      
      const result = await response.json();
      
      // Append result to output
      const resultOutput = `${result.output || ""}${result.error ? `\n${result.error}` : ""}\n`;
      appendOutput(resultOutput);
      
      // Clear command
      setCommand("");
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      appendOutput(`Error: ${message}\n`);
      toast({
        title: "Error",
        description: `Failed to run command: ${message}`,
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Clear terminal
  const clearTerminal = async () => {
    if (!sessionId) return;
    
    try {
      setIsLoading(true);
      const response = await apiRequest("POST", `/api/terminal/clear/${sessionId}`);
      
      if (!response.ok) {
        throw new Error(`Failed to clear terminal: ${response.statusText}`);
      }
      
      setOutput("");
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      toast({
        title: "Error",
        description: `Failed to clear terminal: ${message}`,
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Append text to output
  const appendOutput = (text: string) => {
    setOutput(prev => prev + text);
  };

  return (
    <TerminalContext.Provider
      value={{
        output,
        command,
        isLoading,
        sessionId,
        setCommand,
        runCommand,
        clearTerminal,
        appendOutput
      }}
    >
      {children}
    </TerminalContext.Provider>
  );
};

// Custom hook to use the Terminal context
export const useTerminal = () => {
  const context = useContext(TerminalContext);
  if (context === undefined) {
    throw new Error("useTerminal must be used within a TerminalProvider");
  }
  return context;
};
