import { pgTable, text, serial, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

// === TABLE DEFINITIONS ===
export const equations = pgTable("equations", {
  id: serial("id").primaryKey(),
  title: text("title").notNull(),
  code: text("code").notNull(), // e.g., NBQ_OCT
  concept: text("concept").notNull(),
  latex: text("latex").notNull(),
  deconstruction: text("deconstruction").notNull(),
  category: text("category").default("General").notNull(),
  createdAt: timestamp("created_at").defaultNow(),
});

// === BASE SCHEMAS ===
export const insertEquationSchema = createInsertSchema(equations).omit({ id: true, createdAt: true });

// === EXPLICIT API CONTRACT TYPES ===
export type Equation = typeof equations.$inferSelect;
export type InsertEquation = z.infer<typeof insertEquationSchema>;

export type EquationResponse = Equation;
export type EquationListResponse = Equation[];

export interface EquationsQueryParams {
  search?: string;
}
