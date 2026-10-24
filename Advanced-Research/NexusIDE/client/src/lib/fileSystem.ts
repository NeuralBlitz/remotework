import { FileNode } from "@shared/schema";

// Create a new file or folder path by joining with parent
export function createFilePath(parentPath: string, name: string): string {
  return `${parentPath === '/' ? '' : parentPath}/${name}`;
}

// Get file extension
export function getFileExtension(filename: string): string {
  return filename.slice(((filename.lastIndexOf(".") - 1) >>> 0) + 2);
}

// Check if file is a code file
export function isCodeFile(filename: string): boolean {
  const codeExtensions = ['js', 'jsx', 'ts', 'tsx', 'py', 'java', 'c', 'cpp', 'cs', 'go', 'rb', 'php', 'html', 'css', 'json'];
  const ext = getFileExtension(filename);
  return codeExtensions.includes(ext);
}

// Find a node in the file tree by ID
export function findNodeById(tree: FileNode[], id: number): FileNode | null {
  for (const node of tree) {
    if (node.id === id) {
      return node;
    }
    
    if (node.isFolder && node.children && node.children.length > 0) {
      const found = findNodeById(node.children, id);
      if (found) {
        return found;
      }
    }
  }
  
  return null;
}

// Find a node by path
export function findNodeByPath(tree: FileNode[], path: string): FileNode | null {
  for (const node of tree) {
    if (node.path === path) {
      return node;
    }
    
    if (node.isFolder && node.children && node.children.length > 0) {
      const found = findNodeByPath(node.children, path);
      if (found) {
        return found;
      }
    }
  }
  
  return null;
}

// Get parent node by child ID
export function findParentNode(tree: FileNode[], childId: number): FileNode | null {
  for (const node of tree) {
    if (node.isFolder && node.children) {
      for (const child of node.children) {
        if (child.id === childId) {
          return node;
        }
      }
      
      const found = findParentNode(node.children, childId);
      if (found) {
        return found;
      }
    }
  }
  
  return null;
}

// Get file icon based on file type
export function getFileIcon(filename: string): string {
  const ext = getFileExtension(filename).toLowerCase();
  
  const iconMap: Record<string, string> = {
    js: 'javascript',
    jsx: 'react',
    ts: 'typescript',
    tsx: 'react-ts',
    py: 'python',
    java: 'java',
    html: 'html',
    css: 'css',
    json: 'json',
    md: 'markdown'
  };
  
  return iconMap[ext] || 'file';
}
