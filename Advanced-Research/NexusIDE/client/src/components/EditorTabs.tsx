import { FC } from "react";
import { RiFileCodeLine, RiCloseLine } from "react-icons/ri";
import { cn } from "@/lib/utils";
import { File } from "@shared/schema";

interface EditorTabsProps {
  openFiles: File[];
  activeFileId?: number;
  onSelectTab: (fileId: number) => void;
  onCloseTab: (fileId: number) => void;
}

const EditorTabs: FC<EditorTabsProps> = ({
  openFiles,
  activeFileId,
  onSelectTab,
  onCloseTab
}) => {
  if (openFiles.length === 0) {
    return (
      <div className="border-b border-neutral-800 py-2 px-4 bg-neutral-900 text-neutral-400 italic">
        No files open
      </div>
    );
  }

  return (
    <div className="border-b border-neutral-800 flex overflow-x-auto">
      {openFiles.map((file) => (
        <div 
          key={file.id}
          className={cn(
            "flex items-center py-2 px-4 border-r border-neutral-800 cursor-pointer",
            activeFileId === file.id ? "bg-neutral-900" : "bg-neutral-950"
          )}
          onClick={() => onSelectTab(file.id)}
        >
          <RiFileCodeLine className={cn("mr-2", activeFileId === file.id ? "text-primary" : "text-neutral-400")} />
          <span>{file.name}</span>
          <button 
            className="ml-2 text-neutral-400 hover:text-neutral-100"
            onClick={(e) => {
              e.stopPropagation();
              onCloseTab(file.id);
            }}
          >
            <RiCloseLine />
          </button>
        </div>
      ))}
    </div>
  );
};

export default EditorTabs;
