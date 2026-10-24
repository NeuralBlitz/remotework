import { GoogleGenAI } from "@google/genai";
import { logger } from './logger';
import { LogLevel, AgentModel } from '../types';

let aiInstance: GoogleGenAI | null = null;

const getAI = () => {
  if (!aiInstance) {
    if (!process.env.API_KEY) {
      logger.log('API Key missing', LogLevel.ERROR, 'GEMINI');
      throw new Error("API Key not found");
    }
    aiInstance = new GoogleGenAI({ apiKey: process.env.API_KEY });
  }
  return aiInstance;
};

export const generateAgentResponse = async (
  prompt: string, 
  history: { role: string; parts: { text: string }[] }[],
  model: AgentModel = AgentModel.ADVANCED
): Promise<string> => {
  try {
    logger.log(`Generating response with model: ${model}`, LogLevel.INFO, 'GEMINI');
    
    const ai = getAI();
    
    // Convert history to format expected by @google/genai if necessary, 
    // or simply use generateContent with the prompt if no history is needed for this specific call.
    // However, for a chat agent, we usually want history. 
    // The @google/genai `chats.create` is best for stateful chat.
    // But to keep it stateless/flexible here, we'll pass history as contents list if manually managing,
    // or just use `generateContent` with a big prompt context. 
    
    // Let's use the chat API for better context management.
    const chat = ai.chats.create({
      model: model,
      config: {
        systemInstruction: `You are Nexus, a super-advanced AI agent.
        You have access to a simulated environment with:
        1. A Web Development Workspace (You can write HTML/CSS/JS).
        2. A Terminal (You can suggest bash commands).
        
        FORMATTING RULES:
        - If you write code for the web workspace, wrap it in \`\`\`html\`\`\` (include CSS/JS in the HTML for simplicity).
        - If you suggest a terminal command to run, wrap it in \`\`\`bash\`\`\`.
        - Be concise, technical, and professional.
        - Analyze the user's request and determine the best tool to use.
        `,
      },
      history: history.map(h => ({
        role: h.role,
        parts: h.parts
      }))
    });

    const result = await chat.sendMessage({ message: prompt });
    
    if (result.text) {
      logger.log('Response generated successfully', LogLevel.INFO, 'GEMINI');
      return result.text;
    } else {
      throw new Error("Empty response from model");
    }

  } catch (error) {
    logger.log(`Error generating response: ${error}`, LogLevel.ERROR, 'GEMINI');
    return "Error: Unable to connect to Nexus Core. Check API Key or Network.";
  }
};
