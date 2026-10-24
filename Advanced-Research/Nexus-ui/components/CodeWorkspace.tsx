import React, { useState, useEffect } from 'react';
import { Code, Eye, Monitor, Save, Share2 } from 'lucide-react';
import { logger } from '../services/logger';
import { LogLevel } from '../types';

interface CodeWorkspaceProps {
  code: string;
  onCodeChange: (code: string) => void;
}

export const CodeWorkspace: React.FC<CodeWorkspaceProps> = ({ code, onCodeChange }) => {
  const [activeTab, setActiveTab] = useState<'editor' | 'preview'>('editor');
  const [lastSaved, setLastSaved] = useState<Date | null>(null);

  // We save/log on active changes debounced slightly in a real app, 
  // but here we just log when user actively modifies via typing if we wanted.
  // For now, we log major updates.

  useEffect(() => {
    // Auto-update log when code arrives from AI
    if (code) {
        logger.log('Code workspace updated with new content', LogLevel.INFO, 'DEV_TOOLS');
        setLastSaved(new Date());
    }
  }, [code]);

  return (
    <div className="flex flex-col h-full bg-slate-900 border border-slate-800 rounded-lg shadow-2xl overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-slate-800 bg-slate-900/50">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-indigo-400">
            <Code size={18} />
            <span className="font-semibold tracking-wider text-xs uppercase">Dev Workspace</span>
          </div>
          <div className="flex bg-slate-800 rounded-lg p-1">
            <button
              onClick={() => setActiveTab('editor')}
              className={`px-3 py-1 rounded text-xs font-medium transition-all ${
                activeTab === 'editor' ? 'bg-indigo-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'
              }`}
            >
              Code
            </button>
            <button
              onClick={() => setActiveTab('preview')}
              className={`px-3 py-1 rounded text-xs font-medium transition-all ${
                activeTab === 'preview' ? 'bg-emerald-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'
              }`}
            >
              Preview
            </button>
          </div>
        </div>
        <div className="flex items-center gap-2 text-xs text-slate-500">
          {lastSaved && <span>Updated: {lastSaved.toLocaleTimeString()}</span>}
          <Monitor size={14} />
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 relative">
        {/* Editor */}
        <div className={`absolute inset-0 transition-opacity duration-300 ${activeTab === 'editor' ? 'opacity-100 z-10' : 'opacity-0 z-0'}`}>
          <textarea
            value={code}
            onChange={(e) => onCodeChange(e.target.value)}
            className="w-full h-full bg-slate-950 text-slate-200 font-mono text-sm p-4 outline-none resize-none"
            spellCheck={false}
            placeholder="<!-- HTML/CSS/JS code goes here -->"
          />
        </div>

        {/* Preview */}
        <div className={`absolute inset-0 bg-white transition-opacity duration-300 ${activeTab === 'preview' ? 'opacity-100 z-10' : 'opacity-0 z-0'}`}>
           <iframe
             title="Preview"
             srcDoc={code}
             className="w-full h-full border-none"
             sandbox="allow-scripts"
           />
        </div>
      </div>
      
      {/* Footer */}
      <div className="bg-slate-950 border-t border-slate-800 px-4 py-1 flex justify-between items-center text-[10px] text-slate-500">
        <span>index.html</span>
        <span>UTF-8</span>
      </div>
    </div>
  );
};
