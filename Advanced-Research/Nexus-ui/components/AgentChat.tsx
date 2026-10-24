import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles, Loader2, Cpu } from 'lucide-react';
import { ChatMessage, AgentModel, LogLevel } from '../types';
import { generateAgentResponse } from '../services/gemini';
import { logger } from '../services/logger';

interface AgentChatProps {
  onCodeReceived: (code: string) => void;
  onTerminalCommand: (cmd: string) => void;
}

export const AgentChat: React.FC<AgentChatProps> = ({ onCodeReceived, onTerminalCommand }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [model, setModel] = useState<AgentModel>(AgentModel.FAST);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Initial greeting
    setMessages([{
      id: 'init',
      role: 'model',
      text: "Nexus Online. I am capable of advanced web development and system administration. How can I assist you?",
      timestamp: new Date()
    }]);
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const parseResponse = (text: string) => {
    // Check for code blocks
    const htmlMatch = text.match(/```html([\s\S]*?)```/);
    if (htmlMatch && htmlMatch[1]) {
      onCodeReceived(htmlMatch[1].trim());
      logger.log('Extracted HTML code block from response', LogLevel.SYSTEM, 'PARSER');
    }

    // Check for bash commands
    const bashMatch = text.match(/```bash([\s\S]*?)```/);
    if (bashMatch && bashMatch[1]) {
      onTerminalCommand(bashMatch[1].trim());
      logger.log(`Extracted bash command: ${bashMatch[1].trim()}`, LogLevel.SYSTEM, 'PARSER');
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg: ChatMessage = {
      id: Math.random().toString(36),
      role: 'user',
      text: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);
    logger.log(`User query sent: ${input.substring(0, 50)}...`, LogLevel.INFO, 'CHAT');

    try {
      const history = messages.map(m => ({
        role: m.role,
        parts: [{ text: m.text }]
      }));
      
      const responseText = await generateAgentResponse(userMsg.text, history, model);
      
      const botMsg: ChatMessage = {
        id: Math.random().toString(36),
        role: 'model',
        text: responseText,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMsg]);
      parseResponse(responseText);

    } catch (err) {
      logger.log('Failed to receive response from agent', LogLevel.ERROR, 'CHAT');
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-900 border border-slate-800 rounded-lg shadow-xl overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-slate-950 border-b border-slate-800">
        <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-indigo-500/20 flex items-center justify-center border border-indigo-500/50">
                <Bot size={18} className="text-indigo-400" />
            </div>
            <div>
                <h3 className="text-sm font-bold text-white">Nexus Agent</h3>
                <div className="flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                    <span className="text-[10px] text-slate-400 uppercase tracking-wider">Online</span>
                </div>
            </div>
        </div>
        
        <div className="flex items-center bg-slate-900 rounded-lg p-1 border border-slate-800">
             <button 
                onClick={() => setModel(AgentModel.FAST)}
                className={`px-3 py-1 text-[10px] rounded-md transition-colors ${model === AgentModel.FAST ? 'bg-indigo-600 text-white' : 'text-slate-500 hover:text-slate-300'}`}
             >
                Flash
             </button>
             <button 
                onClick={() => setModel(AgentModel.ADVANCED)}
                className={`px-3 py-1 text-[10px] rounded-md transition-colors flex items-center gap-1 ${model === AgentModel.ADVANCED ? 'bg-purple-600 text-white' : 'text-slate-500 hover:text-slate-300'}`}
             >
                <Sparkles size={10} />
                Pro
             </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6 scroll-smooth bg-slate-900/50">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 
                ${msg.role === 'user' ? 'bg-slate-700 text-slate-300' : 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/20'}`}>
              {msg.role === 'user' ? <User size={16} /> : <Cpu size={16} />}
            </div>
            <div className={`flex flex-col max-w-[80%] ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div className={`px-4 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap
                  ${msg.role === 'user' 
                    ? 'bg-slate-800 text-slate-200 rounded-tr-none border border-slate-700' 
                    : 'bg-indigo-950/30 text-indigo-100 rounded-tl-none border border-indigo-500/20 shadow-sm'
                  }`}>
                {msg.text}
              </div>
              <span className="text-[10px] text-slate-600 mt-1 px-1">
                {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="flex gap-4">
            <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center shrink-0">
               <Cpu size={16} className="text-white animate-pulse" />
            </div>
            <div className="bg-indigo-950/30 border border-indigo-500/20 px-4 py-3 rounded-2xl rounded-tl-none flex items-center gap-2">
               <Loader2 size={14} className="animate-spin text-indigo-400" />
               <span className="text-xs text-indigo-300">Thinking...</span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="p-4 bg-slate-950 border-t border-slate-800">
        <div className="relative flex items-center">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask Nexus to write code or run commands..."
            className="w-full bg-slate-900 text-slate-200 text-sm rounded-xl border border-slate-700 p-3 pr-12 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 resize-none h-12 min-h-[48px] max-h-32 scrollbar-hide"
            rows={1}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isTyping}
            className="absolute right-2 p-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send size={16} />
          </button>
        </div>
        <div className="mt-2 flex justify-center text-[10px] text-slate-600 font-mono">
           Model: {model} • Secure Enclave Active
        </div>
      </div>
    </div>
  );
};
