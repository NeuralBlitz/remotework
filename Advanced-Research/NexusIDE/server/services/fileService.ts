import { exec } from 'child_process';
import path from 'path';
import { promisify } from 'util';
import fs from 'fs/promises';
import { storage } from '../storage';
import { File, InsertFile } from '@shared/schema';

const execAsync = promisify(exec);

export interface ExecutionResult {
  output: string;
  error?: string;
}

export async function runJavaScript(code: string, filename: string): Promise<ExecutionResult> {
  try {
    // Create a temporary directory to run the code
    const tempDir = path.resolve(process.cwd(), 'temp');
    const tempFile = path.join(tempDir, filename);
    
    // Ensure temp directory exists
    try {
      await fs.mkdir(tempDir, { recursive: true });
    } catch (err) {
      console.log('Temp directory already exists');
    }
    
    // Write the code to a temporary file
    await fs.writeFile(tempFile, code);
    
    // Execute the code
    try {
      const { stdout, stderr } = await execAsync(`node ${tempFile}`, { 
        timeout: 5000,  // 5 second timeout
        maxBuffer: 1024 * 1024  // 1MB buffer
      });
      
      return {
        output: stdout,
        error: stderr || undefined
      };
    } catch (error) {
      return {
        output: '',
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      };
    } finally {
      // Clean up temp file
      try {
        await fs.unlink(tempFile);
      } catch (err) {
        console.error('Failed to delete temp file:', err);
      }
    }
  } catch (error) {
    console.error('Error running JavaScript code:', error);
    return {
      output: '',
      error: `Failed to execute code: ${error instanceof Error ? error.message : 'Unknown error'}`
    };
  }
}

export async function runCommand(command: string): Promise<ExecutionResult> {
  try {
    // Only allow safe commands
    const safeCommands = ['node', 'npm', 'ls', 'echo', 'cat', 'pwd'];
    const commandName = command.split(' ')[0];
    
    if (!safeCommands.includes(commandName)) {
      return {
        output: '',
        error: `Command not allowed: ${commandName}. Only the following commands are supported: ${safeCommands.join(', ')}`
      };
    }
    
    // Execute with limited permissions
    const { stdout, stderr } = await execAsync(command, { 
      timeout: 5000,  // 5 second timeout
      maxBuffer: 1024 * 1024  // 1MB buffer
    });
    
    return {
      output: stdout,
      error: stderr || undefined
    };
  } catch (error) {
    return {
      output: '',
      error: error instanceof Error ? error.message : 'Unknown error occurred'
    };
  }
}

export async function createProjectStructure(userId: number, projectName: string): Promise<boolean> {
  try {
    // Create root project folder
    const rootFolder: InsertFile = {
      userId,
      name: projectName,
      path: `/${projectName}`,
      isFolder: true,
      content: '',
      parentId: null
    };
    
    const root = await storage.createFile(rootFolder);
    
    // Create src folder
    const srcFolder: InsertFile = {
      userId,
      name: 'src',
      path: `/${projectName}/src`,
      isFolder: true,
      content: '',
      parentId: root.id
    };
    
    const src = await storage.createFile(srcFolder);
    
    // Create index.js file
    const indexFile: InsertFile = {
      userId,
      name: 'index.js',
      path: `/${projectName}/src/index.js`,
      isFolder: false,
      content: '// Your code here\nconsole.log("Hello, World!");\n',
      parentId: src.id
    };
    
    await storage.createFile(indexFile);
    
    // Create package.json
    const packageJson: InsertFile = {
      userId,
      name: 'package.json',
      path: `/${projectName}/package.json`,
      isFolder: false,
      content: `{
  "name": "${projectName}",
  "version": "1.0.0",
  "description": "A new project",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js"
  }
}`,
      parentId: root.id
    };
    
    await storage.createFile(packageJson);
    
    // Create README.md
    const readme: InsertFile = {
      userId,
      name: 'README.md',
      path: `/${projectName}/README.md`,
      isFolder: false,
      content: `# ${projectName}\n\nA new project created with CodeAI IDE.\n`,
      parentId: root.id
    };
    
    await storage.createFile(readme);
    
    return true;
  } catch (error) {
    console.error('Error creating project structure:', error);
    return false;
  }
}
