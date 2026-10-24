import { z } from 'zod';
import { insertEquationSchema, equations } from './schema';

// ============================================
// SHARED ERROR SCHEMAS
// ============================================
export const errorSchemas = {
  validation: z.object({
    message: z.string(),
    field: z.string().optional(),
  }),
  notFound: z.object({
    message: z.string(),
  }),
  internal: z.object({
    message: z.string(),
  }),
};

// ============================================
// API CONTRACT
// ============================================
export const api = {
  equations: {
    list: {
      method: 'GET' as const,
      path: '/api/equations',
      input: z.object({
        search: z.string().optional(),
      }).optional(),
      responses: {
        200: z.array(z.custom<typeof equations.$inferSelect>()),
      },
    },
    get: {
      method: 'GET' as const,
      path: '/api/equations/:id',
      responses: {
        200: z.custom<typeof equations.$inferSelect>(),
        404: errorSchemas.notFound,
      },
    },
    // Simulation endpoint to "run" a genesis cycle (mocked)
    simulate: {
      method: 'POST' as const,
      path: '/api/simulation/genesis',
      responses: {
        200: z.object({
          status: z.string(),
          traceId: z.string(),
          logs: z.array(z.string())
        })
      }
    }
  },
};

// ============================================
// HELPER
// ============================================
export function buildUrl(path: string, params?: Record<string, string | number>): string {
  let url = path;
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (url.includes(`:${key}`)) {
        url = url.replace(`:${key}`, String(value));
      }
    });
  }
  return url;
}

export type EquationResponse = z.infer<typeof api.equations.get.responses[200]>;
