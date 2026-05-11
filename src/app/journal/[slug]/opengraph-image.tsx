import { ImageResponse } from "next/og";
import { getPost } from "@/lib/journal";

export const alt = "Conformal Journal";
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = "image/png";

export default async function Image({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = getPost(slug);
  const title = post?.title ?? "Conformal Journal";
  const category = post?.category ?? "Journal";

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          background: "#FAFAF8",
          color: "#0B0B0C",
          fontFamily: "Inter, Arial, sans-serif",
          padding: 72,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
          <div
            style={{
              width: 36,
              height: 36,
              borderRadius: 9,
              background: "#0E0E0E",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <div style={{ width: 15, height: 15, borderRadius: 999, background: "#FFFFFF" }} />
          </div>
          <div style={{ fontSize: 26, fontWeight: 500 }}>conformal</div>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 22, maxWidth: 930 }}>
          <div
            style={{
              color: "#B8232E",
              fontSize: 22,
              fontWeight: 500,
              letterSpacing: "0.14em",
              textTransform: "uppercase",
            }}
          >
            {category}
          </div>
          <div style={{ fontSize: 74, lineHeight: 1.04, letterSpacing: "-0.01em" }}>{title}</div>
        </div>
        <div style={{ color: "rgba(11,11,12,0.58)", fontSize: 22 }}>Journal · Production AI, anonymized</div>
      </div>
    ),
    size,
  );
}
