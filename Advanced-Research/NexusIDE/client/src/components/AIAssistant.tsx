import { FC, useState, useRef, useEffect } from "react";
import { RiRobotLine, RiDeleteBinLine, RiSendPlaneFill, RiAttachmentLine, RiCodeLine } from "react-icons/ri";
import { cn } from "@/lib/utils";
import { ChatMessage } from "@shared/schema";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import ReactMarkdown from 'react-markdown';

interface AIAssistantProps {
  messages: ChatMessage[];
  onSendMessage: (content: string) => void;
  onClearChat: () => void;
  isLoading?: boolean;
}

const AIAssistant: FC<AIAssistantProps> = ({
  messages,
  onSendMessage,
  onClearChat,
  isLoading = false
}) => {
  const [message, setMessage] = useState<string>("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = () => {
    if (message.trim() && !isLoading) {
      onSendMessage(message);
      setMessage("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Send message on Ctrl/Cmd + Enter
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  const insertCodeSnippet = () => {
    const codeTemplate = "```\n// Your code here\n```";
    setMessage(prev => prev + codeTemplate);
    textareaRef.current?.focus();
  };

  return (
    <div className="w-full md:w-80 bg-neutral-900 border-l border-neutral-800 flex flex-col h-full">
      {/* Assistant header */}
      <div className="px-4 py-3 border-b border-neutral-800 flex items-center justify-between">
        <div className="flex items-center">
          <div className="w-8 h-8 rounded-full bg-purple-600 flex items-center justify-center mr-2">
            <RiRobotLine className="text-white" />
          </div>
          <h2 className="font-medium">AI Assistant</h2>
        </div>
        <div>
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <button 
                  className="text-neutral-400 hover:text-neutral-100 transition-colors"
                  onClick={onClearChat}
                >
                  <RiDeleteBinLine />
                </button>
              </TooltipTrigger>
              <TooltipContent>
                <p>Clear chat history</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        </div>
      </div>
      
      {/* Chat area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, index) => (
          <div 
            key={`${msg.id}-${index}`}
            className={cn(
              "flex items-start",
              msg.role === "user" && "justify-end"
            )}
          >
            {msg.role === "assistant" && (
              <div className="w-8 h-8 rounded-full bg-purple-600 flex-shrink-0 flex items-center justify-center mr-2">
                <RiRobotLine className="text-white text-sm" />
              </div>
            )}
            
            <div className={cn(
              "rounded-lg p-3 max-w-[85%]",
              msg.role === "assistant" ? "bg-neutral-800" : "bg-primary bg-opacity-20"
            )}>
              <div className="text-sm prose prose-invert max-w-none prose-pre:bg-neutral-950 prose-pre:text-xs prose-pre:p-2 prose-pre:rounded prose-code:text-sky-300 prose-code:bg-neutral-950 prose-code:px-1 prose-code:py-0.5 prose-code:rounded">
                <ReactMarkdown>
                  {msg.content}
                </ReactMarkdown>
              </div>
            </div>
            
            {msg.role === "user" && (
              <div className="w-8 h-8 rounded-full bg-primary flex-shrink-0 flex items-center justify-center ml-2">
                <span className="text-white text-sm">U</span>
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
        
        {isLoading && (
          <div className="flex items-start">
            <div className="w-8 h-8 rounded-full bg-purple-600 flex-shrink-0 flex items-center justify-center mr-2">
              <RiRobotLine className="text-white text-sm" />
            </div>
            <div className="bg-neutral-800 rounded-lg p-3">
              <div className="flex space-x-2">
                <div className="h-2 w-2 bg-neutral-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></div>
                <div className="h-2 w-2 bg-neutral-400 rounded-full animate-bounce" style={{ animationDelay: "100ms" }}></div>
                <div className="h-2 w-2 bg-neutral-400 rounded-full animate-bounce" style={{ animationDelay: "200ms" }}></div>
              </div>
            </div>
          </div>
        )}
      </div>
      
      {/* Message input */}
      <div className="p-4 border-t border-neutral-800">
        <div className="relative">
          <textarea 
            ref={textareaRef}
            className="w-full bg-neutral-800 rounded-lg border border-neutral-700 px-4 py-3 pr-10 text-sm resize-none min-h-[80px] focus:outline-none focus:ring-1 focus:ring-primary"
            placeholder="Ask the AI assistant..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
          />
          <button 
            className={cn(
              "absolute right-3 bottom-3 text-primary hover:text-blue-400 transition-colors",
              isLoading && "opacity-50 cursor-not-allowed"
            )}
            onClick={handleSendMessage}
            disabled={isLoading}
          >
            <RiSendPlaneFill size={18} />
          </button>
        </div>
        <div className="flex justify-between items-center mt-2 text-xs text-neutral-500">
          <div>
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <button className="hover:text-neutral-300 transition-colors mr-3">
                    <RiAttachmentLine />
                  </button>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Upload file (coming soon)</p>
                </TooltipContent>
              </Tooltip>

              <Tooltip>
                <TooltipTrigger asChild>
                  <button 
                    className="hover:text-neutral-300 transition-colors"
                    onClick={insertCodeSnippet}
                  >
                    <RiCodeLine />
                  </button>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Insert code snippet</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>
          <div>Ctrl+Enter to send</div>
        </div>
      </div>
    </div>
  );
};

export default AIAssistant;
