export enum LogLevel {
  INFO = 'INFO',
  WARN = 'WARN',
  ERROR = 'ERROR',
  SYSTEM = 'SYSTEM'
}

export interface LogEntry {
  id: string;
  timestamp: Date;
  level: LogLevel;
  message: string;
  source: string;
}

export interface TerminalLine {
  id: string;
  type: 'input' | 'output' | 'error' | 'system';
  content: string;
}

export interface CodeFile {
  name: string;
  language: string;
  content: string;
}

export enum AgentModel {
  FAST = 'gemini-3-flash-preview',
  ADVANCED = 'gemini-3-pro-preview'
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'model';
  text: string;
  timestamp: Date;
}

export type ProjectStatus = 'online' | 'offline' | 'building' | 'error';

export interface Project {
  id: string;
  name: string;
  description: string;
  status: ProjectStatus;
  framework: 'react' | 'node' | 'python' | 'html';
  lastActive: Date;
  cpu: number;
  memory: number;
  port: number;
}
