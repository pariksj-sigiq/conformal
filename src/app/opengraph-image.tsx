import { ImageResponse } from "next/og";

export const alt = "Conformal";
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = "image/png";

export default function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          background: "#FAFAF8",
          color: "#0B0B0C",
          fontFamily: "Inter, Arial, sans-serif",
          padding: 68,
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            width: "100%",
            border: "1px solid rgba(0,0,0,0.08)",
            borderRadius: 28,
            background: "#FFFFFF",
            padding: 58,
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
          <div style={{ display: "flex", flexDirection: "column", gap: 20, maxWidth: 860 }}>
            <div
              style={{
                color: "rgba(11,11,12,0.56)",
                fontSize: 20,
                letterSpacing: "0.14em",
                textTransform: "uppercase",
              }}
            >
              AI transformation for enterprise leaders
            </div>
            <div style={{ display: "flex", flexWrap: "wrap", fontSize: 76, lineHeight: 1.04, letterSpacing: "-0.01em" }}>
              In working&nbsp;
              <span style={{ color: "#B8232E", fontStyle: "italic" }}>code.</span>
            </div>
          </div>
          <div style={{ display: "flex", gap: 16, color: "rgba(11,11,12,0.58)", fontSize: 22 }}>
            <span>Six-week agents</span>
            <span>·</span>
            <span>Enterprise systems</span>
            <span>·</span>
            <span>Auditable traces</span>
          </div>
        </div>
      </div>
    ),
    size,
  );
}
