import { 
  users, type User, type InsertUser,
  files, type File, type InsertFile,
  chatMessages, type ChatMessage, type InsertChatMessage,
  terminalSessions, type TerminalSession, type InsertTerminalSession,
  FileNode
} from "@shared/schema";

export interface IStorage {
  // User operations
  getUser(id: number): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;

  // File operations
  getFiles(userId: number): Promise<FileNode[]>;
  getFile(id: number): Promise<File | undefined>;
  getFileByPath(userId: number, path: string): Promise<File | undefined>;
  createFile(file: InsertFile): Promise<File>;
  updateFile(id: number, content: string): Promise<File | undefined>;
  deleteFile(id: number): Promise<boolean>;

  // Chat operations
  getChatMessages(userId: number, limit?: number): Promise<ChatMessage[]>;
  createChatMessage(message: InsertChatMessage): Promise<ChatMessage>;
  clearChatMessages(userId: number): Promise<boolean>;

  // Terminal operations
  getTerminalSession(userId: number): Promise<TerminalSession | undefined>;
  createTerminalSession(session: InsertTerminalSession): Promise<TerminalSession>;
  appendTerminalOutput(id: number, output: string): Promise<TerminalSession | undefined>;
  clearTerminalOutput(id: number): Promise<TerminalSession | undefined>;
}

export class MemStorage implements IStorage {
  private users: Map<number, User>;
  private files: Map<number, File>;
  private chatMessages: Map<number, ChatMessage>;
  private terminalSessions: Map<number, TerminalSession>;
  
  private userIdCounter: number;
  private fileIdCounter: number;
  private messageIdCounter: number;
  private sessionIdCounter: number;

  constructor() {
    this.users = new Map();
    this.files = new Map();
    this.chatMessages = new Map();
    this.terminalSessions = new Map();
    
    this.userIdCounter = 1;
    this.fileIdCounter = 1;
    this.messageIdCounter = 1;
    this.sessionIdCounter = 1;

    // Initialize with sample data
    this.initializeStorage();
  }

  private initializeStorage() {
    // Create a demo user
    const demoUser: User = {
      id: this.userIdCounter++,
      username: 'demo',
      password: 'password' // In a real app, this would be hashed
    };
    this.users.set(demoUser.id, demoUser);

    // Create sample project structure
    const rootFolder: File = {
      id: this.fileIdCounter++,
      userId: demoUser.id,
      name: 'my-project',
      path: '/my-project',
      content: '',
      isFolder: true,
      parentId: null,
      createdAt: new Date(),
      updatedAt: new Date()
    };
    this.files.set(rootFolder.id, rootFolder);

    const srcFolder: File = {
      id: this.fileIdCounter++,
      userId: demoUser.id,
      name: 'src',
      path: '/my-project/src',
      content: '',
      isFolder: true,
      parentId: rootFolder.id,
      createdAt: new Date(),
      updatedAt: new Date()
    };
    this.files.set(srcFolder.id, srcFolder);

    const appJsFile: File = {
      id: this.fileIdCounter++,
      userId: demoUser.id,
      name: 'app.js',
      path: '/my-project/src/app.js',
      content: `// Simple React component with AI-powered features
import React, { useState, useEffect } from 'react';
import { useAI } from './utils';

const CodeGenerator = () => {
  const [prompt, setPrompt] = useState('');
  const [code, setCode] = useState('');
  const { generateCode, isLoading, error } = useAI();

  const handleSubmit = async () => {
    try {
      const result = await generateCode(prompt);
      setCode(result);
    } catch (err) {
      console.error(err);
    }
  };

  // Component render code goes here...
}`,
      isFolder: false,
      parentId: srcFolder.id,
      createdAt: new Date(),
      updatedAt: new Date()
    };
    this.files.set(appJsFile.id, appJsFile);

    const utilsJsFile: File = {
      id: this.fileIdCounter++,
      userId: demoUser.id,
      name: 'utils.js',
      path: '/my-project/src/utils.js',
      content: `// AI utilities
export const useAI = () => {
  const generateCode = async (prompt) => {
    const response = await fetch('/api/ai/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    });
    
    if (!response.ok) {
      throw new Error('Failed to generate code');
    }
    
    const data = await response.json();
    return data.code;
  };
  
  return {
    generateCode,
    isLoading: false,
    error: null,
  };
};`,
      isFolder: false,
      parentId: srcFolder.id,
      createdAt: new Date(),
      updatedAt: new Date()
    };
    this.files.set(utilsJsFile.id, utilsJsFile);

    const readmeFile: File = {
      id: this.fileIdCounter++,
      userId: demoUser.id,
      name: 'README.md',
      path: '/my-project/README.md',
      content: `# My Project

A project with AI-assisted coding.

## Getting Started

1. Clone the repository
2. Install dependencies
3. Run the development server`,
      isFolder: false,
      parentId: rootFolder.id,
      createdAt: new Date(),
      updatedAt: new Date()
    };
    this.files.set(readmeFile.id, readmeFile);

    const packageJsonFile: File = {
      id: this.fileIdCounter++,
      userId: demoUser.id,
      name: 'package.json',
      path: '/my-project/package.json',
      content: `{
  "name": "my-project",
  "version": "1.0.0",
  "description": "A project with AI-assisted coding",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.17.1",
    "react": "^17.0.2",
    "react-dom": "^17.0.2"
  },
  "devDependencies": {
    "nodemon": "^2.0.7",
    "jest": "^27.0.6"
  }
}`,
      isFolder: false,
      parentId: rootFolder.id,
      createdAt: new Date(),
      updatedAt: new Date()
    };
    this.files.set(packageJsonFile.id, packageJsonFile);

    // Create initial welcome message from AI
    const welcomeMessage: ChatMessage = {
      id: this.messageIdCounter++,
      userId: demoUser.id,
      role: "assistant",
      content: "Hello! I'm your AI coding assistant. How can I help you with your project today?",
      createdAt: new Date()
    };
    this.chatMessages.set(welcomeMessage.id, welcomeMessage);

    // Create initial terminal session
    const initialSession: TerminalSession = {
      id: this.sessionIdCounter++,
      userId: demoUser.id,
      output: "",
      createdAt: new Date(),
      updatedAt: new Date()
    };
    this.terminalSessions.set(initialSession.id, initialSession);
  }

  // Convert flat file structure to hierarchical for client
  private buildFileTree(userId: number): FileNode[] {
    const allFiles = Array.from(this.files.values()).filter(file => file.userId === userId);
    const rootFiles = allFiles.filter(file => !file.parentId);
    
    const buildNode = (file: File): FileNode => {
      const node: FileNode = {
        id: file.id,
        name: file.name,
        path: file.path,
        isFolder: file.isFolder || false,
        content: file.content || undefined,
        children: []
      };
      
      if (file.isFolder) {
        node.children = allFiles
          .filter(child => child.parentId === file.id)
          .map(child => buildNode(child));
      }
      
      return node;
    };
    
    return rootFiles.map(file => buildNode(file));
  }

  // User operations
  async getUser(id: number): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.username === username,
    );
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = this.userIdCounter++;
    const user: User = { ...insertUser, id };
    this.users.set(id, user);
    return user;
  }

  // File operations
  async getFiles(userId: number): Promise<FileNode[]> {
    return this.buildFileTree(userId);
  }

  async getFile(id: number): Promise<File | undefined> {
    return this.files.get(id);
  }

  async getFileByPath(userId: number, path: string): Promise<File | undefined> {
    return Array.from(this.files.values()).find(
      file => file.userId === userId && file.path === path
    );
  }

  async createFile(file: InsertFile): Promise<File> {
    const id = this.fileIdCounter++;
    const now = new Date();
    const newFile: File = { 
      ...file, 
      id, 
      content: file.content || "",
      isFolder: file.isFolder || false,
      parentId: file.parentId || null,
      createdAt: now, 
      updatedAt: now 
    };
    this.files.set(id, newFile);
    return newFile;
  }

  async updateFile(id: number, content: string): Promise<File | undefined> {
    const file = this.files.get(id);
    if (!file) return undefined;
    
    const updatedFile: File = { 
      ...file, 
      content, 
      updatedAt: new Date() 
    };
    this.files.set(id, updatedFile);
    return updatedFile;
  }

  async deleteFile(id: number): Promise<boolean> {
    const file = this.files.get(id);
    if (!file) return false;
    
    // If it's a folder, delete all children
    if (file.isFolder) {
      const childrenIds: number[] = [];
      
      const findChildren = (parentId: number) => {
        Array.from(this.files.values())
          .filter(f => f.parentId === parentId)
          .forEach(child => {
            childrenIds.push(child.id);
            if (child.isFolder) {
              findChildren(child.id);
            }
          });
      };
      
      findChildren(id);
      
      childrenIds.forEach(childId => {
        this.files.delete(childId);
      });
    }
    
    return this.files.delete(id);
  }

  // Chat operations
  async getChatMessages(userId: number, limit?: number): Promise<ChatMessage[]> {
    const userMessages = Array.from(this.chatMessages.values())
      .filter(msg => msg.userId === userId)
      .sort((a, b) => (a.createdAt?.getTime() || 0) - (b.createdAt?.getTime() || 0));
    
    return limit ? userMessages.slice(-limit) : userMessages;
  }

  async createChatMessage(message: InsertChatMessage): Promise<ChatMessage> {
    const id = this.messageIdCounter++;
    const newMessage: ChatMessage = { 
      ...message, 
      id, 
      createdAt: new Date() 
    };
    this.chatMessages.set(id, newMessage);
    return newMessage;
  }

  async clearChatMessages(userId: number): Promise<boolean> {
    const messagesToDelete = Array.from(this.chatMessages.values())
      .filter(msg => msg.userId === userId)
      .map(msg => msg.id);
    
    messagesToDelete.forEach(id => {
      this.chatMessages.delete(id);
    });
    
    // Add a new welcome message
    const welcomeMessage: ChatMessage = {
      id: this.messageIdCounter++,
      userId,
      role: "assistant",
      content: "Chat history cleared. How can I help you with your project?",
      createdAt: new Date()
    };
    this.chatMessages.set(welcomeMessage.id, welcomeMessage);
    
    return true;
  }

  // Terminal operations
  async getTerminalSession(userId: number): Promise<TerminalSession | undefined> {
    return Array.from(this.terminalSessions.values()).find(
      session => session.userId === userId
    );
  }

  async createTerminalSession(session: InsertTerminalSession): Promise<TerminalSession> {
    const id = this.sessionIdCounter++;
    const now = new Date();
    const newSession: TerminalSession = { 
      ...session, 
      id, 
      output: "", 
      createdAt: now, 
      updatedAt: now 
    };
    this.terminalSessions.set(id, newSession);
    return newSession;
  }

  async appendTerminalOutput(id: number, output: string): Promise<TerminalSession | undefined> {
    const session = this.terminalSessions.get(id);
    if (!session) return undefined;
    
    const updatedSession: TerminalSession = { 
      ...session, 
      output: session.output + output, 
      updatedAt: new Date() 
    };
    this.terminalSessions.set(id, updatedSession);
    return updatedSession;
  }

  async clearTerminalOutput(id: number): Promise<TerminalSession | undefined> {
    const session = this.terminalSessions.get(id);
    if (!session) return undefined;
    
    const updatedSession: TerminalSession = { 
      ...session, 
      output: "", 
      updatedAt: new Date() 
    };
    this.terminalSessions.set(id, updatedSession);
    return updatedSession;
  }
}

export const storage = new MemStorage();
