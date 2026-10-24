import { motion } from "framer-motion";
import { CyberCard } from "@/components/CyberCard";
import { CyberButton } from "@/components/CyberButton";
import { Activity, Database, Cpu, Lock, Shield, Zap } from "lucide-react";
import { Link } from "wouter";

export default function Dashboard() {
  return (
    <div className="space-y-8">
      {/* Header Section */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-primary/20 pb-6">
        <div>
          <h1 className="text-4xl md:text-5xl font-display font-bold text-white mb-2">
            SYSTEM <span className="text-primary text-glow">OVERVIEW</span>
          </h1>
          <p className="font-mono text-primary/60">
            // PROTOCOL: GENESIS // STATUS: ACTIVE // CLEARANCE: OMEGA
          </p>
        </div>
        <div className="flex gap-4">
          <Link href="/simulation">
            <CyberButton variant="primary" glitch>
              INITIATE SEQUENCE
            </CyberButton>
          </Link>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
          icon={Activity} 
          label="Sys. Stability" 
          value="98.4%" 
          color="text-green-400" 
          trend="+0.2%"
        />
        <StatCard 
          icon={Database} 
          label="Data Integrity" 
          value="100%" 
          color="text-primary" 
        />
        <StatCard 
          icon={Cpu} 
          label="Processing Load" 
          value="42%" 
          color="text-secondary" 
          trend="-5.1%"
        />
        <StatCard 
          icon={Lock} 
          label="Encryption" 
          value="AES-4096" 
          color="text-accent" 
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Feed */}
        <div className="lg:col-span-2 space-y-6">
          <CyberCard className="min-h-[400px]" title="Active Processes">
            <div className="space-y-4 font-mono text-sm">
              {[1, 2, 3, 4, 5].map((i) => (
                <motion.div 
                  key={i}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className="flex items-center justify-between p-3 bg-white/5 border border-white/10 hover:border-primary/50 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div className={`w-2 h-2 rounded-full ${i === 1 ? 'bg-primary animate-pulse' : 'bg-green-500'}`} />
                    <span className="text-white/80">PROC_ID_{1000 + i * 42}</span>
                  </div>
                  <span className="text-primary/60">Running...</span>
                  <div className="w-24 h-1 bg-white/10 rounded-full overflow-hidden">
                    <motion.div 
                      className="h-full bg-primary"
                      initial={{ width: "0%" }}
                      animate={{ width: `${Math.random() * 60 + 40}%` }}
                      transition={{ duration: 2, repeat: Infinity, repeatType: "reverse" }}
                    />
                  </div>
                </motion.div>
              ))}
            </div>
            
            <div className="mt-8 p-4 border border-dashed border-primary/30 bg-primary/5 rounded">
              <div className="flex items-start gap-4">
                <Shield className="w-8 h-8 text-primary shrink-0" />
                <div>
                  <h4 className="font-bold text-primary mb-1">SECURITY NOTICE</h4>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    Unverified quantum fluctuations detected in Sector 7G. Recommended action: 
                    Review Hyper-Axiomatic Equations for stability variances.
                  </p>
                </div>
              </div>
            </div>
          </CyberCard>
        </div>

        {/* Side Panel */}
        <div className="space-y-6">
          <CyberCard title="System Resources" className="h-full">
            <div className="flex flex-col gap-6 h-full justify-center">
              <ResourceGauge label="CPU CORE 01" value={78} />
              <ResourceGauge label="CPU CORE 02" value={45} />
              <ResourceGauge label="MEMORY ALLOC" value={62} />
              <ResourceGauge label="NETWORK I/O" value={23} />
            </div>
          </CyberCard>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon: Icon, label, value, color, trend }: any) {
  return (
    <CyberCard className="bg-black/60">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-mono text-muted-foreground uppercase tracking-widest">{label}</p>
          <h3 className={`text-2xl font-display font-bold mt-2 ${color} text-glow`}>{value}</h3>
        </div>
        <div className={`p-2 rounded bg-white/5 border border-white/10 ${color}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>
      {trend && (
        <div className="mt-4 flex items-center gap-2 text-xs font-mono">
          <span className={trend.startsWith('+') ? 'text-green-500' : 'text-red-500'}>
            {trend}
          </span>
          <span className="text-muted-foreground">vs last cycle</span>
        </div>
      )}
    </CyberCard>
  );
}

function ResourceGauge({ label, value }: { label: string, value: number }) {
  return (
    <div className="space-y-2">
      <div className="flex justify-between text-xs font-mono text-primary/80">
        <span>{label}</span>
        <span>{value}%</span>
      </div>
      <div className="h-2 bg-white/10 w-full overflow-hidden skew-x-[-20deg]">
        <motion.div 
          className="h-full bg-gradient-to-r from-primary to-secondary"
          initial={{ width: 0 }}
          animate={{ width: `${value}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
        />
      </div>
    </div>
  );
}
