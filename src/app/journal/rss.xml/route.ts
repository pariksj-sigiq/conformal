import { escapeXml, posts } from "@/lib/journal";

const siteUrl = "https://conformal.live";

export function GET() {
  const items = posts
    .map((post) => {
      const url = `${siteUrl}/journal/${post.slug}`;
      return `
        <item>
          <title>${escapeXml(post.title)}</title>
          <link>${url}</link>
          <guid isPermaLink="true">${url}</guid>
          <description>${escapeXml(post.dek)}</description>
          <category>${escapeXml(post.category)}</category>
          <pubDate>${new Date(`${post.publishedAt}T00:00:00.000Z`).toUTCString()}</pubDate>
        </item>`;
    })
    .join("");

  const feed = `<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
      <channel>
        <title>Conformal Journal</title>
        <link>${siteUrl}/journal</link>
        <atom:link href="${siteUrl}/journal/rss.xml" rel="self" type="application/rss+xml" />
        <description>Notes from production AI engagements, anonymized.</description>
        <language>en-IN</language>
        <lastBuildDate>${new Date(`${posts[0].publishedAt}T00:00:00.000Z`).toUTCString()}</lastBuildDate>
        ${items}
      </channel>
    </rss>`;

  return new Response(feed, {
    headers: {
      "Content-Type": "application/rss+xml; charset=utf-8",
    },
  });
}
