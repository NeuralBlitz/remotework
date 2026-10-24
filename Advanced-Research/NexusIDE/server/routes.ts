import type { Express, Request, Response } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { insertChatMessageSchema, insertFileSchema, insertUserSchema } from "@shared/schema";
import { z } from "zod";
import { generateCodeCompletion, explainCode, suggestImprovements, chatWithAI } from "./services/aiService";
import { runJavaScript, runCommand, createProjectStructure } from "./services/fileService";

export async function registerRoutes(app: Express): Promise<Server> {
  const httpServer = createServer(app);
  
  // Setup WebSockets for real-time communication on a different path to avoid conflict with Vite HMR
  try {
    const WebSocket = await import('ws');
    
    // Create WebSocket server with a specific path to avoid conflicts
    const wss = new WebSocket.WebSocketServer({ 
      server: httpServer,
      path: '/ws/ide' // Use a specific path to avoid conflict with Vite's /_vite/ws
    });
    
    wss.on('connection', (ws) => {
      console.log('WebSocket client connected');
      
      ws.on('message', (message) => {
        try {
          console.log('Received message:', message.toString());
          // Handle WebSocket messages for real-time collaboration
        } catch (err) {
          console.error('Error processing message:', err);
        }
      });
      
      ws.on('error', (error) => {
        console.error('WebSocket client error:', error);
      });
      
      // Send initial connection message
      try {
        ws.send(JSON.stringify({ type: 'connection', message: 'Connected to IDE WebSocket server' }));
      } catch (err) {
        console.error('Error sending welcome message:', err);
      }
    });
    
    console.log('WebSocket server initialized successfully on /ws/ide path');
  } catch (error: any) {
    console.error('Failed to initialize WebSocket server:', error?.message || error);
  }
  
  // Authentication routes
  app.post('/api/auth/login', async (req: Request, res: Response) => {
    try {
      const { username, password } = req.body;
      
      if (!username || !password) {
        return res.status(400).json({ message: 'Username and password are required' });
      }
      
      const user = await storage.getUserByUsername(username);
      
      if (!user || user.password !== password) {
        return res.status(401).json({ message: 'Invalid username or password' });
      }
      
      // Store user in session (in a real app, we'd use proper session management)
      return res.json({ 
        id: user.id, 
        username: user.username 
      });
    } catch (error) {
      console.error('Login error:', error);
      return res.status(500).json({ message: 'Internal server error' });
    }
  });
  
  app.post('/api/auth/register', async (req: Request, res: Response) => {
    try {
      const result = insertUserSchema.safeParse(req.body);
      
      if (!result.success) {
        return res.status(400).json({ message: 'Invalid user data', errors: result.error.format() });
      }
      
      const existingUser = await storage.getUserByUsername(result.data.username);
      
      if (existingUser) {
        return res.status(409).json({ message: 'Username already exists' });
      }
      
      const user = await storage.createUser(result.data);
      
      // Create default project for new user
      await createProjectStructure(user.id, 'my-project');
      
      return res.status(201).json({ 
        id: user.id, 
        username: user.username 
      });
    } catch (error) {
      console.error('Registration error:', error);
      return res.status(500).json({ message: 'Internal server error' });
    }
  });
  
  // File system routes
  app.get('/api/files', async (req: Request, res: Response) => {
    try {
      const userId = parseInt(req.query.userId as string);
      
      if (isNaN(userId)) {
        return res.status(400).json({ message: 'Invalid user ID' });
      }
      
      const files = await storage.getFiles(userId);
      return res.json(files);
    } catch (error) {
      console.error('Get files error:', error);
      return res.status(500).json({ message: 'Internal server error' });
    }
  });
  
  app.get('/api/files/:id', async (req: Request, res: Response) => {
    try {
      const id = parseInt(req.params.id);
      
      if (isNaN(id)) {
        return res.status(400).json({ message: 'Invalid file ID' });
      }
      
      const file = await storage.getFile(id);
      
      if (!file) {
        return res.status(404).json({ message: 'File not found' });
      }
      
      return res.json(file);
    } catch (error) {
      console.error('Get file error:', error);
      return res.status(500).json({ message: 'Internal server error' });
    }
  });
  
  app.post('/api/files', async (req: Request, res: Response) => {
    try {
      const result = insertFileSchema.safeParse(req.body);
      
      if (!result.success) {
        return res.status(400).json({ message: 'Invalid file data', errors: result.error.format() });
      }
      
      const file = await storage.createFile(result.data);
      return res.status(201).json(file);
    } catch (error) {
      console.error('Create file error:', error);
      return res.status(500).json({ message: 'Internal server error' });
    }
  });
  
  app.put('/api/files/:id', async (req: Request, res: Response) => {
    try {
      const id = parseInt(req.params.id);
      const { content } = req.body;
      
      if (isNaN(id) || typeof content !== 'string') {
        return res.status(400).json({ message: 'Invalid request data' });
      }
      
      const file = await storage.updateFile(id, content);
      
      if (!file) {
        return res.status(404).json({ message: 'File not found' });
      }
      
      return res.json(file);
    } catch (error) {
      console.error('Update file error:', error);
      return res.status(500).json({ message: 'Internal server error' });
    }
  });
  
  app.delete('/api/files/:id', async (req: Request, res: Response) => {
    try {
      const id = parseInt(req.params.id);
      
      if (isNaN(id)) {
        return res.status(400).json({ message: 'Invalid file ID' });
      }
      
      const success = await storage.deleteFile(id);
      
      if (!success) {
        return res.status(404).json({ message: 'File not found' });
      }
      
      return res.json({ success: true });
    } catch (error) {
      console.error('Delete file error:', error);
      return res.status(500).json({ message: 'Internal server error' });
    }
  });
  
  app.post('/api/files/run', async (req: Request, res: Response) => {
    try {
      const { code, filename } = req.body;
      
      if (typeof code !== 'string' || typeof filename !== 'string') {
        return res.status(400).json({ message: 'Invalid request data' });
      }
      
      const result = await runJavaScript(code, filename);
      return res.json(result);
    } catch (error) {
      console.error('Run code error:', error);
      return res.status(500).json({ message: 'Internal server error' });
    }
  });
  
  // Terminal routes
  app.get('/api/terminal/:userId', async (req: Request, res: Response) => {
    try {
      const userId = parseInt(req.params.userId);
      
      if (isNaN(userId)) {
        return res.status(400).json({ message: 'Invalid user ID' });
      }
      
      let session = await storage.getTerminalSession(userId);
      
      if (!session) {
        session = await storage.createTerminalSession({ userId });
      }
      
      return res.json(session);
    } catch (error) {
      console.error('Get terminal error:', error);
      return res.status(500).json({ message: 'Internal server error' });
    }
  });
  
  app.post('/api/terminal/command', async (req: Request, res: Response) => {
    try {
      const { command, sessionId } = req.body;
      
      if (typeof command !== 'string' || typeof sessionId !== 'number') {
        return res.status(400).json({ message: 'Invalid request data' });
      }
      
      const result = await runCommand(command);
      
      // Append command and result to terminal output
      await storage.appendTerminalOutput(
        sessionId, 
        `$ ${command}\n${result.output}${result.error ? '\n' + result.error : ''}\n`
      );
      
      return res.json(result);
    } catch (error) {
      console.error('Run command error:', error);
      return res.status(500).json({ message: 'Internal server error' });
    }
  });
  
  app.post('/api/terminal/clear/:id', async (req: Request, res: Response) => {
    try {
      const id = parseInt(req.params.id);
      
      if (isNaN(id)) {
        return res.status(400).json({ message: 'Invalid session ID' });
      }
      
      const session = await storage.clearTerminalOutput(id);
      
      if (!session) {
        return res.status(404).json({ message: 'Terminal session not found' });
      }
      
      return res.json(session);
    } catch (error) {
      console.error('Clear terminal error:', error);
      return res.status(500).json({ message: 'Internal server error' });
    }
  });
  
  // AI routes
  app.post('/api/ai/generate', async (req: Request, res: Response) => {
    try {
      const { prompt, code } = req.body;
      
      if (typeof prompt !== 'string') {
        return res.status(400).json({ message: 'Invalid request data' });
      }
      
      const result = await generateCodeCompletion(prompt, code);
      return res.json(result);
    } catch (error: any) {
      console.error('Generate code error:', error);
      return res.status(500).json({ 
        message: error?.message || 'Failed to generate code' 
      });
    }
  });
  
  app.post('/api/ai/explain', async (req: Request, res: Response) => {
    try {
      const { code } = req.body;
      
      if (typeof code !== 'string') {
        return res.status(400).json({ message: 'Invalid request data' });
      }
      
      const result = await explainCode(code);
      return res.json(result);
    } catch (error: any) {
      console.error('Explain code error:', error);
      return res.status(500).json({ 
        message: error?.message || 'Failed to explain code' 
      });
    }
  });
  
  app.post('/api/ai/suggest', async (req: Request, res: Response) => {
    try {
      const { code } = req.body;
      
      if (typeof code !== 'string') {
        return res.status(400).json({ message: 'Invalid request data' });
      }
      
      const result = await suggestImprovements(code);
      return res.json(result);
    } catch (error: any) {
      console.error('Suggest improvements error:', error);
      return res.status(500).json({ 
        message: error?.message || 'Failed to suggest improvements' 
      });
    }
  });
  
  // Chat routes
  app.get('/api/chat/:userId', async (req: Request, res: Response) => {
    try {
      const userId = parseInt(req.params.userId);
      
      if (isNaN(userId)) {
        return res.status(400).json({ message: 'Invalid user ID' });
      }
      
      const messages = await storage.getChatMessages(userId);
      return res.json(messages);
    } catch (error) {
      console.error('Get chat messages error:', error);
      return res.status(500).json({ message: 'Internal server error' });
    }
  });
  
  app.post('/api/chat', async (req: Request, res: Response) => {
    try {
      const result = insertChatMessageSchema.safeParse(req.body);
      
      if (!result.success) {
        return res.status(400).json({ message: 'Invalid message data', errors: result.error.format() });
      }
      
      // Save user message
      const userMessage = await storage.createChatMessage(result.data);
      
      // Get chat history
      const messages = await storage.getChatMessages(result.data.userId, 10);
      
      // Format messages for Google AI
      const formattedMessages = messages.map(msg => ({
        role: msg.role,
        content: msg.content
      }));
      
      // Generate AI response
      const aiResponse = await chatWithAI(formattedMessages);
      
      // Save AI response
      const assistantMessage = await storage.createChatMessage({
        userId: result.data.userId,
        role: 'assistant',
        content: aiResponse
      });
      
      return res.json({
        userMessage,
        assistantMessage
      });
    } catch (error: any) {
      console.error('Send chat message error:', error);
      return res.status(500).json({ 
        message: error?.message || 'Internal server error' 
      });
    }
  });
  
  app.post('/api/chat/clear/:userId', async (req: Request, res: Response) => {
    try {
      const userId = parseInt(req.params.userId);
      
      if (isNaN(userId)) {
        return res.status(400).json({ message: 'Invalid user ID' });
      }
      
      const success = await storage.clearChatMessages(userId);
      
      if (!success) {
        return res.status(500).json({ message: 'Failed to clear chat messages' });
      }
      
      const messages = await storage.getChatMessages(userId);
      return res.json(messages);
    } catch (error) {
      console.error('Clear chat messages error:', error);
      return res.status(500).json({ message: 'Internal server error' });
    }
  });

  return httpServer;
}
