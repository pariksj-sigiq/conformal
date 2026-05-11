"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { formatPostDate, journalCategories, posts, type JournalCategory } from "@/lib/journal";

type Filter = (typeof journalCategories)[number];

function cx(...classes: Array<string | false | null | undefined>) {
  return classes.filter(Boolean).join(" ");
}

export function JournalIndex() {
  const [active, setActive] = useState<Filter>("All");
  const filteredPosts = useMemo(
    () => active === "All" ? posts : posts.filter((post) => post.category === (active as JournalCategory)),
    [active],
  );

  return (
    <>
      <div className="sticky top-0 z-10 border-y border-[color:var(--line)] bg-[color:var(--panel)]/95 px-6 py-3 backdrop-blur md:px-9">
        <div className="flex flex-wrap gap-2">
          {journalCategories.map((category) => (
            <button
              key={category}
              className={cx(
                "rounded-full border px-3 py-1.5 text-[12px] transition",
                active === category
                  ? "border-[#B8232E] bg-[#B8232E] text-white"
                  : "border-[color:var(--line)] bg-transparent text-[color:var(--muted)] hover:border-[#B8232E]/50 hover:text-[color:var(--foreground)]",
              )}
              type="button"
              onClick={() => setActive(category)}
            >
              {category}
            </button>
          ))}
        </div>
      </div>
      <section className="px-6 py-8 md:px-9 md:py-12">
        <div className="flex flex-col">
          {filteredPosts.map((post) => (
            <Link
              key={post.slug}
              className="grid gap-4 border-b border-[color:var(--line)] py-7 text-[color:var(--foreground)] no-underline last:border-b-0 md:grid-cols-[120px_minmax(0,1fr)_auto] md:gap-7"
              href={`/journal/${post.slug}`}
            >
              <div>
                <p className="mb-1 text-[11px] font-medium uppercase tracking-[0.14em] text-[color:var(--muted)]">{post.category}</p>
                <p className="m-0 text-[11px] text-[color:var(--muted)] opacity-80">{post.readTime} · {formatPostDate(post.publishedAt)}</p>
              </div>
              <div>
                <h2 className="mb-2 font-serif text-[24px] font-normal leading-[1.3] text-[color:var(--foreground)]">{post.title}</h2>
                <p className="m-0 max-w-[760px] text-sm leading-[1.7] text-[color:var(--muted)]">{post.dek}</p>
              </div>
              <ArrowUpRight className="hidden text-[color:var(--muted)] md:block" size={18} aria-hidden="true" />
            </Link>
          ))}
        </div>
        <p className="mt-8 text-center text-[12px] text-[color:var(--muted)]">You&apos;ve reached the end.</p>
      </section>
    </>
  );
}
