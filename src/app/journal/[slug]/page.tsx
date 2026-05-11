import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowRight } from "lucide-react";
import { JournalChrome } from "@/components/journal/JournalChrome";
import { formatPostDate, getPost, getRelatedPosts, posts } from "@/lib/journal";

type PostPageProps = {
  params: Promise<{ slug: string }>;
};

export function generateStaticParams() {
  return posts.map((post) => ({ slug: post.slug }));
}

export async function generateMetadata({ params }: PostPageProps): Promise<Metadata> {
  const { slug } = await params;
  const post = getPost(slug);

  if (!post) {
    return {};
  }

  return {
    title: post.title,
    description: post.dek,
    alternates: {
      canonical: `/journal/${post.slug}`,
    },
    openGraph: {
      title: post.title,
      description: post.dek,
      url: `https://conformal.live/journal/${post.slug}`,
      siteName: "Conformal",
      type: "article",
      publishedTime: post.publishedAt,
      authors: ["Conformal Engineering"],
      images: [
        {
          url: `https://conformal.live/journal/${post.slug}/opengraph-image`,
          width: 1200,
          height: 630,
          alt: post.title,
        },
      ],
    },
  };
}

export default async function JournalPostPage({ params }: PostPageProps) {
  const { slug } = await params;
  const post = getPost(slug);

  if (!post) {
    notFound();
  }

  const relatedPosts = getRelatedPosts(post.slug);

  return (
    <JournalChrome>
      <article className="mx-auto max-w-[760px] px-6 py-14 md:px-9 md:py-20">
        <p className="mb-4 text-[11px] font-medium uppercase tracking-[0.14em] text-[#B8232E]">{post.category}</p>
        <h1 className="conformal-display mb-5 font-serif text-[42px] font-normal leading-[1.08] tracking-normal text-[color:var(--foreground)] md:text-[54px]">
          {post.title}
        </h1>
        <p className="mb-4 text-lg leading-[1.65] text-[color:var(--muted)]">{post.dek}</p>
        <p className="mb-12 border-b border-[color:var(--line)] pb-6 text-[12px] font-medium uppercase tracking-[0.12em] text-[color:var(--muted)]">
          Conformal Engineering · {formatPostDate(post.publishedAt)} · {post.readTime} read
        </p>

        <div className="mx-auto max-w-[660px]">
          {post.sections.map((section, index) => (
            <section key={section.heading ?? `intro-${index}`} className="mb-9 last:mb-0">
              {section.heading ? (
                <h2 className="mb-4 font-serif text-[30px] font-normal leading-[1.18] tracking-normal text-[color:var(--foreground)]">{section.heading}</h2>
              ) : null}
              {section.paragraphs.map((paragraph) => (
                <p key={paragraph} className="mb-5 text-[17px] leading-[1.75] text-[color:var(--foreground)] last:mb-0">
                  {paragraph}
                </p>
              ))}
            </section>
          ))}
        </div>
      </article>

      <section className="border-t border-[color:var(--line)] px-6 py-12 md:px-9">
        <div className="mx-auto max-w-[760px]">
          <p className="mb-6 text-[11px] font-medium uppercase tracking-[0.14em] text-[color:var(--muted)]">More from the Journal</p>
          <div className="grid gap-5 md:grid-cols-3">
            {relatedPosts.map((related) => (
              <Link key={related.slug} className="group text-[color:var(--foreground)] no-underline" href={`/journal/${related.slug}`}>
                <p className="mb-2 text-[11px] font-medium uppercase tracking-[0.12em] text-[#B8232E]">{related.category}</p>
                <h3 className="mb-2 font-serif text-xl font-normal leading-[1.25] group-hover:text-[#B8232E]">{related.title}</h3>
                <p className="inline-flex items-center gap-1 text-[12px] text-[color:var(--muted)]">
                  Read next <ArrowRight size={13} aria-hidden="true" />
                </p>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </JournalChrome>
  );
}
