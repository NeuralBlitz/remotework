import { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } from "@google/generative-ai";

const API_KEY = process.env.GOOGLE_API_KEY || process.env.OPENAI_API_KEY || "";

if (!API_KEY) {
  console.warn("Warning: No Google AI API key provided. AI features will not work.");
}

// Initialize Google Generative AI with your API key
const genAI = new GoogleGenerativeAI(API_KEY);

// Model configuration - using Gemini 1.5 Pro
const MODEL_NAME = "gemini-1.5-pro";

export interface CodeCompletion {
  code: string;
  explanation?: string;
}

export interface CodeExplanation {
  explanation: string;
}

export interface CodeSuggestion {
  suggestions: string[];
  explanations: string[];
}

export async function generateCodeCompletion(prompt: string, code?: string): Promise<CodeCompletion> {
  try {
    if (!API_KEY) {
      throw new Error("Google AI API key not configured");
    }

    // Get the model
    const model = genAI.getGenerativeModel({ model: MODEL_NAME });

    // Create prompt with context
    const systemContent = `You are an expert programming assistant. Provide helpful, accurate, and efficient code based on the user's request. 
    Include explanations when helpful. Always prioritize best practices, security, and performance.`;

    const userContent = code 
      ? `${prompt}\n\nCurrent code:\n\`\`\`\n${code}\n\`\`\``
      : prompt;

    const fullPrompt = `${systemContent}\n\n${userContent}\n\nRespond in JSON format with 'code' and 'explanation' fields.`;

    // Generate content
    const result = await model.generateContent(fullPrompt);
    const response = result.response;
    const text = response.text();

    if (!text) {
      throw new Error("No response from Google AI");
    }

    try {
      // Try to parse as JSON
      const jsonMatch = text.match(/```json\n([\s\S]*?)\n```/) || text.match(/\{[\s\S]*\}/);
      let jsonResponse;
      
      if (jsonMatch) {
        jsonResponse = JSON.parse(jsonMatch[0].replace(/```json\n/, '').replace(/\n```/, ''));
      } else {
        // If not valid JSON, extract code blocks
        const codeBlockRegex = /```(?:[\w]*)\n([\s\S]*?)```/g;
        let match;
        const matches = [];
        
        while ((match = codeBlockRegex.exec(text)) !== null) {
          matches.push(match);
        }
        
        if (matches.length > 0) {
          return {
            code: matches[0][1],
            explanation: text.replace(codeBlockRegex, "").trim()
          };
        }
        
        return { 
          code: "", 
          explanation: text 
        };
      }
      
      return {
        code: jsonResponse.code || "",
        explanation: jsonResponse.explanation || ""
      };
    } catch (e) {
      // If parsing fails, extract code blocks
      const codeBlockRegex = /```(?:[\w]*)\n([\s\S]*?)```/g;
      let match;
      const matches = [];
      
      while ((match = codeBlockRegex.exec(text)) !== null) {
        matches.push(match);
      }
      
      if (matches.length > 0) {
        return {
          code: matches[0][1],
          explanation: text.replace(codeBlockRegex, "").trim()
        };
      }
      
      return { 
        code: "", 
        explanation: text 
      };
    }
  } catch (error) {
    console.error("Error generating code completion:", error);
    throw error;
  }
}

export async function explainCode(code: string): Promise<CodeExplanation> {
  try {
    if (!API_KEY) {
      throw new Error("Google AI API key not configured");
    }

    // Get the model
    const model = genAI.getGenerativeModel({ model: MODEL_NAME });

    // Create prompt with context
    const prompt = `You are an expert programming tutor. Explain the following code in a clear, concise way.
    
    Code to explain:
    \`\`\`
    ${code}
    \`\`\`

    Respond in JSON format with an 'explanation' field containing your explanation.`;

    // Generate content
    const result = await model.generateContent(prompt);
    const response = result.response;
    const text = response.text();

    if (!text) {
      throw new Error("No response from Google AI");
    }

    try {
      // Try to parse as JSON
      const jsonMatch = text.match(/```json\n([\s\S]*?)\n```/) || text.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const jsonResponse = JSON.parse(jsonMatch[0].replace(/```json\n/, '').replace(/\n```/, ''));
        return { explanation: jsonResponse.explanation || "" };
      } else {
        return { explanation: text };
      }
    } catch {
      return { explanation: text };
    }
  } catch (error) {
    console.error("Error explaining code:", error);
    throw error;
  }
}

export async function suggestImprovements(code: string): Promise<CodeSuggestion> {
  try {
    if (!API_KEY) {
      throw new Error("Google AI API key not configured");
    }

    // Get the model
    const model = genAI.getGenerativeModel({ model: MODEL_NAME });

    // Create prompt with context
    const prompt = `You are an expert code reviewer. Analyze the provided code and suggest up to 3 specific improvements.
    Format your response as JSON with 'suggestions' (array of code suggestions) and 'explanations' (array of explanations).
    
    Code to review:
    \`\`\`
    ${code}
    \`\`\`
    
    Respond with a JSON object containing two arrays: 'suggestions' and 'explanations'.`;

    // Generate content
    const result = await model.generateContent(prompt);
    const response = result.response;
    const text = response.text();

    if (!text) {
      throw new Error("No response from Google AI");
    }

    try {
      // Try to parse as JSON
      const jsonMatch = text.match(/```json\n([\s\S]*?)\n```/) || text.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const jsonResponse = JSON.parse(jsonMatch[0].replace(/```json\n/, '').replace(/\n```/, ''));
        return {
          suggestions: jsonResponse.suggestions || [],
          explanations: jsonResponse.explanations || []
        };
      } else {
        // Extract suggestions from text if not in JSON format
        return {
          suggestions: ["Could not parse suggestions"],
          explanations: [text]
        };
      }
    } catch {
      return {
        suggestions: ["Could not parse suggestions"],
        explanations: [text]
      };
    }
  } catch (error) {
    console.error("Error suggesting improvements:", error);
    throw error;
  }
}

export async function chatWithAI(messages: { role: string; content: string }[]): Promise<string> {
  try {
    if (!API_KEY) {
      throw new Error("Google AI API key not configured");
    }

    // Get the model
    const model = genAI.getGenerativeModel({ model: MODEL_NAME });

    // System message providing context
    const systemMessage = `You are a helpful AI coding assistant. You provide concise, accurate information about programming, 
    and can help with code examples, explanations, and best practices. When sharing code, format it using markdown 
    code blocks with the appropriate language syntax highlighting.`;

    // Combine messages into a single prompt
    let prompt = systemMessage + "\n\n";
    
    // Process conversation history
    messages.forEach(msg => {
      if (msg.role === "user") {
        prompt += `User: ${msg.content}\n\n`;
      } else if (msg.role === "assistant") {
        prompt += `Assistant: ${msg.content}\n\n`;
      }
    });
    
    // Add final instruction if the last message is from the user
    if (messages.length > 0 && messages[messages.length - 1].role === "user") {
      prompt += "Assistant: ";
    }

    // Generate content
    const result = await model.generateContent(prompt);
    const response = result.response;
    const text = response.text();

    if (!text) {
      return "I'm sorry, I couldn't generate a response.";
    }

    return text;
  } catch (error) {
    console.error("Error chatting with AI:", error);
    throw error;
  }
}
