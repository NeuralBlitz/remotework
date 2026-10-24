import React, { useState } from 'react';
import { X, Box, Type, FileText, Layers, Activity } from 'lucide-react';
import { Project, ProjectStatus } from '../types';

interface NewProjectModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreate: (project: Omit<Project, 'id' | 'lastActive' | 'cpu' | 'memory' | 'port'>) => void;
}

export const NewProjectModal: React.FC<NewProjectModalProps> = ({ isOpen, onClose, onCreate }) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [framework, setFramework] = useState<Project['framework']>('react');
  const [status, setStatus] = useState<ProjectStatus>('offline');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onCreate({
      name,
      description,
      framework,
      status
    });
    // Reset and close
    setName('');
    setDescription('');
    setFramework('react');
    setStatus('offline');
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-xl shadow-2xl p-6 relative animate-in zoom-in-95 duration-200">
        <button 
          onClick={onClose}
          className="absolute right-4 top-4 text-slate-500 hover:text-white transition-colors"
        >
          <X size={20} />
        </button>
        
        <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
          <Box className="text-indigo-500" />
          Create New Project
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1">
            <label className="text-xs font-semibold text-slate-400 uppercase flex items-center gap-1">
              <Type size={12} /> Project Name
            </label>
            <input 
              type="text" 
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500 transition-colors"
              placeholder="e.g. Neural Network Viz"
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-semibold text-slate-400 uppercase flex items-center gap-1">
              <FileText size={12} /> Description
            </label>
            <textarea 
              required
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500 transition-colors resize-none h-24"
              placeholder="Brief description of the project..."
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-400 uppercase flex items-center gap-1">
                <Layers size={12} /> Framework
              </label>
              <select 
                value={framework}
                onChange={(e) => setFramework(e.target.value as any)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500 transition-colors appearance-none"
              >
                <option value="react">React</option>
                <option value="node">Node.js</option>
                <option value="python">Python</option>
                <option value="html">HTML/Static</option>
              </select>
            </div>
            
             <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-400 uppercase flex items-center gap-1">
                <Activity size={12} /> Initial Status
              </label>
              <select 
                value={status}
                onChange={(e) => setStatus(e.target.value as any)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500 transition-colors appearance-none"
              >
                <option value="offline">Offline</option>
                <option value="online">Online</option>
                <option value="building">Building</option>
              </select>
            </div>
          </div>

          <div className="pt-4 flex gap-3">
            <button 
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-sm font-semibold transition-colors"
            >
              Cancel
            </button>
            <button 
              type="submit"
              className="flex-1 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-semibold transition-colors shadow-lg shadow-indigo-500/20"
            >
              Create Project
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
