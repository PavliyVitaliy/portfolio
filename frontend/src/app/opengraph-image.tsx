import { ImageResponse } from "next/og";

export const alt = "Vitalii Pavlii — Senior Full-Stack Software Engineer";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OpenGraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          background: "#f8f7f3",
          color: "#1c1917",
          display: "flex",
          flexDirection: "column",
          height: "100%",
          justifyContent: "space-between",
          padding: "72px",
          width: "100%",
        }}
      >
        <div style={{ alignItems: "center", display: "flex", gap: "20px" }}>
          <div
            style={{
              alignItems: "center",
              background: "#1c1917",
              borderRadius: "50%",
              color: "#f8f7f3",
              display: "flex",
              fontFamily: "serif",
              fontSize: 28,
              fontWeight: 700,
              height: "64px",
              justifyContent: "center",
              width: "64px",
            }}
          >
            VP
          </div>
          <span style={{ fontSize: 28, fontWeight: 600, letterSpacing: "0.04em" }}>PORTFOLIO</span>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
          <span style={{ color: "#075985", fontSize: 22, fontWeight: 700, letterSpacing: "0.2em" }}>
            INDEPENDENT SOFTWARE ENGINEER
          </span>
          <span style={{ fontFamily: "serif", fontSize: 76, fontWeight: 700, letterSpacing: "-0.04em" }}>
            Vitalii Pavlii
          </span>
          <span style={{ color: "#57534e", fontSize: 30 }}>Senior Full-Stack Software Engineer</span>
        </div>
        <div style={{ borderTop: "2px solid #d6d3d1", display: "flex", justifyContent: "space-between", paddingTop: "24px" }}>
          <span style={{ color: "#57534e", fontSize: 22 }}>Reliable products, systems and delivery processes.</span>
          <span style={{ color: "#075985", fontSize: 22 }}>vitaliipavlii.com</span>
        </div>
      </div>
    ),
    size,
  );
}
