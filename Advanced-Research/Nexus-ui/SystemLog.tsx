import React, { useEffect, useState, useRef } from 'react';
import { Activity, XCircle, AlertTriangle, Info, ShieldCheck } from 'lucide-react';
import { logger } from '../services/logger';
import { LogEntry, LogLevel } from '../types';

export const SystemLog: React.FC = () => {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setLogs(logger.getHistory());
    const unsubscribe = logger.subscribe((entry) => {
      setLogs(prev => [...prev, entry]);
    });
    return unsubscribe;
  }, []);

  useEffect(() => {
    if (bottomRef.current) {
        bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [logs]);

  const getIcon = (level: LogLevel) => {
    switch (level) {
      case LogLevel.ERROR: return <XCircle size={12} className="text-red-500" />;
      case LogLevel.WARN: return <AlertTriangle size={12} className="text-yellow-500" />;
      case LogLevel.SYSTEM: return <ShieldCheck size={12} className="text-cyan-500" />;
      default: return <Info size={12} className="text-blue-500" />;
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-950/80 backdrop-blur-sm border-l border-slate-800 w-full text-xs font-mono">
      <div className="flex items-center gap-2 px-3 py-2 border-b border-slate-800 bg-slate-900/50">
        <Activity size={14} className="text-emerald-400" />
        <span className="font-bold text-slate-300 uppercase tracking-widest text-[10px]">System Log</span>
      </div>
      <div className="flex-1 overflow-y-auto p-2 space-y-1.5">
        {logs.map(log => (
          <div key={log.id} className="flex gap-2 items-start opacity-80 hover:opacity-100 transition-opacity">
            <span className="text-slate-600 shrink-0">[{log.timestamp.toLocaleTimeString([], { hour12: false })}]</span>
            <span className="mt-0.5 shrink-0">{getIcon(log.level)}</span>
            <span className="text-slate-500 font-bold shrink-0 w-16 truncate text-[10px] uppercase tracking-wider text-right">{log.source}</span>
            <span className={`break-all ${
                log.level === LogLevel.ERROR ? 'text-red-400' : 
                log.level === LogLevel.WARN ? 'text-yellow-400' : 
                log.level === LogLevel.SYSTEM ? 'text-cyan-400' : 'text-slate-300'
            }`}>
              {log.message}
            </span>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  );
};
