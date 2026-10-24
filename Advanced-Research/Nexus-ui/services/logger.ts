import { LogEntry, LogLevel } from '../types';

type LogListener = (entry: LogEntry) => void;

class LoggerService {
  private listeners: LogListener[] = [];
  private logs: LogEntry[] = [];

  public log(message: string, level: LogLevel = LogLevel.INFO, source: string = 'SYSTEM') {
    const entry: LogEntry = {
      id: Math.random().toString(36).substring(7),
      timestamp: new Date(),
      level,
      message,
      source
    };
    
    this.logs.push(entry);
    // Keep only last 1000 logs
    if (this.logs.length > 1000) this.logs.shift();
    
    this.notify(entry);
  }

  public subscribe(listener: LogListener): () => void {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  private notify(entry: LogEntry) {
    this.listeners.forEach(l => l(entry));
  }

  public getHistory(): LogEntry[] {
    return [...this.logs];
  }
}

export const logger = new LoggerService();
