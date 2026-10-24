import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { FileNode } from "@shared/schema";
import { apiRequest } from "@/lib/queryClient";
import { useToast } from "@/hooks/use-toast";

// Context interface
interface FileSystemContextType {
  files: FileNode[];
  loading: boolean;
  error: string | null;
  refreshFiles: () => Promise<void>;
  createFile: (name: string, path: string, isFolder: boolean, parentId: number | null) => Promise<boolean>;
  updateFile: (id: number, content: string) => Promise<boolean>;
  deleteFile: (id: number) => Promise<boolean>;
  getFile: (id: number) => Promise<any>;
}

// Create context
const FileSystemContext = createContext<FileSystemContextType | undefined>(undefined);

// Provider component
export const FileSystemProvider = ({ children }: { children: ReactNode }) => {
  const [files, setFiles] = useState<FileNode[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  // Mock user ID for demo - in a real app, this would come from auth
  const userId = 1;

  // Fetch files on mount
  useEffect(() => {
    refreshFiles();
  }, []);

  // Refresh files
  const refreshFiles = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/files?userId=${userId}`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch files: ${response.statusText}`);
      }
      
      const data = await response.json();
      setFiles(data);
      setError(null);
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      setError(`Error loading files: ${message}`);
      toast({
        title: "Error",
        description: `Failed to load files: ${message}`,
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  // Create file
  const createFile = async (name: string, path: string, isFolder: boolean, parentId: number | null) => {
    try {
      const response = await apiRequest("POST", "/api/files", {
        userId,
        name,
        path,
        isFolder,
        content: isFolder ? "" : "// Add your code here",
        parentId
      });
      
      if (!response.ok) {
        throw new Error(`Failed to create file: ${response.statusText}`);
      }
      
      await refreshFiles();
      toast({
        title: "Success",
        description: `${isFolder ? "Folder" : "File"} created successfully`,
      });
      return true;
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      toast({
        title: "Error",
        description: `Failed to create ${isFolder ? "folder" : "file"}: ${message}`,
        variant: "destructive"
      });
      return false;
    }
  };

  // Update file
  const updateFile = async (id: number, content: string) => {
    try {
      const response = await apiRequest("PUT", `/api/files/${id}`, { content });
      
      if (!response.ok) {
        throw new Error(`Failed to update file: ${response.statusText}`);
      }
      
      return true;
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      toast({
        title: "Error",
        description: `Failed to save file: ${message}`,
        variant: "destructive"
      });
      return false;
    }
  };

  // Delete file
  const deleteFile = async (id: number) => {
    try {
      const response = await apiRequest("DELETE", `/api/files/${id}`);
      
      if (!response.ok) {
        throw new Error(`Failed to delete file: ${response.statusText}`);
      }
      
      await refreshFiles();
      toast({
        title: "Success",
        description: "File deleted successfully",
      });
      return true;
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      toast({
        title: "Error",
        description: `Failed to delete file: ${message}`,
        variant: "destructive"
      });
      return false;
    }
  };

  // Get file
  const getFile = async (id: number) => {
    try {
      const response = await fetch(`/api/files/${id}`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch file: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      toast({
        title: "Error",
        description: `Failed to load file: ${message}`,
        variant: "destructive"
      });
      throw err;
    }
  };

  return (
    <FileSystemContext.Provider
      value={{
        files,
        loading,
        error,
        refreshFiles,
        createFile,
        updateFile,
        deleteFile,
        getFile
      }}
    >
      {children}
    </FileSystemContext.Provider>
  );
};

// Custom hook to use the FileSystem context
export const useFileSystem = () => {
  const context = useContext(FileSystemContext);
  if (context === undefined) {
    throw new Error("useFileSystem must be used within a FileSystemProvider");
  }
  return context;
};
