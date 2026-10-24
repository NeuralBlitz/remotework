import React, { useState, useEffect, useRef } from 'react';
import { 
  ArrowLeft, 
  Terminal, 
  Cpu, 
  Activity, 
  Clock, 
  Server, 
  PlayCircle, 
  AlertCircle, 
  CheckCircle,
  GitCommit,
  HardDrive,
  Network,
  Box,
  Loader2,
  GitBranch,
  User,
  Calendar,
  Copy,
  Check,
  ChevronDown,
  Key,
  Plus,
  Trash2,
  X,
  Archive,
  ArrowUpCircle,
  Eye,
  FileText,
  AlertTriangle,
  Shield,
  FileCode,
  GitPullRequest,
  List,
  Maximize2
} from 'lucide-react';
import { Project, ProjectStatus } from '../types';

interface ProjectDetailsProps {
  project: Project;
  onBack: () => void;
  onOpenWorkspace: () => void;
}

export const ProjectDetails: React.FC<ProjectDetailsProps> = ({ project, onBack, onOpenWorkspace }) => {
  const [isCopied, setIsCopied] = useState(false);
  const [currentBranch, setCurrentBranch] = useState(project.framework === 'node' ? 'main' : 'master');
  const [showBranchMenu, setShowBranchMenu] = useState(false);
  const [projectStatus, setProjectStatus] = useState<ProjectStatus>(project.status);
  
  // Deploy Confirmation & Logs State
  const [showDeployConfirm, setShowDeployConfirm] = useState(false);
  const [buildLogs, setBuildLogs] = useState<string[]>([]);
  const [showBuildLogs, setShowBuildLogs] = useState(false);
  const logsEndRef = useRef<HTMLDivElement>(null);

  // SSH Key State
  const [sshKeys, setSSHKeys] = useState([
    { id: '1', name: 'MacBook Pro (Personal)', fingerprint: 'SHA256:e9...4a', created: '2d ago', expiry: 'Never' },
    { id: '2', name: 'CI/CD Pipeline', fingerprint: 'SHA256:7f...9b', created: '5d ago', expiry: '30 days' },
  ]);
  const [isKeyModalOpen, setIsKeyModalOpen] = useState(false);
  const [newKeyName, setNewKeyName] = useState('');
  const [newKeyExpiry, setNewKeyExpiry] = useState('90');
  const [viewKey, setViewKey] = useState<{name: string, content: string} | null>(null);

  // Git State
  const [commitMessage, setCommitMessage] = useState('');
  const [commits, setCommits] = useState([
    { hash: '8f3a29b', msg: 'Update configuration for production', author: 'Nexus Admin', time: '2h ago' },
    { hash: '7e2c18a', msg: 'Fix login bug in auth service', author: 'Nexus Admin', time: '5h ago' },
    { hash: '4b1d90c', msg: 'Initial project setup', author: 'System', time: '1d ago' },
  ]);
  const [stashStack, setStashStack] = useState<string[]>([]);
  
  // Advanced Git Features State
  const [showBranchRules, setShowBranchRules] = useState(false);
  const [branchRules, setBranchRules] = useState({
      requirePullRequest: true,
      requireStatusChecks: true,
      requireLinearHistory: false,
      includeAdmins: false
  });
  const [viewCommitDiff, setViewCommitDiff] = useState<any>(null);
  const [showBlame, setShowBlame] = useState(false);

  // Activity Log State
  const [activityLogs, setActivityLogs] = useState([
    { id: 1, type: 'success', msg: 'Build completed successfully (v2.4.1)', time: '2 mins ago' },
    { id: 2, type: 'info', msg: 'Deploying to region us-east-1', time: '2 mins ago' },
    { id: 3, type: 'info', msg: 'Starting build process...', time: '3 mins ago' },
    { id: 4, type: 'warning', msg: 'High memory usage detected during compilation', time: '1 hour ago' },
    { id: 5, type: 'success', msg: 'Automated tests passed (42/42)', time: '3 hours ago' },
  ]);

  const availableBranches = ['main', 'develop', 'feature/auth-flow', 'fix/api-latency', 'release/v2.4.0'];

  // Scroll to bottom of build logs
  useEffect(() => {
      if (logsEndRef.current && showBuildLogs) {
          logsEndRef.current.scrollIntoView({ behavior: 'smooth' });
      }
  }, [buildLogs, showBuildLogs]);

  const getStatusColor = (status: ProjectStatus) => {
    switch (status) {
      case 'online': return 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20';
      case 'building': return 'text-amber-400 bg-amber-400/10 border-amber-400/20';
      case 'error': return 'text-red-400 bg-red-400/10 border-red-400/20';
      default: return 'text-slate-400 bg-slate-400/10 border-slate-400/20';
    }
  };

  const getFrameworkColor = (fw: string) => {
    switch (fw) {
      case 'react': return 'text-cyan-400 bg-cyan-950/50 border-cyan-500/30';
      case 'node': return 'text-green-400 bg-green-950/50 border-green-500/30';
      case 'python': return 'text-yellow-400 bg-yellow-950/50 border-yellow-500/30';
      default: return 'text-orange-400 bg-orange-950/50 border-orange-500/30';
    }
  };

  const repoUrl = `git@nexus.ai:projects/${project.name.toLowerCase().replace(/\s+/g, '-')}.git`;

  const copyToClipboard = () => {
    navigator.clipboard.writeText(`git clone ${repoUrl}`);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  const createSSHKey = () => {
    if (!newKeyName.trim()) return;
    
    let expiryLabel = 'Never';
    if (newKeyExpiry !== 'never') {
        const date = new Date();
        date.setDate(date.getDate() + parseInt(newKeyExpiry));
        expiryLabel = date.toLocaleDateString();
    }

    const newKey = {
        id: Math.random().toString(36).substring(7),
        name: newKeyName,
        fingerprint: `SHA256:${Math.random().toString(36).substring(2, 12)}...`,
        created: 'Just now',
        expiry: expiryLabel
    };
    setSSHKeys(prev => [newKey, ...prev]);
    setIsKeyModalOpen(false);
    setNewKeyName('');
    setNewKeyExpiry('90');
  };

  const handleViewKey = (key: typeof sshKeys[0]) => {
      const mockContent = `ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC0${Math.random().toString(36).substring(2)}${Math.random().toString(36).substring(2)}...${Math.random().toString(36).substring(2)} ${key.name}`;
      setViewKey({ name: key.name, content: mockContent });
  };

  const handleDeployClick = () => {
      if (projectStatus === 'building') return;
      setShowDeployConfirm(true);
  };

  const confirmDeploy = () => {
    setShowDeployConfirm(false);
    setProjectStatus('building');
    setShowBuildLogs(true);
    setBuildLogs(['> Initializing deployment sequence...', '> Connecting to build server...']);
    
    const newLogStart = {
        id: Date.now(),
        type: 'info',
        msg: `Manual deployment triggered from ${currentBranch}`,
        time: 'Just now'
    };
    setActivityLogs(prev => [newLogStart, ...prev]);

    // Simulate detailed build process
    const steps = [
        '> Checking out source code...',
        `> Switched to branch '${currentBranch}'`,
        '> Installing dependencies (npm install)...',
        '> [npm] Added 423 packages in 1.2s',
        '> Running lint checks...',
        '> [lint] No errors found.',
        '> Compiling assets...',
        '> [webpack] Building production bundle...',
        '> [webpack] Optimizing chunks...',
        '> Uploading artifacts to edge nodes...',
        '> Verifying health checks...',
        '> Deployment successful.'
    ];

    let step = 0;
    const interval = setInterval(() => {
        if (step >= steps.length) {
            clearInterval(interval);
            setProjectStatus('online');
            const newLogEnd = {
                id: Date.now() + 1,
                type: 'success',
                msg: `Deployment successful (v${Math.floor(Math.random() * 10)}.${Math.floor(Math.random() * 10)}.${Math.floor(Math.random() * 10)})`,
                time: 'Just now'
            };
            setActivityLogs(prev => [newLogEnd, ...prev]);
        } else {
            setBuildLogs(prev => [...prev, steps[step]]);
            step++;
        }
    }, 800);
  };

  const handleCommit = () => {
      if (!commitMessage.trim()) return;
      const newCommit = {
          hash: Math.random().toString(16).substring(2, 9),
          msg: commitMessage,
          author: 'Nexus Admin',
          time: 'Just now'
      };
      setCommits(prev => [newCommit, ...prev]);
      setCommitMessage('');
      setActivityLogs(prev => [{
          id: Date.now(),
          type: 'info',
          msg: `Git commit: ${newCommit.msg}`,
          time: 'Just now'
      }, ...prev]);
  };

  const handleStash = () => {
      const stashId = `stash@{${stashStack.length}}`;
      setStashStack(prev => [stashId, ...prev]);
      setActivityLogs(prev => [{
          id: Date.now(),
          type: 'info',
          msg: `Changes stashed to ${stashId}`,
          time: 'Just now'
      }, ...prev]);
  };

  const handlePopStash = () => {
      if (stashStack.length === 0) return;
      const stashId = stashStack[0];
      setStashStack(prev => prev.slice(1));
      setActivityLogs(prev => [{
          id: Date.now(),
          type: 'info',
          msg: `Applied stashed changes from ${stashId}`,
          time: 'Just now'
      }, ...prev]);
  };

  return (
    <div className="flex-1 overflow-y-auto bg-slate-950 p-6 md:p-8 animate-in fade-in duration-300">
      <div className="max-w-6xl mx-auto space-y-6">
        
        {/* Navigation & Header */}
        <div className="flex flex-col gap-6">
          <button 
            onClick={onBack}
            className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors w-fit group"
          >
            <ArrowLeft size={16} className="group-hover:-translate-x-1 transition-transform" />
            <span className="text-sm font-medium">Back to Dashboard</span>
          </button>

          <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
            <div className="space-y-2">
              <h1 className="text-3xl font-bold text-white tracking-tight">{project.name}</h1>
              <p className="text-slate-400 max-w-2xl">{project.description}</p>
            </div>
            <div className="flex items-center gap-3">
               <button 
                onClick={onOpenWorkspace}
                className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-semibold transition-colors shadow-lg shadow-indigo-500/20"
              >
                <Terminal size={18} />
                Open Workspace
              </button>
            </div>
          </div>

          {/* Status Bar */}
          <div className="flex flex-wrap gap-4 items-center p-4 bg-slate-900/50 border border-slate-800 rounded-xl backdrop-blur-sm">
             <div className={`px-3 py-1 rounded-full border text-xs font-bold uppercase flex items-center gap-2 ${getStatusColor(projectStatus)}`}>
                {projectStatus === 'building' ? <Loader2 size={12} className="animate-spin" /> : <Activity size={12} />}
                {projectStatus}
             </div>
             <div className={`px-3 py-1 rounded-full border text-xs font-bold uppercase flex items-center gap-2 ${getFrameworkColor(project.framework)}`}>
                <Box size={12} />
                {project.framework}
             </div>
             <div className="h-4 w-px bg-slate-800 mx-2" />
             <div className="flex items-center gap-2 text-xs text-slate-400">
                <Clock size={14} />
                <span>Last Active: <span className="text-slate-300">{project.lastActive.toLocaleDateString()} {project.lastActive.toLocaleTimeString()}</span></span>
             </div>
             <div className="flex items-center gap-2 text-xs text-slate-400 ml-auto">
                <Network size={14} />
                <span className="font-mono">{projectStatus === 'online' ? `localhost:${project.port}` : 'Port Inactive'}</span>
             </div>
          </div>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* Left Column: Stats & Resources */}
            <div className="lg:col-span-2 space-y-6">
                {/* Resource Usage */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-6 flex items-center gap-2">
                        <Activity size={16} className="text-indigo-400" />
                        Resource Utilization
                    </h3>
                    
                    <div className="space-y-6">
                        <div className="space-y-2">
                            <div className="flex justify-between text-xs text-slate-400">
                                <span className="flex items-center gap-2"><Cpu size={14} /> CPU Usage</span>
                                <span className="text-indigo-300 font-mono">{project.cpu}%</span>
                            </div>
                            <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                                <div className="h-full bg-indigo-500 rounded-full transition-all duration-1000" style={{ width: `${project.cpu}%` }}></div>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <div className="flex justify-between text-xs text-slate-400">
                                <span className="flex items-center gap-2"><HardDrive size={14} /> Memory Usage</span>
                                <span className="text-emerald-300 font-mono">{project.memory} MB / 2048 MB</span>
                            </div>
                            <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                                <div className="h-full bg-emerald-500 rounded-full transition-all duration-1000" style={{ width: `${(project.memory / 2048) * 100}%` }}></div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Git/Source Control Info */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 relative">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                            <GitBranch size={16} className="text-purple-400" />
                            Source Control
                        </h3>
                        
                        <div className="flex items-center gap-2">
                            <button 
                                onClick={() => setShowBlame(true)}
                                className="p-1.5 hover:bg-slate-800 rounded text-slate-500 hover:text-indigo-400 transition-colors"
                                title="View Git Blame"
                            >
                                <List size={16} />
                            </button>
                            <button 
                                onClick={() => setShowBranchRules(true)}
                                className="p-1.5 hover:bg-slate-800 rounded text-slate-500 hover:text-emerald-400 transition-colors"
                                title="Branch Protection Rules"
                            >
                                <Shield size={16} />
                            </button>
                            <div className="relative">
                                <button 
                                    onClick={() => setShowBranchMenu(!showBranchMenu)}
                                    className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 hover:border-indigo-500/50 hover:text-indigo-300 transition-all text-xs font-mono text-slate-400"
                                >
                                    <GitBranch size={12} />
                                    {currentBranch}
                                    <ChevronDown size={12} className={`transition-transform duration-200 ${showBranchMenu ? 'rotate-180' : ''}`} />
                                </button>
                                
                                {showBranchMenu && (
                                    <div className="absolute right-0 top-full mt-2 w-48 bg-slate-900 border border-slate-800 rounded-lg shadow-xl z-20 overflow-hidden animate-in fade-in zoom-in-95 duration-100">
                                        <div className="px-3 py-2 text-[10px] text-slate-500 uppercase font-bold border-b border-slate-800">Switch Branch</div>
                                        {availableBranches.map(branch => (
                                            <button
                                                key={branch}
                                                onClick={() => {
                                                    setCurrentBranch(branch);
                                                    setShowBranchMenu(false);
                                                }}
                                                className={`w-full text-left px-3 py-2 text-xs font-mono hover:bg-slate-800 transition-colors flex items-center justify-between ${currentBranch === branch ? 'text-indigo-400 bg-indigo-500/10' : 'text-slate-400'}`}
                                            >
                                                <span className="truncate">{branch}</span>
                                                {currentBranch === branch && <Check size={12} />}
                                            </button>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Clone URL */}
                    <div className="mb-6 flex items-center gap-2">
                        <div className="flex-1 p-1 bg-slate-950 rounded-lg border border-slate-800 flex items-center">
                            <div className="px-3 py-2 text-slate-500 font-mono text-xs select-none">$</div>
                            <input 
                                readOnly 
                                value={`git clone ${repoUrl}`}
                                className="flex-1 bg-transparent border-none outline-none text-slate-300 font-mono text-xs"
                            />
                        </div>
                        <button 
                            onClick={copyToClipboard}
                            className="flex items-center gap-2 px-3 py-2.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-slate-600 rounded-lg text-slate-300 text-xs font-medium transition-all"
                            title="Copy to clipboard"
                        >
                            {isCopied ? <Check size={14} className="text-emerald-400" /> : <Copy size={14} />}
                            {isCopied ? 'Copied' : 'Copy'}
                        </button>
                    </div>

                    {/* Git Controls & Staging */}
                    <div className="space-y-4">
                        <div className="flex gap-2">
                             <input 
                                type="text"
                                value={commitMessage}
                                onChange={(e) => setCommitMessage(e.target.value)}
                                placeholder="Commit message..."
                                className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500 transition-colors"
                             />
                             <button 
                                onClick={handleCommit}
                                disabled={!commitMessage.trim()}
                                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed text-white text-xs font-bold rounded-lg transition-colors flex items-center gap-2"
                             >
                                <GitCommit size={14} /> Commit
                             </button>
                        </div>
                        
                        <div className="flex items-center justify-between pb-2 border-b border-slate-800/50">
                            <div className="flex gap-2">
                                <button 
                                    onClick={handleStash}
                                    className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-[10px] font-bold uppercase rounded-lg transition-colors border border-slate-700"
                                >
                                    <Archive size={12} /> Stash
                                </button>
                                <button 
                                    onClick={handlePopStash}
                                    disabled={stashStack.length === 0}
                                    className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed text-slate-300 text-[10px] font-bold uppercase rounded-lg transition-colors border border-slate-700"
                                >
                                    <ArrowUpCircle size={12} /> Pop
                                </button>
                            </div>
                            <span className="text-[10px] text-slate-500 font-mono">
                                {stashStack.length} stashed
                            </span>
                        </div>
                    </div>

                    {/* Recent Commits List */}
                    <div className="mt-4 space-y-3">
                        <h4 className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-2">Recent Commits</h4>
                        {commits.map((commit, idx) => (
                            <div 
                                key={idx} 
                                onClick={() => setViewCommitDiff(commit)}
                                className="group p-3 bg-slate-950 rounded-lg border border-slate-800 hover:border-indigo-500/30 hover:bg-slate-900 transition-all cursor-pointer"
                            >
                                <div className="flex justify-between items-start mb-1">
                                    <span className="font-mono text-indigo-400 text-xs flex items-center gap-2">
                                        {commit.hash}
                                        <Maximize2 size={10} className="opacity-0 group-hover:opacity-100 transition-opacity" />
                                    </span>
                                    <span className="text-[10px] text-slate-500">{commit.time}</span>
                                </div>
                                <p className="text-xs text-slate-300 font-medium truncate mb-2">{commit.msg}</p>
                                <div className="flex items-center gap-2 text-[10px] text-slate-500">
                                    <User size={10} />
                                    <span>{commit.author}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* SSH Key Management */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                            <Key size={16} className="text-amber-400" />
                            SSH Access Keys
                        </h3>
                        <button 
                            onClick={() => setIsKeyModalOpen(true)}
                            className="flex items-center gap-1.5 px-2 py-1 rounded bg-indigo-600 hover:bg-indigo-500 text-white text-[10px] font-bold uppercase tracking-wide transition-colors shadow-lg shadow-indigo-500/20"
                        >
                            <Plus size={12} /> Generate Key
                        </button>
                    </div>
                    <div className="space-y-3">
                        {sshKeys.map(key => (
                            <div 
                                key={key.id} 
                                className="flex items-center justify-between p-3 bg-slate-950 rounded-lg border border-slate-800 group hover:border-indigo-500/30 transition-colors cursor-pointer"
                                onClick={() => handleViewKey(key)}
                            >
                                <div className="flex items-center gap-3">
                                    <div className="p-2 bg-amber-500/10 rounded-lg text-amber-500 border border-amber-500/20">
                                        <Key size={14} />
                                    </div>
                                    <div>
                                        <div className="text-xs font-bold text-slate-300 group-hover:text-indigo-300 transition-colors flex items-center gap-2">
                                            {key.name}
                                            {key.expiry.includes('days') && parseInt(key.expiry) < 7 && (
                                                <AlertTriangle size={10} className="text-amber-500" />
                                            )}
                                        </div>
                                        <div className="text-[10px] font-mono text-slate-500">{key.fingerprint}</div>
                                    </div>
                                </div>
                                <div className="flex items-center gap-4">
                                    <div className="flex flex-col items-end gap-0.5">
                                        <span className="text-[10px] text-slate-500">Created: {key.created}</span>
                                        <span className={`text-[10px] ${key.expiry === 'Never' ? 'text-emerald-500' : 'text-slate-500'}`}>Expires: {key.expiry}</span>
                                    </div>
                                    <div className="flex items-center gap-2 pl-2 border-l border-slate-800">
                                        <Eye size={14} className="text-slate-600 group-hover:text-indigo-400 transition-colors" />
                                        <button 
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                setSSHKeys(prev => prev.filter(k => k.id !== key.id));
                                            }}
                                            className="text-slate-600 hover:text-red-400 p-1 hover:bg-slate-900 rounded transition-colors"
                                            title="Revoke Key"
                                        >
                                            <Trash2 size={12} />
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))}
                        
                        {sshKeys.length === 0 && (
                            <div className="text-center py-6 text-slate-500 text-xs italic">
                                No SSH keys configured for this project.
                            </div>
                        )}
                    </div>
                </div>

            </div>

            {/* Right Column: Activity Log & Build Logs */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col h-full">
                <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-4 flex items-center gap-2">
                    <Terminal size={16} className="text-emerald-400" />
                    Recent Activity
                </h3>
                
                {/* Build Logs Console */}
                {showBuildLogs && (
                    <div className="mb-4 bg-black rounded-lg border border-slate-800 p-3 font-mono text-[10px] h-48 overflow-y-auto">
                        <div className="flex items-center gap-2 mb-2 pb-2 border-b border-slate-800 text-slate-500">
                            <Loader2 size={10} className="animate-spin" />
                            <span>Build Output - {currentBranch}</span>
                        </div>
                        <div className="space-y-1">
                            {buildLogs.map((log, i) => (
                                <div key={i} className="text-slate-300">{log}</div>
                            ))}
                            <div ref={logsEndRef} />
                        </div>
                    </div>
                )}

                <div className="flex-1 space-y-4">
                    {activityLogs.map((log) => (
                        <div key={log.id} className="relative pl-6 pb-2 border-l border-slate-800 last:border-0 animate-in fade-in slide-in-from-left-2 duration-300">
                            <div className={`absolute -left-[5px] top-1 w-2.5 h-2.5 rounded-full border-2 border-slate-900 ${
                                log.type === 'success' ? 'bg-emerald-500' :
                                log.type === 'warning' ? 'bg-amber-500' : 'bg-blue-500'
                            }`} />
                            <div className="text-xs font-medium text-slate-300">{log.msg}</div>
                            <div className="text-[10px] text-slate-500 mt-1">{log.time}</div>
                        </div>
                    ))}
                    
                    {/* Mock Older Logs */}
                     <div className="relative pl-6 pt-2">
                        <div className="absolute -left-[5px] top-3 w-2.5 h-2.5 rounded-full border-2 border-slate-900 bg-slate-700" />
                        <div className="text-xs text-slate-500 italic">View older logs...</div>
                     </div>
                </div>
                
                <div className="mt-6 pt-4 border-t border-slate-800">
                    <button 
                        onClick={handleDeployClick}
                        disabled={projectStatus === 'building'}
                        className={`w-full py-2 ${projectStatus === 'building' ? 'bg-indigo-600/50 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-500'} text-white text-xs font-semibold rounded-lg transition-colors flex items-center justify-center gap-2 shadow-lg shadow-indigo-500/20`}
                    >
                        {projectStatus === 'building' ? (
                            <>
                                <Loader2 size={14} className="animate-spin" />
                                Deploying...
                            </>
                        ) : (
                            <>
                                <PlayCircle size={14} />
                                Trigger Deployment
                            </>
                        )}
                    </button>
                </div>
            </div>
        </div>
      </div>
      
      {/* Key Generation Modal */}
      {isKeyModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 w-full max-w-sm shadow-2xl relative animate-in zoom-in-95 duration-200">
                <button 
                    onClick={() => setIsKeyModalOpen(false)}
                    className="absolute right-4 top-4 text-slate-500 hover:text-white transition-colors"
                >
                    <X size={18} />
                </button>
                
                <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                    <Key size={18} className="text-amber-400" />
                    Generate New SSH Key
                </h3>

                <div className="space-y-4">
                    <div className="space-y-1">
                        <label className="text-xs font-semibold text-slate-400 uppercase">Key Name</label>
                        <input 
                            type="text"
                            autoFocus
                            value={newKeyName}
                            onChange={(e) => setNewKeyName(e.target.value)}
                            placeholder="e.g. MacBook Pro"
                            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500 transition-colors"
                            onKeyDown={(e) => e.key === 'Enter' && createSSHKey()}
                        />
                    </div>

                    <div className="space-y-1">
                        <label className="text-xs font-semibold text-slate-400 uppercase">Expiration</label>
                        <select 
                            value={newKeyExpiry}
                            onChange={(e) => setNewKeyExpiry(e.target.value)}
                            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500 transition-colors appearance-none"
                        >
                            <option value="30">30 Days</option>
                            <option value="90">90 Days</option>
                            <option value="365">1 Year</option>
                            <option value="never">Never</option>
                        </select>
                    </div>
                    
                    <div className="bg-amber-500/10 border border-amber-500/20 rounded-lg p-3">
                        <div className="flex gap-2">
                            <AlertCircle size={14} className="text-amber-500 shrink-0 mt-0.5" />
                            <p className="text-[10px] text-amber-200/80 leading-relaxed">
                                The private key will be displayed only once. Make sure to copy it immediately.
                            </p>
                        </div>
                    </div>

                    <div className="flex gap-3 pt-2">
                        <button 
                            onClick={() => setIsKeyModalOpen(false)}
                            className="flex-1 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold uppercase rounded-lg transition-colors"
                        >
                            Cancel
                        </button>
                        <button 
                            onClick={createSSHKey}
                            disabled={!newKeyName.trim()}
                            className="flex-1 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed text-white text-xs font-bold uppercase rounded-lg transition-colors shadow-lg shadow-indigo-500/20"
                        >
                            Generate
                        </button>
                    </div>
                </div>
            </div>
        </div>
      )}

      {/* View Full Key Modal */}
      {viewKey && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 w-full max-w-lg shadow-2xl relative animate-in zoom-in-95 duration-200">
                  <button 
                      onClick={() => setViewKey(null)}
                      className="absolute right-4 top-4 text-slate-500 hover:text-white transition-colors"
                  >
                      <X size={18} />
                  </button>
                  <h3 className="text-lg font-bold text-white mb-1 flex items-center gap-2">
                      <FileText size={18} className="text-blue-400" />
                      Public Key
                  </h3>
                  <p className="text-xs text-slate-500 mb-4">{viewKey.name}</p>
                  
                  <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 font-mono text-[10px] text-slate-300 break-all leading-relaxed max-h-64 overflow-y-auto">
                      {viewKey.content}
                  </div>
                  
                  <div className="mt-4 flex justify-end">
                      <button 
                          onClick={() => {
                              navigator.clipboard.writeText(viewKey.content);
                              setViewKey(null);
                          }}
                          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-lg transition-colors"
                      >
                          Copy & Close
                      </button>
                  </div>
              </div>
          </div>
      )}

      {/* Deploy Confirmation Modal */}
      {showDeployConfirm && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 w-full max-w-sm shadow-2xl relative animate-in zoom-in-95 duration-200">
                  <div className="flex items-center gap-4 mb-4">
                      <div className="p-3 bg-amber-500/10 rounded-full border border-amber-500/20 text-amber-500">
                          <AlertTriangle size={24} />
                      </div>
                      <div>
                          <h3 className="text-lg font-bold text-white">Confirm Deployment</h3>
                          <p className="text-xs text-slate-400">Production environment</p>
                      </div>
                  </div>
                  
                  <p className="text-sm text-slate-300 mb-6 leading-relaxed">
                      You are about to deploy branch <span className="text-indigo-400 font-mono font-bold bg-indigo-500/10 px-1 rounded">{currentBranch}</span> to production. This action will trigger a new build and replace the currently running instance.
                  </p>

                  <div className="flex gap-3">
                      <button 
                          onClick={() => setShowDeployConfirm(false)}
                          className="flex-1 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold uppercase rounded-lg transition-colors"
                      >
                          Cancel
                      </button>
                      <button 
                          onClick={confirmDeploy}
                          className="flex-1 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold uppercase rounded-lg transition-colors shadow-lg shadow-indigo-500/20"
                      >
                          Confirm Deploy
                      </button>
                  </div>
              </div>
          </div>
      )}

      {/* Branch Protection Rules Modal */}
      {showBranchRules && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 w-full max-w-md shadow-2xl relative animate-in zoom-in-95 duration-200">
                  <button 
                      onClick={() => setShowBranchRules(false)}
                      className="absolute right-4 top-4 text-slate-500 hover:text-white transition-colors"
                  >
                      <X size={18} />
                  </button>
                  <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                      <Shield size={18} className="text-emerald-400" />
                      Branch Protection Rules
                  </h3>
                  <div className="mb-4 p-3 bg-indigo-900/20 border border-indigo-500/20 rounded-lg">
                      <p className="text-xs text-indigo-300 flex items-center gap-2">
                          <GitBranch size={12} />
                          Target Branch: <span className="font-mono font-bold">{currentBranch}</span>
                      </p>
                  </div>
                  <div className="space-y-3">
                      <label className="flex items-start gap-3 p-3 bg-slate-950 rounded-lg border border-slate-800 cursor-pointer hover:border-slate-700 transition-colors">
                          <input 
                              type="checkbox" 
                              checked={branchRules.requirePullRequest}
                              onChange={(e) => setBranchRules({...branchRules, requirePullRequest: e.target.checked})}
                              className="mt-1 accent-indigo-500"
                          />
                          <div>
                              <div className="text-sm font-bold text-slate-200">Require pull request</div>
                              <div className="text-xs text-slate-500">Reviews must be approved before merging.</div>
                          </div>
                      </label>
                      <label className="flex items-start gap-3 p-3 bg-slate-950 rounded-lg border border-slate-800 cursor-pointer hover:border-slate-700 transition-colors">
                          <input 
                              type="checkbox" 
                              checked={branchRules.requireStatusChecks}
                              onChange={(e) => setBranchRules({...branchRules, requireStatusChecks: e.target.checked})}
                              className="mt-1 accent-indigo-500"
                          />
                          <div>
                              <div className="text-sm font-bold text-slate-200">Require status checks</div>
                              <div className="text-xs text-slate-500">Build and tests must pass before merging.</div>
                          </div>
                      </label>
                      <label className="flex items-start gap-3 p-3 bg-slate-950 rounded-lg border border-slate-800 cursor-pointer hover:border-slate-700 transition-colors">
                          <input 
                              type="checkbox" 
                              checked={branchRules.includeAdmins}
                              onChange={(e) => setBranchRules({...branchRules, includeAdmins: e.target.checked})}
                              className="mt-1 accent-indigo-500"
                          />
                          <div>
                              <div className="text-sm font-bold text-slate-200">Include administrators</div>
                              <div className="text-xs text-slate-500">Enforce rules for all users, including admins.</div>
                          </div>
                      </label>
                  </div>
                  <div className="mt-6 flex justify-end">
                      <button 
                          onClick={() => setShowBranchRules(false)}
                          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-lg transition-colors"
                      >
                          Save Changes
                      </button>
                  </div>
              </div>
          </div>
      )}

      {/* Git Blame Modal */}
      {showBlame && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
              <div className="bg-slate-900 border border-slate-800 rounded-xl w-full max-w-4xl h-[80vh] flex flex-col shadow-2xl relative animate-in zoom-in-95 duration-200 overflow-hidden">
                  <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-900">
                    <h3 className="text-lg font-bold text-white flex items-center gap-2">
                        <FileCode size={18} className="text-blue-400" />
                        Git Blame: src/App.tsx
                    </h3>
                    <button 
                        onClick={() => setShowBlame(false)}
                        className="text-slate-500 hover:text-white transition-colors"
                    >
                        <X size={20} />
                    </button>
                  </div>
                  <div className="flex-1 overflow-auto bg-slate-950 p-0 font-mono text-xs">
                      {[
                          { hash: '8f3a29b', author: 'Nexus Admin', date: '2h ago', content: 'import React from "react";' },
                          { hash: '8f3a29b', author: 'Nexus Admin', date: '2h ago', content: 'import ReactDOM from "react-dom/client";' },
                          { hash: '4b1d90c', author: 'System', date: '1d ago', content: '' },
                          { hash: '4b1d90c', author: 'System', date: '1d ago', content: 'function App() {' },
                          { hash: '7e2c18a', author: 'Nexus Admin', date: '5h ago', content: '  return (' },
                          { hash: '7e2c18a', author: 'Nexus Admin', date: '5h ago', content: '    <div className="app">' },
                          { hash: '7e2c18a', author: 'Nexus Admin', date: '5h ago', content: '       <h1>Nexus Dashboard</h1>' },
                          { hash: '4b1d90c', author: 'System', date: '1d ago', content: '    </div>' },
                          { hash: '4b1d90c', author: 'System', date: '1d ago', content: '  );' },
                          { hash: '4b1d90c', author: 'System', date: '1d ago', content: '}' },
                      ].map((line, i) => (
                          <div key={i} className="flex hover:bg-slate-900 group">
                              <div className="w-24 px-3 py-1 text-indigo-400 border-r border-slate-800 shrink-0 bg-slate-950 group-hover:bg-slate-900 select-none">{line.hash}</div>
                              <div className="w-32 px-3 py-1 text-slate-500 border-r border-slate-800 shrink-0 bg-slate-950 group-hover:bg-slate-900 truncate">{line.author}</div>
                              <div className="w-20 px-3 py-1 text-slate-600 border-r border-slate-800 shrink-0 bg-slate-950 group-hover:bg-slate-900 text-right">{line.date}</div>
                              <div className="px-4 py-1 text-slate-300 whitespace-pre flex-1">{line.content}</div>
                          </div>
                      ))}
                  </div>
              </div>
          </div>
      )}

      {/* Commit Diff Modal */}
      {viewCommitDiff && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
              <div className="bg-slate-900 border border-slate-800 rounded-xl w-full max-w-3xl shadow-2xl relative animate-in zoom-in-95 duration-200 max-h-[80vh] flex flex-col">
                  <div className="p-6 border-b border-slate-800">
                      <button 
                          onClick={() => setViewCommitDiff(null)}
                          className="absolute right-4 top-4 text-slate-500 hover:text-white transition-colors"
                      >
                          <X size={18} />
                      </button>
                      <h3 className="text-lg font-bold text-white flex items-center gap-2 mb-1">
                          <GitPullRequest size={18} className="text-purple-400" />
                          Commit Details
                      </h3>
                      <div className="text-sm font-mono text-slate-400 flex items-center gap-2">
                          <span className="text-indigo-400">{viewCommitDiff.hash}</span>
                          <span>•</span>
                          <span>{viewCommitDiff.msg}</span>
                      </div>
                  </div>
                  
                  <div className="flex-1 overflow-auto p-0 font-mono text-xs">
                      <div className="px-4 py-2 bg-slate-800/50 text-slate-300 border-b border-slate-800 flex justify-between">
                          <span>src/config.ts</span>
                          <span className="text-slate-500">2 additions, 1 deletion</span>
                      </div>
                      <div className="flex bg-slate-950/50">
                          <div className="w-12 text-slate-600 text-right pr-2 select-none py-1 border-r border-slate-800">1</div>
                          <div className="flex-1 py-1 px-4 text-slate-400">export const API_ENDPOINT = "https://api.nexus.ai/v1";</div>
                      </div>
                      <div className="flex bg-red-900/10">
                          <div className="w-12 text-slate-600 text-right pr-2 select-none py-1 border-r border-slate-800 bg-red-900/20">2</div>
                          <div className="flex-1 py-1 px-4 text-red-300">- export const TIMEOUT = 5000;</div>
                      </div>
                      <div className="flex bg-emerald-900/10">
                          <div className="w-12 text-slate-600 text-right pr-2 select-none py-1 border-r border-slate-800 bg-emerald-900/20">3</div>
                          <div className="flex-1 py-1 px-4 text-emerald-300">+ export const TIMEOUT = 10000;</div>
                      </div>
                      <div className="flex bg-emerald-900/10">
                          <div className="w-12 text-slate-600 text-right pr-2 select-none py-1 border-r border-slate-800 bg-emerald-900/20">4</div>
                          <div className="flex-1 py-1 px-4 text-emerald-300">+ export const RETRY_COUNT = 3;</div>
                      </div>
                      <div className="flex bg-slate-950/50">
                          <div className="w-12 text-slate-600 text-right pr-2 select-none py-1 border-r border-slate-800">5</div>
                          <div className="flex-1 py-1 px-4 text-slate-400">export const DEBUG_MODE = process.env.NODE_ENV === 'development';</div>
                      </div>
                  </div>

                  <div className="p-4 border-t border-slate-800 bg-slate-900 flex justify-end">
                      <button 
                          onClick={() => setViewCommitDiff(null)}
                          className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold rounded-lg transition-colors"
                      >
                          Close
                      </button>
                  </div>
              </div>
          </div>
      )}

    </div>
  );
};
