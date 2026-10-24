import { useState, useEffect } from "react";
import AppHeader from "@/components/AppHeader";
import FileExplorer from "@/components/FileExplorer";
import EditorTabs from "@/components/EditorTabs";
import CodeEditor from "@/components/CodeEditor";
import AccessoryBar from "@/components/AccessoryBar";
import Terminal from "@/components/Terminal";
import AIAssistant from "@/components/AIAssistant";
import StatusBar from "@/components/StatusBar";
import { useFileSystem } from "@/contexts/FileSystemContext";
import { useEditor } from "@/contexts/EditorContext";
import { useTerminal } from "@/contexts/TerminalContext";
import { useAI } from "@/contexts/AIContext";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { createFilePath } from "@/lib/fileSystem";
import { useToast } from "@/hooks/use-toast";
import { Loader2 } from "lucide-react";

export default function IDE() {
  const { files, loading: filesLoading, refreshFiles } = useFileSystem();
  const { 
    activeFileId, activeFile, openFiles, 
    openFile, closeFile, setActiveFileId, 
    updateContent, saveFile, runCurrentFile 
  } = useEditor();
  const { 
    output, command, isLoading: terminalLoading,
    setCommand, runCommand 
  } = useTerminal();
  const { messages, isLoading: aiLoading, sendMessage, clearChat } = useAI();
  const { toast } = useToast();

  // State for new file/folder dialog
  const [showNewFileDialog, setShowNewFileDialog] = useState(false);
  const [isFolder, setIsFolder] = useState(false);
  const [fileName, setFileName] = useState("");
  const [selectedParentId, setSelectedParentId] = useState<number | null>(null);

  // Cursor position in editor
  const [cursorPosition, setCursorPosition] = useState({ line: 1, column: 1 });
  
  // Get language for status bar
  const getLanguage = () => {
    if (!activeFile) return "";
    const extension = activeFile.name.split('.').pop()?.toLowerCase() || "";
    
    const languages: Record<string, string> = {
      js: "JavaScript",
      jsx: "JavaScript (JSX)",
      ts: "TypeScript",
      tsx: "TypeScript (TSX)",
      py: "Python",
      html: "HTML",
      css: "CSS",
      json: "JSON",
      md: "Markdown"
    };
    
    return languages[extension] || extension.toUpperCase();
  };

  // Handle new file/folder
  const handleNewFile = () => {
    setIsFolder(false);
    setFileName("");
    setSelectedParentId(null);
    setShowNewFileDialog(true);
  };

  const handleNewFolder = () => {
    setIsFolder(true);
    setFileName("");
    setSelectedParentId(null);
    setShowNewFileDialog(true);
  };

  // Create new file/folder
  const createNewFile = async () => {
    if (!fileName.trim()) {
      toast({
        title: "Error",
        description: "Name cannot be empty",
        variant: "destructive"
      });
      return;
    }
    
    // Find parent node if selected
    let parentNode = null;
    let parentPath = "";
    
    if (selectedParentId) {
      // Find the parent node in the file tree
      files.forEach(rootNode => {
        const findNode = (node: any) => {
          if (node.id === selectedParentId) {
            parentNode = node;
            return true;
          }
          if (node.children) {
            return node.children.some(findNode);
          }
          return false;
        };
        findNode(rootNode);
      });
      
      if (parentNode) {
        parentPath = (parentNode as any).path;
      }
    } else {
      // Default to first root folder
      const rootFolder = files.find(f => f.isFolder);
      if (rootFolder) {
        parentNode = rootFolder;
        parentPath = rootFolder.path;
        setSelectedParentId(rootFolder.id);
      }
    }
    
    if (!parentNode) {
      toast({
        title: "Error",
        description: "Could not find parent folder",
        variant: "destructive"
      });
      return;
    }
    
    // Create file path
    const path = createFilePath(parentPath, fileName);
    
    // Create file or folder
    const result = await useFileSystem().createFile(
      fileName,
      path,
      isFolder,
      selectedParentId
    );
    
    if (result) {
      setShowNewFileDialog(false);
      refreshFiles();
    }
  };

  // File content change handler
  const handleCodeChange = (newCode: string) => {
    if (activeFileId) {
      updateContent(activeFileId, newCode);
    }
  };

  // Save file keyboard shortcut
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Cmd/Ctrl + S to save
      if ((event.metaKey || event.ctrlKey) && event.key === 's') {
        event.preventDefault();
        if (activeFileId && activeFile) {
          const content = openFiles.find(f => f.id === activeFileId)?.content || "";
          saveFile(activeFileId, content);
        }
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [activeFileId, activeFile, openFiles]);

  return (
    <div className="bg-neutral-900 text-white font-sans h-screen flex flex-col overflow-hidden">
      <AppHeader />
      
      <div className="flex-1 flex flex-col md:flex-row overflow-hidden">
        {/* File Explorer */}
        <FileExplorer
          files={files}
          activeFileId={activeFileId || undefined}
          onSelectFile={(file) => {
            if (!file.isFolder) {
              openFile(file.id);
            }
          }}
          onNewFile={handleNewFile}
          onNewFolder={handleNewFolder}
          onRefresh={refreshFiles}
        />
        
        {/* Editor Area */}
        <div className="flex-1 flex flex-col overflow-hidden bg-neutral-800">
          {/* Editor Tabs */}
          <EditorTabs
            openFiles={openFiles}
            activeFileId={activeFileId || undefined}
            onSelectTab={setActiveFileId}
            onCloseTab={closeFile}
          />
          
          {/* Code Editor */}
          {activeFile ? (
            <div className="flex-1 flex flex-col overflow-hidden relative">
              <CodeEditor
                code={activeFile.content || ""}
                language={activeFile.name}
                onChange={handleCodeChange}
              />
              <AccessoryBar 
                onInsert={(text) => {
                  const editor = (window as any).monacoEditor;
                  if (editor) {
                    const selection = editor.getSelection();
                    const id = { major: 1, minor: 1 };
                    const op = {
                      identifier: id,
                      range: selection,
                      text: text,
                      forceMoveMarkers: true
                    };
                    editor.executeEdits("accessory-bar", [op]);
                    editor.focus();
                    
                    // Auto-closing brackets
                    const pairs: Record<string, string> = {
                      '{': '}',
                      '(': ')',
                      '[': ']',
                      '"': '"',
                      "'": "'"
                    };
                    
                    if (pairs[text]) {
                      const pos = editor.getPosition();
                      const closeOp = {
                        identifier: id,
                        range: new (window as any).monaco.Range(pos.lineNumber, pos.column, pos.lineNumber, pos.column),
                        text: pairs[text],
                        forceMoveMarkers: true
                      };
                      editor.executeEdits("auto-close", [closeOp]);
                      editor.setPosition(pos); // Keep cursor between brackets
                    }
                  } else {
                    handleCodeChange((activeFile.content || "") + text);
                  }
                }} 
              />
            </div>
          ) : (
            <div className="flex-1 flex items-center justify-center bg-neutral-800 text-neutral-400">
              <div className="text-center">
                <p className="mb-2">No file open</p>
                <p className="text-sm">Select a file from the explorer to start editing</p>
              </div>
            </div>
          )}
          
          {/* Terminal */}
          <Terminal
            output={output}
            command={command}
            onCommandChange={setCommand}
            onRunCommand={runCommand}
            onRunFile={activeFile ? runCurrentFile : undefined}
          />
        </div>
        
        {/* AI Assistant */}
        <AIAssistant
          messages={messages}
          onSendMessage={sendMessage}
          onClearChat={clearChat}
          isLoading={aiLoading}
        />
      </div>
      
      {/* Status Bar */}
      <StatusBar
        language={getLanguage()}
        position={cursorPosition}
        connected={true}
      />
      
      {/* New File/Folder Dialog */}
      <Dialog open={showNewFileDialog} onOpenChange={setShowNewFileDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Create New {isFolder ? 'Folder' : 'File'}</DialogTitle>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="name" className="text-right">
                Name
              </Label>
              <Input
                id="name"
                value={fileName}
                onChange={(e) => setFileName(e.target.value)}
                className="col-span-3"
                placeholder={isFolder ? "folder-name" : "file-name.js"}
                autoFocus
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowNewFileDialog(false)}>
              Cancel
            </Button>
            <Button onClick={createNewFile}>
              Create
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
      
      {/* Loading Overlay */}
      {filesLoading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-neutral-800 p-6 rounded-lg flex items-center space-x-4">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
            <p>Loading IDE...</p>
          </div>
        </div>
      )}
    </div>
  );
}
