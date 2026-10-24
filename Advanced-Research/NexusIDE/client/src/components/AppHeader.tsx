import { FC } from "react";
import { RiCodeBoxLine, RiSettings3Line } from "react-icons/ri";

interface AppHeaderProps {
  title?: string;
  user?: {
    name: string;
    initials: string;
  };
}

const AppHeader: FC<AppHeaderProps> = ({ 
  title = "CodeAI IDE",
  user = { name: "Guest User", initials: "GU" }
}) => {
  return (
    <header className="bg-dark-300 border-b border-neutral-800 px-4 py-2 flex items-center justify-between">
      <div className="flex items-center">
        <RiCodeBoxLine className="text-primary text-2xl mr-2" />
        <h1 className="text-xl font-semibold">{title}</h1>
      </div>
      <div className="flex items-center space-x-4">
        <button className="text-neutral-400 hover:text-neutral-100 transition-colors">
          <RiSettings3Line size={20} />
        </button>
        <div className="flex items-center">
          <span className="text-sm mr-2">{user.name}</span>
          <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-white">
            <span>{user.initials}</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default AppHeader;
