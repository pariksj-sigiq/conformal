"use client";

import Link from "next/link";
import { BarChart3 } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { cn } from "@/lib/utils";
import { DuckDBStore } from "@/lib/duckdb-store";
import { ChatPanel } from "./ChatPanel";
import type { ChartBundle } from "./types";

const PINNED_CHARTS_KEY = "project-leap-pinned-charts";

export function CockpitShell() {
  const [live, setLive] = useState(true);
  const [pinnedCharts, setPinnedCharts] = usePinnedCharts();

  useEffect(() => {
    if (!live) return;

    const tables = [
      "secondary_sales",
      "field_force_activity",
      "channel_partners",
      "farmer_engagement",
      "procurement_spend",
      "wave1_microbattles",
      "commodity_prices",
      "farmer_nps",
    ];
    let index = 0;
    const timer = window.setInterval(() => {
      DuckDBStore.mutate(tables[index % tables.length]);
      DuckDBStore.mutate(tables[(index + 3) % tables.length]);
      index += 1;
    }, 4200);

    return () => window.clearInterval(timer);
  }, [live]);

  const pinnedIds = useMemo(() => new Set(pinnedCharts.map((chart) => chart.id)), [pinnedCharts]);

  const togglePin = (chart: ChartBundle) => {
    setPinnedCharts((current) => {
      if (current.some((item) => item.id === chart.id)) return current.filter((item) => item.id !== chart.id);
      return [{ ...chart, generatedAt: chart.generatedAt ?? Date.now() }, ...current];
    });
  };

  return (
    <main className="app-shell">
      <aside className="sfs-sidebar">
        <div>
          <div className="sfs-mark">SFS</div>
          <div className="project-label">Project Leap</div>
        </div>

        <nav className="sidebar-nav" aria-label="Primary">
          <a href="#" className="active">
            Chat
          </a>
          <Link href="/dashboard">
            Dashboard
          </Link>
        </nav>

        <section className="sidebar-section">
          <h2>Conversations</h2>
          <a className="conversation active" href="#">
            <strong>Field force Q3</strong>
            <span>2 mins ago</span>
          </a>
          <a className="conversation" href="#">
            <strong>Procurement</strong>
            <span>Yesterday</span>
          </a>
          <a className="conversation" href="#">
            <strong>Farmer NPS</strong>
            <span>Mon</span>
          </a>
        </section>

        <section className="sidebar-section sidebar-pinned">
          <h2>Pinned</h2>
          <Link href="/dashboard" className="pinned-link">
            <BarChart3 size={15} />
            <span>Main dashboard</span>
          </Link>
        </section>
      </aside>

      <div className="app-main">
        <header className="top-bar">
          <div className="breadcrumb">
            <strong>Executive Cockpit</strong>
            <span>/</span>
            <em>Shriram Farm Solutions</em>
          </div>

          <div className="top-actions">
            <button type="button" className={cn("live-toggle", live && "live-toggle-on")} onClick={() => setLive((current) => !current)}>
              <span />
              Live
            </button>
            <div className="top-divider" />
            <div className="avatar">AK</div>
          </div>
        </header>

        <ChatPanel live={live} pinnedIds={pinnedIds} onPinChart={togglePin} />
      </div>
    </main>
  );
}

export function usePinnedCharts() {
  const [charts, setCharts] = useState<ChartBundle[]>([]);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    queueMicrotask(() => {
      try {
        const raw = localStorage.getItem(PINNED_CHARTS_KEY);
        setCharts(raw ? (JSON.parse(raw) as ChartBundle[]) : []);
      } catch {
        setCharts([]);
      } finally {
        setHydrated(true);
      }
    });
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    localStorage.setItem(PINNED_CHARTS_KEY, JSON.stringify(charts));
  }, [charts, hydrated]);

  return [charts, setCharts] as const;
}
