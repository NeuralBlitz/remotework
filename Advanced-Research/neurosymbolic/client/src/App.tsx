import { Switch, Route } from "wouter";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/not-found";
import Dashboard from "@/pages/dashboard";
import RepoStructure from "@/pages/repo";
import EpistemicLog from "@/pages/epistemic";
import DataProvenance from "@/pages/data";
import GovernanceConfig from "@/pages/settings";
import Playground from "@/pages/playground";
import EthicsCharter from "@/pages/charter";
import CausalReasoning from "@/pages/causal";
import SynergyEngine from "@/pages/synergy";
import RiskHeatmap from "@/pages/heatmap";
import PolicySimulator from "@/pages/simulator";
import DiscoveryEngine from "@/pages/discovery";
import LineageVisualizer from "@/pages/lineage";
import AuditVault from "@/pages/audit";

function Router() {
  return (
    <Switch>
      <Route path="/" component={Dashboard} />
      <Route path="/discovery" component={DiscoveryEngine} />
      <Route path="/heatmap" component={RiskHeatmap} />
      <Route path="/playground" component={Playground} />
      <Route path="/simulator" component={PolicySimulator} />
      <Route path="/causal" component={CausalReasoning} />
      <Route path="/lineage" component={LineageVisualizer} />
      <Route path="/audit" component={AuditVault} />
      <Route path="/repo" component={RepoStructure} />
      <Route path="/synergy" component={SynergyEngine} />
      <Route path="/charter" component={EthicsCharter} />
      <Route path="/epistemic" component={EpistemicLog} />
      <Route path="/data" component={DataProvenance} />
      <Route path="/settings" component={GovernanceConfig} />
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Router />
      </TooltipProvider>
    </QueryClientProvider>
  );
}

export default App;
