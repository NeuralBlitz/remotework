import { createContext, useContext, useState, ReactNode, useEffect } from "react";
import { File } from "@shared/schema";
import { useFileSystem } from "./FileSystemContext";
import { useToast } from "@/hooks/use-toast";

// Context interface
interface EditorContextType {
  activeFileId: number | null;
  openFiles: File[];
  activeFile: File | null;
  setActiveFileId: (id: number | null) => void;
  openFile: (id: number) => Promise<void>;
  closeFile: (id: number) => void;
  saveFile: (id: number, content: string) => Promise<boolean>;
  updateContent: (id: number, content: string) => void;
  runCurrentFile: () => Promise<void>;
}

// Create context
const EditorContext = createContext<EditorContextType | undefined>(undefined);

// Provider component
export const EditorProvider = ({ children }: { children: ReactNode }) => {
  const [activeFileId, setActiveFileId] = useState<number | null>(null);
  const [openFiles, setOpenFiles] = useState<File[]>([]);
  const [fileContents, setFileContents] = useState<Record<number, string>>({});
  const { getFile, updateFile } = useFileSystem();
  const { toast } = useToast();

  // Get active file
  const activeFile = openFiles.find(file => file.id === activeFileId) || null;

  // Update content without saving
  const updateContent = (id: number, content: string) => {
    setFileContents(prev => ({
      ...prev,
      [id]: content
    }));
  };

  // Open a file
  const openFile = async (id: number) => {
    try {
      // Check if file is already open
      if (openFiles.some(file => file.id === id)) {
        setActiveFileId(id);
        return;
      }
      
      // Fetch file data
      const file = await getFile(id);
      
      // Don't open folders
      if (file.isFolder) {
        return;
      }
      
      // Add file to open files
      setOpenFiles(prev => [...prev, file]);
      
      // Set file content
      setFileContents(prev => ({
        ...prev,
        [id]: file.content
      }));
      
      // Set as active file
      setActiveFileId(id);
    } catch (err) {
      toast({
        title: "Error",
        description: "Failed to open file",
        variant: "destructive"
      });
    }
  };

  // Close a file
  const closeFile = (id: number) => {
    setOpenFiles(prev => prev.filter(file => file.id !== id));
    
    // If closing the active file, set active to the next available file
    if (activeFileId === id) {
      const remainingFiles = openFiles.filter(file => file.id !== id);
      setActiveFileId(remainingFiles.length > 0 ? remainingFiles[0].id : null);
    }
  };

  // Save a file
  const saveFile = async (id: number, content: string) => {
    try {
      const success = await updateFile(id, content);
      
      if (success) {
        // Update local file content
        setFileContents(prev => ({
          ...prev,
          [id]: content
        }));
        
        toast({
          title: "Success",
          description: "File saved successfully"
        });
      }
      
      return success;
    } catch (err) {
      return false;
    }
  };

  // Run current file
  const runCurrentFile = async () => {
    if (!activeFile) {
      toast({
        title: "Error",
        description: "No file is currently active",
        variant: "destructive"
      });
      return;
    }

    try {
      // Only allow running JavaScript files for now
      if (!activeFile.name.endsWith('.js')) {
        toast({
          title: "Error",
          description: "Only JavaScript files can be run at the moment",
          variant: "destructive"
        });
        return;
      }

      // Get current content (could be unsaved)
      const content = fileContents[activeFile.id] || activeFile.content;

      // Run the code
      const response = await fetch('/api/files/run', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: content,
          filename: activeFile.name
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to run file: ${response.statusText}`);
      }

      const result = await response.json();

      // Let the terminal context handle the output
      // This will be caught by the useEffect in the IDE component
      if (result.error) {
        document.dispatchEvent(new CustomEvent('terminal-output', { 
          detail: {
            command: `node ${activeFile.name}`,
            output: result.error,
            isError: true
          }
        }));
      } else {
        document.dispatchEvent(new CustomEvent('terminal-output', { 
          detail: {
            command: `node ${activeFile.name}`,
            output: result.output,
            isError: false
          }
        }));
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      toast({
        title: "Error",
        description: `Failed to run file: ${message}`,
        variant: "destructive"
      });
    }
  };

  return (
    <EditorContext.Provider
      value={{
        activeFileId,
        openFiles,
        activeFile,
        setActiveFileId,
        openFile,
        closeFile,
        saveFile,
        updateContent,
        runCurrentFile
      }}
    >
      {children}
    </EditorContext.Provider>
  );
};

// Custom hook to use the Editor context
export const useEditor = () => {
  const context = useContext(EditorContext);
  if (context === undefined) {
    throw new Error("useEditor must be used within an EditorProvider");
  }
  return context;
};
