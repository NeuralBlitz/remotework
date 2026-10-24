# Web-based IDE Project

## Project Overview
A comprehensive web-based integrated development environment (IDE) with AI-powered code assistance, real-time collaboration, and full-stack development capabilities.

## Tech Stack
- **Frontend**: React 18, TypeScript, Vite
- **Backend**: Node.js, Express, TypeScript  
- **AI Integration**: Google Gemini AI
- **WebSockets**: Custom WebSocket server for real-time features
- **Storage**: In-memory storage (MemStorage)
- **UI Components**: shadcn/ui, Tailwind CSS
- **State Management**: React Context, TanStack Query

## Project Architecture

### Server Architecture
- Express server with TypeScript
- WebSocket server for real-time communication
- AI service integration for code generation and assistance
- File system service for project management
- In-memory storage for development

### Client Architecture  
- React SPA with multiple contexts for state management
- Code editor with Monaco Editor
- File explorer with hierarchical structure
- AI assistant chat interface
- Terminal emulator
- Real-time collaboration features

## Current Issues
- WebSocket frame parsing error preventing application startup
- Conflict between custom WebSocket server and Vite's HMR WebSocket
- LSP diagnostics showing 6 issues across server files

## Development Status
- Project structure complete
- Core components implemented
- AI integration configured
- Currently debugging WebSocket conflicts

## User Preferences
- Language: English
- Communication style: Technical and direct
- Focus: Debugging and fixing application startup issues

## Recent Changes
- Initial project setup with full-stack architecture
- WebSocket server implementation for real-time features
- AI assistant integration with Google Gemini
- In-memory storage implementation with sample data

## Next Steps
- Fix WebSocket conflicts preventing startup
- Resolve LSP diagnostics
- Test application functionality
- Deploy working solution