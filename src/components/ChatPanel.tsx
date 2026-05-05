"use client";

import { Bot, ChevronDown, CornerDownLeft, Loader2, Send, UserRound, Wrench } from "lucide-react";
import { FormEvent, useMemo, useState } from "react";
import { motion } from "motion/react";
import { cn } from "@/lib/utils";
import { LiveChart } from "./LiveChart";
import type { ChartBundle, ChatMessage, TraceEvent } from "./types";

type ChatPanelProps = {
  live: boolean;
  pinnedIds: Set<string>;
  onPinChart: (chart: ChartBundle) => void;
};

const starters = [
  "How is the field force tracking this quarter?",
  "Show me procurement savings vs target by category.",
  "What's happening with farmer NPS across regions?",
  "Status of Wave 1 micro-battles.",
  "Channel partners at churn risk in North zone.",
  "What's moving in commodity markets today?",
];

export function ChatPanel({ live, pinnedIds, onPinChart }: ChatPanelProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome",
      role: "assistant",
      content: "Ask for a KPI, variance, segment deep dive, or operating risk. I will show my tool trace and keep charts live when the data tables move.",
      createdAt: Date.now(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);

  const activeCharts = useMemo(() => messages.flatMap((message) => message.charts ?? []), [messages]);

  async function submitPrompt(event?: FormEvent, override?: string) {
    event?.preventDefault();
    const prompt = (override ?? input).trim();
    if (!prompt || isSending) return;

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: prompt,
      createdAt: Date.now(),
    };
    const assistantId = crypto.randomUUID();
    const assistantMessage: ChatMessage = {
      id: assistantId,
      role: "assistant",
      content: "",
      trace: [],
      charts: [],
      createdAt: Date.now(),
    };

    setMessages((current) => [...current, userMessage, assistantMessage]);
    setInput("");
    setIsSending(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ question: prompt }),
      });

      if (!response.ok) throw new Error(`Chat failed with ${response.status}`);
      if (!response.body) throw new Error("Chat stream did not start.");

      await consumeNdjson(response.body, (eventData) => {
        setMessages((current) =>
          current.map((message) => (message.id === assistantId ? applyChatEvent(message, eventData) : message)),
        );
      });
    } catch (error) {
      setMessages((current) =>
        current.map((message) =>
          message.id === assistantId
            ? {
                ...message,
                content: error instanceof Error ? error.message : "The agent could not complete the request.",
                trace: [
                  ...(message.trace ?? []),
                  {
                    id: crypto.randomUUID(),
                    type: "error",
                    label: "Stream error",
                    status: "error",
                    detail: error instanceof Error ? error.message : "Unknown failure",
                    timestamp: Date.now(),
                  },
                ],
              }
            : message,
        ),
      );
    } finally {
      setIsSending(false);
    }
  }

  return (
    <div className="cockpit-workspace">
      <section className="chat-pane">
        <div className="pane-heading">
          <div>
            <span>Agent workspace</span>
            <h2>Executive prompt</h2>
          </div>
          <div className={cn("pulse-chip", isSending && "pulse-chip-active")}>
            {isSending ? <Loader2 size={14} className="animate-spin" /> : <CornerDownLeft size={14} />}
            NDJSON stream
          </div>
        </div>

        <div className="message-list">
          {messages.map((message) => (
            <motion.article
              layout
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className={cn("message", message.role === "user" && "message-user")}
              key={message.id}
            >
              <div className="message-avatar">{message.role === "user" ? <UserRound size={16} /> : <Bot size={16} />}</div>
              <div className="message-body">
                <p>{message.content || (isSending && message.role === "assistant" ? "Working through the data..." : "")}</p>
                {message.trace?.length ? <ToolTrace trace={message.trace} /> : null}
              </div>
            </motion.article>
          ))}
        </div>

        <div className="starter-row">
          {starters.map((starter) => (
            <button type="button" key={starter} onClick={() => submitPrompt(undefined, starter)}>
              {starter}
            </button>
          ))}
        </div>

        <form className="prompt-box" onSubmit={submitPrompt}>
          <textarea
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Ask the cockpit to investigate revenue, margin, inventory, or working-capital movement..."
            onKeyDown={(event) => {
              if (event.key === "Enter" && (event.metaKey || event.ctrlKey)) submitPrompt(event);
            }}
          />
          <button type="submit" disabled={!input.trim() || isSending} title="Send prompt">
            {isSending ? <Loader2 size={17} className="animate-spin" /> : <Send size={17} />}
          </button>
        </form>
      </section>

      <section className="canvas-pane">
        <div className="pane-heading">
          <div>
            <span>Chart canvas</span>
            <h2>Live analyses</h2>
          </div>
          <strong>{activeCharts.length} charts</strong>
        </div>

        <div className="chart-stack">
          {activeCharts.length ? (
            activeCharts.map((chart) => (
              <LiveChart key={chart.id} chart={chart} live={live} pinned={pinnedIds.has(chart.id)} onPin={onPinChart} />
            ))
          ) : (
            <div className="empty-canvas">
              <span>Charts generated by the agent will appear here.</span>
              <small>Each chart can be pinned to the dashboard, copied as SQL or CSV, and refreshed when source tables mutate.</small>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

function ToolTrace({ trace }: { trace: TraceEvent[] }) {
  const [open, setOpen] = useState(true);

  return (
    <div className="tool-trace">
      <button type="button" onClick={() => setOpen((current) => !current)}>
        <Wrench size={14} />
        Tool trace
        <ChevronDown size={14} className={cn(open && "rotate-180")} />
      </button>
      {open ? (
        <div className="trace-items">
          {trace.map((item, index) => (
            <details key={`${item.id}-${item.type}-${index}`} open={item.status === "error"}>
              <summary>
                <span data-status={item.status ?? "complete"} />
                {item.label}
              </summary>
              {item.detail ? <p>{item.detail}</p> : null}
              {item.payload ? <pre>{JSON.stringify(item.payload, null, 2)}</pre> : null}
            </details>
          ))}
        </div>
      ) : null}
    </div>
  );
}

async function consumeNdjson(stream: ReadableStream<Uint8Array>, onEvent: (eventData: Record<string, unknown>) => void) {
  const reader = stream.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";

    for (const line of lines) {
      const text = line.trim();
      if (!text) continue;
      onEvent(JSON.parse(text));
    }
  }

  const final = buffer.trim();
  if (final) onEvent(JSON.parse(final));
}

function applyChatEvent(message: ChatMessage, eventData: Record<string, unknown>): ChatMessage {
  const type = String(eventData.type ?? eventData.event ?? "trace");

  if (type === "chart" || eventData.chart || eventData.chartBundle) {
    const rawChart = (eventData.chart ?? eventData.chartBundle ?? eventData) as Partial<ChartBundle>;
    const chart: ChartBundle = {
      id: rawChart.id ?? crypto.randomUUID(),
      title: rawChart.title ?? "Generated analysis",
      sql: rawChart.sql ?? "select 1 as value",
      description: rawChart.description ?? (rawChart as { narrative?: string }).narrative,
      spec: rawChart.spec,
      generatedAt: Date.now(),
    };

    return { ...message, charts: [...(message.charts ?? []), chart] };
  }

  if (type === "final" || type === "message" || type === "narrative") {
    const content = String(eventData.content ?? eventData.text ?? eventData.narrative ?? eventData.answer ?? "");
    return { ...message, content: [message.content, content].filter(Boolean).join(message.content ? "\n\n" : "") };
  }

  const trace: TraceEvent = {
    id: String(eventData.id ?? crypto.randomUUID()),
    type,
    label: String(eventData.label ?? eventData.name ?? eventData.tool ?? type),
    status: (eventData.status as TraceEvent["status"]) ?? "complete",
    detail: eventData.detail
      ? String(eventData.detail)
      : eventData.message
        ? String(eventData.message)
        : (eventData.output as { summary?: string } | undefined)?.summary,
    payload: eventData.payload ?? eventData.data ?? eventData.input ?? eventData.output,
    timestamp: Date.now(),
  };

  return { ...message, trace: [...(message.trace ?? []), trace] };
}
