import type { Metadata } from "next";
import { JournalChrome, Divider } from "@/components/journal/JournalChrome";
import { JournalIndex } from "@/components/journal/JournalIndex";

export const metadata: Metadata = {
  title: "Journal",
  description: "Notes from production AI engagements, anonymized. Written by the people shipping the code.",
  alternates: {
    canonical: "/journal",
    types: {
      "application/rss+xml": "/journal/rss.xml",
    },
  },
  openGraph: {
    title: "Conformal Journal",
    description: "Notes from production AI engagements, anonymized.",
    url: "https://conformal.live/journal",
    siteName: "Conformal",
    type: "website",
  },
};

export default function JournalPage() {
  return (
    <JournalChrome>
      <section className="px-6 py-14 md:px-9 md:py-20">
        <Divider>Journal</Divider>
        <h1 className="conformal-display mb-6 max-w-[880px] font-serif text-[44px] font-normal leading-[1.08] tracking-normal text-[color:var(--foreground)] md:text-[54px]">
          Notes from production engagements, <em className="italic text-[#B8232E]">anonymized.</em>
        </h1>
        <p className="mb-6 max-w-[660px] text-base leading-[1.75] text-[color:var(--muted)]">
          Written by Conformal Engineering and the partners doing the work. We publish when an engagement teaches something reusable: architecture patterns, evals, field notes, hiring practices, and strategy that survives contact with production.
        </p>
        <div className="flex flex-wrap gap-4">
          <a className="text-[13px] text-[color:var(--foreground)] underline decoration-[color:var(--line)] underline-offset-4 hover:text-[#B8232E]" href="/journal/rss.xml">RSS</a>
          <a className="text-[13px] text-[color:var(--foreground)] underline decoration-[color:var(--line)] underline-offset-4 hover:text-[#B8232E]" href="mailto:hello@conformal.live?subject=Email%20me%20when%20Conformal%20publishes">Email when we publish</a>
        </div>
      </section>
      <JournalIndex />
    </JournalChrome>
  );
}
