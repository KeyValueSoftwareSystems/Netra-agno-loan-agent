import * as fs from "fs";
import type { Database } from "../schema/db.js";

let db: Database | null = null;

export function initDb(): void {
  const dbText = fs.readFileSync("./src/db/db.json", "utf-8");

  db = JSON.parse(dbText) as Database;
}

export function getDb(): Database {
  if (db === null) {
    throw new Error(
      "You must call initDb() first before getting the database!",
    );
  }
  return db;
}
