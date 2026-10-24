import React, { useState, useEffect } from 'react';
import { 
  LayoutGrid, 
  Box, 
  Activity, 
  Cpu, 
  Globe, 
  Terminal, 
  MoreVertical, 
  Play, 
  StopCircle,
  GitBranch,
  Clock,
  Plus,
  Loader2
} from 'lucide-react';
import { Project, ProjectStatus } from '../types';
import { NewProjectModal } from './NewProjectModal';

interface DashboardProps {
  onOpenProject: (project: Project) => void;
  onViewDetails: (project: Project) => void;
}

interface BackgroundProcess {
  id: string;
  pid: number;
  command: string;
  status: 'running' | 'building' | 'error';
  startTime: number;
  latestOutput: string;
}

const MOCK_PROJECTS: Project[] = [
  {
    id: 'p1',
    name: 'Nexus Core Platform',
    description: 'Main operating system interface for the agent network.',
    status: 'online',
    framework: 'react',
    lastActive: new Date(),
    cpu: 12,
    memory: 450,
    port: 3000
  },
  {
    id: 'p2',
    name: 'Data Pipeline Alpha',
    description: 'Real-time data ingestion service with Gemini processing.',
    status: 'building',
    framework: 'python',
    lastActive: new Date(Date.now() - 3600000),
    cpu: 85,
    memory: 1024,
    port: 8080
  },
  {
    id: 'p3',
    name: 'Landing Page v2',
    description: 'Marketing site with interactive 3D elements.',
    status: 'offline',
    framework: 'html',
    lastActive: new Date(Date.now() - 86400000),
    cpu: 0,
    memory: 0,
    port: 5500
  },
  {
    id: 'p4',
    name: 'Auth Service',
    description: 'JWT authentication provider and user management.',
    status: 'online',
    framework: 'node',
    lastActive: new Date(Date.now() - 1800000),
    cpu: 4,
    memory: 128,
    port: 4000
  }
];

export const Dashboard: React.FC<DashboardProps> = ({ onOpenProject, onViewDetails }) => {
  const [projects, setProjects] = useState<Project[]>(MOCK_PROJECTS);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [processes, setProcesses] = useState<BackgroundProcess[]>([
    { 
      id: '1', 
      pid: 8392, 
      command: 'npm run start:prod --filter=@nexus/core', 
      status: 'running', 
      startTime: Date.now() - 2535000, 
      latestOutput: '[Nest] 8392  - LOG [RouterExplorer] Mapped {/api/v1/users, GET} route'
    },
    { 
      id: '2', 
      pid: 1102, 
      command: 'python3 worker_queue.py --shards=4', 
      status: 'running', 
      startTime: Date.now() - 8133000, 
      latestOutput: 'INFO:root:Shard 2 processing batch #4092 - 145 items'
    },
    { 
      id: '3', 
      pid: 9941, 
      command: 'docker build -t nexus/auth-service .', 
      status: 'building', 
      startTime: Date.now() - 65000, 
      latestOutput: '#8 [4/5] RUN npm install --production' 
    }
  ]);

  const [currentTime, setCurrentTime] = useState(Date.now());

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(Date.now());
      setProcesses(prev => prev.map(p => {
        let newOutput = p.latestOutput;
        
        // Randomly update output based on command type
        if (Math.random() > 0.4) {
            if (p.command.includes('npm')) {
                const logs = [
                    '[Nest] LOG [InstanceLoader] AppModule dependencies initialized',
                    '[Nest] LOG [RoutesResolver] AppController {/}:',
                    'GET /health 200 4ms',
                    'POST /api/v1/agent/interact 201 124ms',
                    'WARN [HMR] Update check failed: connection refused',
                    '[TypeOrmModule] Dependencies initialized'
                ];
                newOutput = logs[Math.floor(Math.random() * logs.length)];
            } else if (p.command.includes('python')) {
                const logs = [
                    'INFO:root:Heartbeat received from worker-01',
                    'DEBUG:asyncio:Using selector: EpollSelector',
                    'INFO:root:Batch processed in 0.4s',
                    'WARNING:root:High latency on vector search (400ms)',
                    'INFO:celery.worker.strategy:Task nexus.tasks.index[4a8b...] received'
                ];
                newOutput = logs[Math.floor(Math.random() * logs.length)];
            } else if (p.command.includes('docker')) {
                const logs = [
                    '#8 [5/5] COPY . .',
                    '#9 exporting to image',
                    '#9 exporting layers 0.2s done',
                    '#9 writing image sha256:e8f... done',
                    '#10 naming to docker.io/nexus/auth-service:latest'
                ];
                newOutput = logs[Math.floor(Math.random() * logs.length)];
            }
        }
        
        return { ...p, latestOutput: newOutput };
      }));
    }, 1500);
    return () => clearInterval(interval);
  }, []);

  const handleCreateProject = (newProjectData: Omit<Project, 'id' | 'lastActive' | 'cpu' | 'memory' | 'port'>) => {
    const newProject: Project = {
      ...newProjectData,
      id: Math.random().toString(36).substring(7),
      lastActive: new Date(),
      cpu: 0,
      memory: 0,
      port: Math.floor(Math.random() * (9000 - 3000) + 3000)
    };
    setProjects(prev => [...prev, newProject]);
  };

  const formatDuration = (startTime: number) => {
    const diff = Math.floor((currentTime - startTime) / 1000);
    const h = Math.floor(diff / 3600);
    const m = Math.floor((diff % 3600) / 60);
    const s = diff % 60;
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  const getStatusTextColor = (status: ProjectStatus) => {
    switch (status) {
      case 'online': return 'text-emerald-400';
      case 'building': return 'text-amber-400';
      case 'error': return 'text-red-500';
      case 'offline': return 'text-red-400';
      default: return 'text-slate-400';
    }
  };

  const getProcessStatusColor = (status: BackgroundProcess['status']) => {
    switch(status) {
        case 'running': return 'text-emerald-500';
        case 'building': return 'text-amber-500';
        case 'error': return 'text-red-500';
        default: return 'text-slate-500';
    }
  };

  const getFrameworkIcon = (fw: string) => {
    switch (fw) {
      case 'react': return <div className="text-cyan-400 font-bold text-xs border border-cyan-500/30 px-2 py-0.5 rounded-full bg-cyan-950/30">REACT</div>;
      case 'node': return <div className="text-green-400 font-bold text-xs border border-green-500/30 px-2 py-0.5 rounded-full bg-green-950/30">NODE</div>;
      case 'python': return <div className="text-yellow-400 font-bold text-xs border border-yellow-500/30 px-2 py-0.5 rounded-full bg-yellow-950/30">PYTHON</div>;
      default: return <div className="text-orange-400 font-bold text-xs border border-orange-500/30 px-2 py-0.5 rounded-full bg-orange-950/30">HTML</div>;
    }
  };

  const getLogColor = (log: string) => {
    if (log.includes('ERROR') || log.includes('failed') || log.includes('refused')) return 'text-red-400';
    if (log.includes('WARN') || log.includes('WARNING')) return 'text-amber-400';
    if (log.includes('SUCCESS') || log.includes('done') || log.includes('200') || log.includes('201')) return 'text-emerald-400';
    if (log.includes('INFO') || log.includes('LOG') || log.includes('DEBUG')) return 'text-blue-400';
    return 'text-slate-500 group-hover:text-slate-300';
  };

  return (
    <div className="flex-1 overflow-y-auto p-8 bg-slate-950">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-slate-900/50 border border-slate-800 p-4 rounded-xl backdrop-blur-sm">
            <div className="flex items-center gap-3 text-slate-400 mb-2">
              <Box size={16} />
              <span className="text-xs uppercase tracking-wider font-semibold">Total Projects</span>
            </div>
            <div className="text-2xl font-bold text-white">{projects.length}</div>
          </div>
          <div className="bg-slate-900/50 border border-slate-800 p-4 rounded-xl backdrop-blur-sm">
            <div className="flex items-center gap-3 text-slate-400 mb-2">
              <Activity size={16} />
              <span className="text-xs uppercase tracking-wider font-semibold">Active Agents</span>
            </div>
            <div className="text-2xl font-bold text-emerald-400">4</div>
          </div>
          <div className="bg-slate-900/50 border border-slate-800 p-4 rounded-xl backdrop-blur-sm">
            <div className="flex items-center gap-3 text-slate-400 mb-2">
              <Cpu size={16} />
              <span className="text-xs uppercase tracking-wider font-semibold">System Load</span>
            </div>
            <div className="text-2xl font-bold text-indigo-400">24%</div>
          </div>
          <div 
            onClick={() => setIsModalOpen(true)}
            className="bg-gradient-to-br from-indigo-600 to-purple-600 border border-indigo-400/20 p-4 rounded-xl flex flex-col justify-center items-center cursor-pointer hover:shadow-lg hover:shadow-indigo-500/20 transition-all group"
          >
             <Plus size={24} className="text-white mb-1 group-hover:scale-110 transition-transform" />
             <span className="text-xs font-bold text-white uppercase tracking-wider">New Project</span>
          </div>
        </div>

        {/* Projects Grid */}
        <div>
          <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <LayoutGrid size={18} className="text-indigo-400" />
            Active Projects
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project) => (
              <div 
                key={project.id}
                onClick={() => onViewDetails(project)}
                className="group bg-slate-900 border border-slate-800 rounded-xl overflow-hidden hover:border-indigo-500/50 transition-all duration-300 hover:shadow-xl hover:shadow-indigo-900/10 cursor-pointer"
              >
                {/* Card Header */}
                <div className="p-5 border-b border-slate-800 bg-slate-900/50 relative">
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex items-center gap-2">
                      {/* Visual Status Indicator */}
                      {project.status === 'building' ? (
                        <div className="relative">
                            <Loader2 size={16} className="animate-spin text-amber-500" />
                            <span className="absolute inset-0 bg-amber-500/20 blur-[2px] rounded-full"></span>
                        </div>
                      ) : project.status === 'online' ? (
                        <span className="relative flex h-3 w-3">
                          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                          <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.8)] border border-emerald-400/30"></span>
                        </span>
                      ) : (
                        <span className="relative flex h-2.5 w-2.5">
                            {project.status === 'error' && <span className="animate-pulse absolute inline-flex h-full w-full rounded-full bg-red-500 opacity-50"></span>}
                            <span className={`relative inline-flex rounded-full h-2.5 w-2.5 ${project.status === 'error' ? 'bg-red-600 shadow-[0_0_8px_rgba(220,38,38,0.8)]' : 'bg-red-500/50'}`}></span>
                        </span>
                      )}

                      <span className={`text-xs font-bold uppercase tracking-wide ml-1 ${getStatusTextColor(project.status)}`}>
                        {project.status}
                      </span>
                    </div>
                    <button className="text-slate-500 hover:text-white transition-colors" onClick={(e) => e.stopPropagation()}>
                      <MoreVertical size={16} />
                    </button>
                  </div>
                  <h3 className="text-lg font-bold text-slate-100 group-hover:text-indigo-300 transition-colors">{project.name}</h3>
                  <p className="text-sm text-slate-500 mt-1 line-clamp-2 min-h-[40px]">{project.description}</p>
                </div>

                {/* Card Stats */}
                <div className="px-5 py-4 grid grid-cols-2 gap-4 text-xs text-slate-400">
                  <div className="space-y-1">
                    <div className="flex items-center gap-1.5">
                        <Clock size={12} />
                        <span>Last Active</span>
                    </div>
                    <div className="text-slate-300 font-mono">{project.lastActive.toLocaleDateString()}</div>
                  </div>
                  <div className="space-y-1">
                    <div className="flex items-center gap-1.5">
                        <Globe size={12} />
                        <span>Port</span>
                    </div>
                    <div className="text-slate-300 font-mono">{project.port}</div>
                  </div>
                  <div className="space-y-1">
                    <div className="flex items-center gap-1.5">
                        <Cpu size={12} />
                        <span>CPU Usage</span>
                    </div>
                    <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                        <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${project.cpu}%` }}></div>
                    </div>
                  </div>
                  <div className="space-y-1">
                    <div className="flex items-center gap-1.5">
                        <Terminal size={12} />
                        <span>Memory</span>
                    </div>
                    <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                        <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${(project.memory / 2048) * 100}%` }}></div>
                    </div>
                  </div>
                </div>

                {/* Card Footer */}
                <div className="px-5 py-4 bg-slate-950 border-t border-slate-800 flex items-center justify-between" onClick={(e) => e.stopPropagation()}>
                   {getFrameworkIcon(project.framework)}
                   
                   <div className="flex gap-2">
                      <button className="p-2 rounded-lg bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white transition-colors">
                        <GitBranch size={14} />
                      </button>
                      <button 
                        onClick={(e) => {
                            e.stopPropagation();
                            onOpenProject(project);
                        }}
                        className="flex items-center gap-2 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold transition-colors shadow-lg shadow-indigo-500/20"
                      >
                        <Terminal size={12} />
                        Open Workspace
                      </button>
                   </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Terminal Sessions Snippet */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
                <h3 className="font-bold text-white flex items-center gap-2">
                    <Terminal size={16} className="text-emerald-400" />
                    Active Background Processes
                </h3>
                <span className="text-xs px-2 py-1 rounded bg-slate-800 text-slate-400">{processes.length} Running</span>
            </div>
            <div className="p-4 font-mono text-xs space-y-2">
                {processes.map(proc => (
                  <div key={proc.id} className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 text-slate-400 hover:bg-slate-800/50 p-2 rounded cursor-pointer transition-colors group">
                      <div className="flex items-center gap-4 min-w-[150px]">
                          <span className={`${getProcessStatusColor(proc.status)} shrink-0 flex items-center gap-2 w-20`}>
                              <span className={`w-2 h-2 rounded-full bg-current ${proc.status === 'running' ? 'animate-pulse' : ''}`}></span>
                              {proc.status}
                          </span>
                          <span className="text-indigo-400 shrink-0">pid: {proc.pid}</span>
                      </div>
                      
                      <div className="flex-1 min-w-0 flex flex-col gap-1">
                          <span className="text-slate-300 font-semibold truncate">{proc.command}</span>
                          <div className="flex items-center gap-2 overflow-hidden">
                              <span className="text-slate-600 shrink-0">{'>'}</span>
                              <span className={`truncate font-mono text-[10px] transition-colors ${getLogColor(proc.latestOutput)}`}>
                                  {proc.latestOutput}
                              </span>
                          </div>
                      </div>

                      <span className="ml-auto text-slate-600 font-mono shrink-0">
                          {formatDuration(proc.startTime)}
                      </span>
                  </div>
                ))}
            </div>
        </div>
      </div>
      <NewProjectModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} onCreate={handleCreateProject} />
    </div>
  );
};
