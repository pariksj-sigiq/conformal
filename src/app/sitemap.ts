import type { MetadataRoute } from "next";
import { posts } from "@/lib/journal";

export default function sitemap(): MetadataRoute.Sitemap {
  const baseRoutes: MetadataRoute.Sitemap = [
    {
      url: "https://conformal.live/",
      lastModified: new Date("2026-05-11"),
      changeFrequency: "monthly",
      priority: 1,
    },
    {
      url: "https://conformal.live/journal",
      lastModified: new Date(posts[0].publishedAt),
      changeFrequency: "weekly",
      priority: 0.8,
    },
  ];

  return [
    ...baseRoutes,
    ...posts.map((post) => ({
      url: `https://conformal.live/journal/${post.slug}`,
      lastModified: new Date(post.publishedAt),
      changeFrequency: "monthly" as const,
      priority: 0.7,
    })),
  ];
}
