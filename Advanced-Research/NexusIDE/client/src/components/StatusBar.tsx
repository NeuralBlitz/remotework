import { FC } from "react";
import { RiGitBranchLine } from "react-icons/ri";
import { cn } from "@/lib/utils";

interface StatusBarProps {
  language?: string;
  position?: {
    line: number;
    column: number;
  };
  encoding?: string;
  connected?: boolean;
  branch?: string;
}

const StatusBar: FC<StatusBarProps> = ({
  language = "",
  position = { line: 1, column: 1 },
  encoding = "UTF-8",
  connected = true,
  branch = "main"
}) => {
  return (
    <footer className="bg-neutral-950 text-neutral-400 py-1 px-4 border-t border-neutral-800 text-xs flex justify-between">
      <div className="flex items-center space-x-4">
        <div className="flex items-center">
          <RiGitBranchLine className="mr-1" />
          <span>{branch}</span>
        </div>
        <div>
          <span className={cn(
            "inline-block w-2 h-2 rounded-full mr-1",
            connected ? "bg-green-500" : "bg-red-500"
          )}></span>
          <span>{connected ? "Connected" : "Disconnected"}</span>
        </div>
      </div>
      <div className="flex items-center space-x-4">
        {language && <div>{language}</div>}
        <div>Ln {position.line}, Col {position.column}</div>
        <div>{encoding}</div>
      </div>
    </footer>
  );
};

export default StatusBar;
