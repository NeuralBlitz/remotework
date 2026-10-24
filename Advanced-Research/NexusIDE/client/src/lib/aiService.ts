import { apiRequest } from "./queryClient";

// Interface for code generation
export interface CodeCompletionResult {
  code: string;
  explanation?: string;
}

// Interface for code explanation
export interface CodeExplanationResult {
  explanation: string;
}

// Interface for code suggestions
export interface CodeSuggestionResult {
  suggestions: string[];
  explanations: string[];
}

// Generate code completion from prompt
export async function generateCodeCompletion(
  prompt: string,
  code?: string
): Promise<CodeCompletionResult> {
  const response = await apiRequest("POST", "/api/ai/generate", {
    prompt,
    code
  });
  
  return await response.json();
}

// Get explanation of code
export async function explainCode(code: string): Promise<CodeExplanationResult> {
  const response = await apiRequest("POST", "/api/ai/explain", {
    code
  });
  
  return await response.json();
}

// Get suggestions for improving code
export async function suggestImprovements(code: string): Promise<CodeSuggestionResult> {
  const response = await apiRequest("POST", "/api/ai/suggest", {
    code
  });
  
  return await response.json();
}

// Function to handle code highlighting in markdown
export function formatCodeBlocks(text: string): string {
  // Replace Markdown code blocks with HTML
  return text.replace(
    /```(\w+)?\n([\s\S]+?)```/g,
    (_, lang, code) => {
      const language = lang || 'plaintext';
      return `<pre class="language-${language}"><code>${escapeHtml(code)}</code></pre>`;
    }
  );
}

// Helper function to escape HTML
function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
