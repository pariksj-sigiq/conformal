"use client";

type DuckDbModule = {
  DuckDBStore?: unknown;
  duckDBStore?: unknown;
  default?: unknown;
  tablesReferencedBy?: (sql: string) => string[];
};

export type DuckDbApi = {
  runSql: (sql: string) => Promise<Record<string, unknown>[]>;
  subscribe?: (tables: string[], onMutation: () => void) => (() => void) | { unsubscribe: () => void };
  tablesReferencedBy?: (sql: string) => string[];
};

type StoreCandidate = Partial<DuckDbApi> & {
  getInstance?: () => DuckDbApi;
  instance?: DuckDbApi;
  create?: () => Promise<DuckDbApi>;
  subscribe?: unknown;
};

let modulePromise: Promise<DuckDbModule | null> | null = null;

async function loadDuckDbModule() {
  if (!modulePromise) {
    modulePromise = import(`@/lib/${"duckdb-store"}`)
      .then((mod) => mod as DuckDbModule)
      .catch(() => null);
  }

  return modulePromise;
}

function resolveStore(candidate: unknown): DuckDbApi | null {
  if (!candidate || typeof candidate !== "object") return null;

  const store = candidate as StoreCandidate;
  if (typeof store.runSql === "function") return normalizeStore(store as DuckDbApi);
  if (typeof store.getInstance === "function") return normalizeStore(store.getInstance());
  if (store.instance && typeof store.instance.runSql === "function") return normalizeStore(store.instance);

  try {
    const Constructable = candidate as new () => DuckDbApi;
    const instance = new Constructable();
    return typeof instance.runSql === "function" ? normalizeStore(instance) : null;
  } catch {
    return null;
  }
}

function normalizeStore(store: DuckDbApi): DuckDbApi {
  return {
    runSql: async (sql: string) => {
      const result = await store.runSql(sql);
      if (Array.isArray(result)) return result;

      const maybeResult = result as unknown as { rows?: Record<string, unknown>[] };
      return Array.isArray(maybeResult.rows) ? maybeResult.rows : [];
    },
    tablesReferencedBy:
      typeof store.tablesReferencedBy === "function" ? (sql: string) => store.tablesReferencedBy?.(sql) ?? [] : undefined,
    subscribe:
      typeof store.subscribe === "function"
        ? (tables, onMutation) => {
            const rawSubscribe = store.subscribe as NonNullable<DuckDbApi["subscribe"]>;
            const subscribe = rawSubscribe.bind(store);
            if (rawSubscribe.length === 1) {
              return (subscribe as unknown as (listener: (event: { table?: string }) => void) => () => void)((event) => {
                if (!tables.length || !event.table || tables.includes(event.table)) onMutation();
              });
            }

            return subscribe(tables, onMutation) ?? (() => undefined);
          }
        : undefined,
  };
}

export async function getDuckDbStore(): Promise<DuckDbApi | null> {
  const mod = await loadDuckDbModule();
  if (!mod) return null;

  return (
    resolveStore(mod.DuckDBStore) ??
    resolveStore(mod.duckDBStore) ??
    resolveStore(mod.default) ??
    null
  );
}

export async function tablesForSql(sql: string): Promise<string[]> {
  const [mod, store] = await Promise.all([loadDuckDbModule(), getDuckDbStore()]);
  if (store?.tablesReferencedBy) return store.tablesReferencedBy(sql);
  if (mod?.tablesReferencedBy) return mod.tablesReferencedBy(sql);

  const matches = sql.matchAll(/\b(?:from|join)\s+["`[]?([a-zA-Z0-9_.-]+)/gi);
  return Array.from(new Set(Array.from(matches, (match) => match[1])));
}

export function rowsToCsv(rows: Record<string, unknown>[]) {
  if (!rows.length) return "";

  const columns = Object.keys(rows[0]);
  const escape = (value: unknown) => {
    if (value == null) return "";
    const text = String(value);
    return /[",\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
  };

  return [columns.join(","), ...rows.map((row) => columns.map((column) => escape(row[column])).join(","))].join("\n");
}
