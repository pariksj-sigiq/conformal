import { scriptedEvents } from "@/lib/hero-queries";

export function runChatEngine(message: string) {
  return scriptedEvents(message);
}
