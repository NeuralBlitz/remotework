import React, { useState, useEffect, useRef } from 'react';
import { Terminal as TerminalIcon, Play, RefreshCw, Trash2 } from 'lucide-react';
import { TerminalLine, LogLevel } from '../types';
import { logger } from '../services/logger';

interface TerminalProps {
  onCommand?: (cmd: string) => void;
  externalOutput?: string | null;
}

export const Terminal: React.FC<TerminalProps> = ({ onCommand, externalOutput }) => {
  const [lines, setLines] = useState<TerminalLine[]>([
    { id: 'init', type: 'system', content: 'Nexus OS v2.4.0 initialized...' },
    { id: 'init2', type: 'system', content: 'Type "help" for available commands.' }
  ]);
  const [input, setInput] = useState('');
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [lines]);

  useEffect(() => {
    if (externalOutput) {
       addOutput(externalOutput);
       logger.log(`External process output received`, LogLevel.INFO, 'TERMINAL');
    }
  }, [externalOutput]);

  const addLine = (type: TerminalLine['type'], content: string) => {
    setLines(prev => [...prev, { id: Math.random().toString(36), type, content }]);
  };

  const addOutput = (text: string) => {
    // Split by newlines to make it look real
    text.split('\n').forEach(line => {
      if (line.trim()) addLine('output', line);
    });
  };

  const handleCommand = (cmd: string) => {
    const trimmed = cmd.trim();
    if (!trimmed) return;

    logger.log(`Command executed: ${trimmed}`, LogLevel.INFO, 'TERMINAL');
    addLine('input', `> ${trimmed}`);

    // Internal commands
    switch (trimmed.toLowerCase()) {
      case 'clear':
        setLines([]);
        break;
      case 'help':
        addOutput(`
Available Commands:
  help      - Show this help message
  clear     - Clear terminal history
  status    - Check system status
  deploy    - Simulate deployment
  whoami    - Current user info
        `);
        break;
      case 'status':
        addOutput('System: ONLINE\nConnection: SECURE\nLatency: 12ms');
        break;
      case 'whoami':
        addOutput('User: Administrator\nPermissions: ROOT');
        break;
      case 'deploy':
        addOutput('Initiating deployment sequence...');
        setTimeout(() => addOutput('[Build] Compiling assets...'), 500);
        setTimeout(() => addOutput('[Build] Minifying scripts...'), 1200);
        setTimeout(() => addOutput('[Deploy] Uploading to edge...'), 2000);
        setTimeout(() => addOutput('Success: Deployment active at v4.2.1'), 2800);
        break;
      default:
        // Pass to parent or show error
        if (onCommand) {
             // Mock executing arbitrary bash
             setTimeout(() => {
                addOutput(`command not found: ${trimmed}`);
             }, 200);
        }
        break;
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleCommand(input);
    setInput('');
  };

  return (
    <div className="flex flex-col h-full bg-slate-950 border border-slate-800 rounded-lg overflow-hidden shadow-2xl font-mono text-sm">
      <div className="flex items-center justify-between px-4 py-2 bg-slate-900 border-b border-slate-800">
        <div className="flex items-center gap-2 text-slate-400">
          <TerminalIcon size={16} />
          <span className="font-semibold tracking-wider text-xs uppercase">Terminal</span>
        </div>
        <div className="flex gap-2">
            <button onClick={() => setLines([])} className="text-slate-500 hover:text-red-400 transition-colors">
                <Trash2 size={14} />
            </button>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-1 bg-black/50">
        {lines.map(line => (
          <div key={line.id} className={`
            ${line.type === 'input' ? 'text-yellow-400 font-bold' : ''}
            ${line.type === 'output' ? 'text-slate-300' : ''}
            ${line.type === 'error' ? 'text-red-500' : ''}
            ${line.type === 'system' ? 'text-cyan-500' : ''}
          `}>
            {line.content}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <form onSubmit={handleSubmit} className="p-2 bg-slate-900 border-t border-slate-800 flex gap-2">
        <span className="text-green-500 font-bold select-none">{'>'}</span>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 bg-transparent border-none outline-none text-green-400 placeholder-slate-700"
          placeholder="Enter command..."
          autoFocus
        />
      </form>
    </div>
  );
};
