import { FC } from "react";
import { RiFileAddLine, RiFolderAddLine, RiRefreshLine, RiFolderOpenLine, RiFolderLine, RiFileCodeLine, RiFileTextLine } from "react-icons/ri";
import { cn } from "@/lib/utils";
import { FileNode } from "@shared/schema";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

interface FileExplorerProps {
  files: FileNode[];
  activeFileId?: number;
  onSelectFile: (file: FileNode) => void;
  onNewFile: () => void;
  onNewFolder: () => void;
  onRefresh: () => void;
}

const FileExplorer: FC<FileExplorerProps> = ({
  files,
  activeFileId,
  onSelectFile,
  onNewFile,
  onNewFolder,
  onRefresh
}) => {
  // Recursive function to render file tree
  const renderFileTree = (nodes: FileNode[], depth = 0) => {
    return nodes.map((node) => (
      <div key={node.id} className="mb-1" style={{ paddingLeft: `${depth * 12}px` }}>
        <div 
          className={cn(
            "flex items-center px-2 py-1 hover:bg-neutral-800 rounded cursor-pointer",
            activeFileId === node.id && "bg-neutral-800"
          )}
          onClick={() => onSelectFile(node)}
        >
          {node.isFolder ? (
            <RiFolderOpenLine className="text-neutral-400 mr-2" />
          ) : node.name.endsWith('.js') || node.name.endsWith('.jsx') || node.name.endsWith('.ts') || node.name.endsWith('.tsx') ? (
            <RiFileCodeLine className={cn("mr-2", activeFileId === node.id ? "text-primary" : "text-neutral-400")} />
          ) : (
            <RiFileTextLine className={cn("mr-2", activeFileId === node.id ? "text-primary" : "text-neutral-400")} />
          )}
          <span className={activeFileId === node.id ? "font-medium" : ""}>{node.name}</span>
        </div>
        
        {node.isFolder && node.children && (
          <div className="pl-4">
            {renderFileTree(node.children, depth + 1)}
          </div>
        )}
      </div>
    ));
  };

  return (
    <div className="w-full md:w-64 bg-neutral-900 border-r border-neutral-800 flex flex-col h-full">
      {/* Explorer header */}
      <div className="px-4 py-3 border-b border-neutral-800 flex justify-between items-center">
        <h2 className="font-medium">Explorer</h2>
        <div className="flex space-x-2">
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <button 
                  className="text-neutral-400 hover:text-neutral-100 transition-colors"
                  onClick={onNewFile}
                >
                  <RiFileAddLine />
                </button>
              </TooltipTrigger>
              <TooltipContent>
                <p>New File</p>
              </TooltipContent>
            </Tooltip>

            <Tooltip>
              <TooltipTrigger asChild>
                <button 
                  className="text-neutral-400 hover:text-neutral-100 transition-colors"
                  onClick={onNewFolder}
                >
                  <RiFolderAddLine />
                </button>
              </TooltipTrigger>
              <TooltipContent>
                <p>New Folder</p>
              </TooltipContent>
            </Tooltip>

            <Tooltip>
              <TooltipTrigger asChild>
                <button 
                  className="text-neutral-400 hover:text-neutral-100 transition-colors"
                  onClick={onRefresh}
                >
                  <RiRefreshLine />
                </button>
              </TooltipTrigger>
              <TooltipContent>
                <p>Refresh</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        </div>
      </div>
      
      {/* File tree */}
      <div className="overflow-y-auto flex-1 py-2">
        <div className="px-2">
          {renderFileTree(files)}
        </div>
      </div>
    </div>
  );
};

export default FileExplorer;
