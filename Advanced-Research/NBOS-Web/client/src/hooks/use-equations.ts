import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api, buildUrl } from "@shared/routes";
import { z } from "zod";

export function useEquations(search?: string) {
  return useQuery({
    queryKey: [api.equations.list.path, search],
    queryFn: async () => {
      const url = buildUrl(api.equations.list.path);
      const queryParams = search ? `?search=${encodeURIComponent(search)}` : "";
      const res = await fetch(url + queryParams, { credentials: "include" });
      if (!res.ok) throw new Error("Failed to fetch equations");
      return api.equations.list.responses[200].parse(await res.json());
    },
  });
}

export function useEquation(id: number) {
  return useQuery({
    queryKey: [api.equations.get.path, id],
    queryFn: async () => {
      const url = buildUrl(api.equations.get.path, { id });
      const res = await fetch(url, { credentials: "include" });
      if (res.status === 404) return null;
      if (!res.ok) throw new Error("Failed to fetch equation");
      return api.equations.get.responses[200].parse(await res.json());
    },
    enabled: !isNaN(id),
  });
}

export function useSimulateGenesis() {
  return useMutation({
    mutationFn: async () => {
      const res = await fetch(api.equations.simulate.path, {
        method: api.equations.simulate.method,
        credentials: "include",
      });
      if (!res.ok) throw new Error("Simulation failed initiation");
      return api.equations.simulate.responses[200].parse(await res.json());
    },
  });
}
