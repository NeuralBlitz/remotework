import { create } from 'zustand';

export interface LogEntry {
  id: string;
  time: string;
  msg: string;
  type: 'info' | 'warn' | 'success';
  details?: string;
  category: 'neural' | 'epistemic' | 'data' | 'governance';
}

interface SimulatorState {
  blitzStatus: string;
  activeModel: string;
  activeMode: string;
  logs: LogEntry[];
  activeTokens: number;
  latency: number;
  
  setBlitzStatus: (status: string) => void;
  setActiveModel: (model: string) => void;
  setActiveMode: (mode: string) => void;
  addLog: (log: Omit<LogEntry, 'id' | 'time'>) => void;
  updateStats: (tokens: number, latency: number) => void;
}

export const useSimulator = create<SimulatorState>((set) => ({
  blitzStatus: "OPERATIONAL",
  activeModel: "Synergy-v9.8-Quantum",
  activeMode: "Holistic",
  logs: [
    { 
      id: '1', 
      time: new Date().toLocaleTimeString(), 
      msg: "System Initialized", 
      type: 'info', 
      category: 'neural',
      details: "Full system boot complete." 
    }
  ],
  activeTokens: 1200,
  latency: 12,

  setBlitzStatus: (blitzStatus) => set({ blitzStatus }),
  setActiveModel: (activeModel) => set({ activeModel }),
  setActiveMode: (activeMode) => set({ activeMode }),
  addLog: (log) => set((state) => ({
    logs: [...state.logs.slice(-100), {
      ...log,
      id: Math.random().toString(),
      time: new Date().toLocaleTimeString(),
    }] as LogEntry[]
  })),
  updateStats: (activeTokens, latency) => set({ activeTokens, latency }),
}));
