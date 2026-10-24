import { Switch, Route } from "wouter";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/not-found";
import IDE from "@/pages/IDE";
import { FileSystemProvider } from "./contexts/FileSystemContext";
import { EditorProvider } from "./contexts/EditorContext";
import { TerminalProvider } from "./contexts/TerminalContext";
import { AIProvider } from "./contexts/AIContext";

function Router() {
  return (
    <Switch>
      <Route path="/" component={IDE}/>
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <FileSystemProvider>
          <EditorProvider>
            <TerminalProvider>
              <AIProvider>
                <Toaster />
                <Router />
              </AIProvider>
            </TerminalProvider>
          </EditorProvider>
        </FileSystemProvider>
      </TooltipProvider>
    </QueryClientProvider>
  );
}

export default App;
