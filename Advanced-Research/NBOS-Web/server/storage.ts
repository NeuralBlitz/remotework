import { db } from "./db";
import {
  equations,
  type InsertEquation,
  type Equation
} from "@shared/schema";
import { eq, ilike } from "drizzle-orm";

export interface IStorage {
  getEquations(search?: string): Promise<Equation[]>;
  getEquation(id: number): Promise<Equation | undefined>;
  createEquation(equation: InsertEquation): Promise<Equation>;
}

export class DatabaseStorage implements IStorage {
  async getEquations(search?: string): Promise<Equation[]> {
    if (search) {
      return await db.select().from(equations).where(ilike(equations.title, `%${search}%`));
    }
    return await db.select().from(equations);
  }

  async getEquation(id: number): Promise<Equation | undefined> {
    const [equation] = await db.select().from(equations).where(eq(equations.id, id));
    return equation;
  }

  async createEquation(insertEquation: InsertEquation): Promise<Equation> {
    const [equation] = await db.insert(equations).values(insertEquation).returning();
    return equation;
  }
}

export const storage = new DatabaseStorage();
