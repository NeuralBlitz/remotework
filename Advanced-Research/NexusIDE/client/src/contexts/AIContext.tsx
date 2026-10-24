import { createContext, useContext, useState, ReactNode, useEffect } from "react";
import { ChatMessage } from "@shared/schema";
import { apiRequest } from "@/lib/queryClient";
import { useToast } from "@/hooks/use-toast";

// Context interface
interface AIContextType {
  messages: ChatMessage[];
  isLoading: boolean;
  sendMessage: (content: string) => Promise<void>;
  clearChat: () => Promise<void>;
  generateCode: (prompt: string, code?: string) => Promise<{ code: string; explanation?: string; }>;
  explainCode: (code: string) => Promise<{ explanation: string; }>;
  suggestImprovements: (code: string) => Promise<{ suggestions: string[]; explanations: string[]; }>;
}

// Create context
const AIContext = createContext<AIContextType | undefined>(undefined);

// Provider component
export const AIProvider = ({ children }: { children: ReactNode }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const { toast } = useToast();

  // Mock user ID for demo - in a real app, this would come from auth
  const userId = 1;

  // Fetch chat messages on mount
  useEffect(() => {
    fetchMessages();
  }, []);

  // Fetch messages
  const fetchMessages = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`/api/chat/${userId}`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch chat messages: ${response.statusText}`);
      }
      
      const data = await response.json();
      setMessages(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      toast({
        title: "Error",
        description: `Failed to load chat history: ${message}`,
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Send message
  const sendMessage = async (content: string) => {
    try {
      setIsLoading(true);
      
      const response = await apiRequest("POST", "/api/chat", {
        userId,
        role: "user",
        content
      });
      
      const data = await response.json();
      
      // Refresh messages
      await fetchMessages();
      
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      toast({
        title: "Error",
        description: `Failed to send message: ${message}`,
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Clear chat
  const clearChat = async () => {
    try {
      setIsLoading(true);
      const response = await apiRequest("POST", `/api/chat/clear/${userId}`);
      
      if (!response.ok) {
        throw new Error(`Failed to clear chat: ${response.statusText}`);
      }
      
      const data = await response.json();
      setMessages(data);
      
      toast({
        title: "Success",
        description: "Chat history cleared"
      });
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      toast({
        title: "Error",
        description: `Failed to clear chat: ${message}`,
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Generate code
  const generateCode = async (prompt: string, code?: string) => {
    try {
      const response = await apiRequest("POST", "/api/ai/generate", {
        prompt,
        code
      });
      
      return await response.json();
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      toast({
        title: "Error",
        description: `Failed to generate code: ${message}`,
        variant: "destructive"
      });
      throw err;
    }
  };

  // Explain code
  const explainCode = async (code: string) => {
    try {
      const response = await apiRequest("POST", "/api/ai/explain", {
        code
      });
      
      return await response.json();
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      toast({
        title: "Error",
        description: `Failed to explain code: ${message}`,
        variant: "destructive"
      });
      throw err;
    }
  };

  // Suggest improvements
  const suggestImprovements = async (code: string) => {
    try {
      const response = await apiRequest("POST", "/api/ai/suggest", {
        code
      });
      
      return await response.json();
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      toast({
        title: "Error",
        description: `Failed to suggest improvements: ${message}`,
        variant: "destructive"
      });
      throw err;
    }
  };

  return (
    <AIContext.Provider
      value={{
        messages,
        isLoading,
        sendMessage,
        clearChat,
        generateCode,
        explainCode,
        suggestImprovements
      }}
    >
      {children}
    </AIContext.Provider>
  );
};

// Custom hook to use the AI context
export const useAI = () => {
  const context = useContext(AIContext);
  if (context === undefined) {
    throw new Error("useAI must be used within an AIProvider");
  }
  return context;
};
