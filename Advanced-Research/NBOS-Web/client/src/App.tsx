import { Switch, Route } from "wouter";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { Navigation } from "@/components/Navigation";
import NotFound from "@/pages/not-found";
import Dashboard from "@/pages/Dashboard";
import EquationIndex from "@/pages/EquationIndex";
import EquationDetail from "@/pages/EquationDetail";
import Simulation from "@/pages/Simulation";

function Router() {
  return (
    <div className="flex min-h-screen bg-background text-foreground overflow-hidden">
      {/* Scanline overlay for retro effect */}
      <div className="scanline" />
      
      {/* Sidebar Navigation */}
      <Navigation />
      
      {/* Main Content Area */}
      <main className="flex-1 ml-20 md:ml-64 relative overflow-y-auto h-screen scroll-smooth">
        <div className="container mx-auto p-4 md:p-8 lg:p-12 pb-24 max-w-7xl">
          <Switch>
            <Route path="/" component={Dashboard} />
            <Route path="/equations" component={EquationIndex} />
            <Route path="/equations/:id" component={EquationDetail} />
            <Route path="/simulation" component={Simulation} />
            <Route component={NotFound} />
          </Switch>
        </div>
      </main>
    </div>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Toaster />
      <Router />
    </QueryClientProvider>
  );
}

export default App;
