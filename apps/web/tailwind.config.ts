import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/features/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        // Mastercard-Inspired Warm Editorial Palette
        canvas: {
          DEFAULT: "#F3F0EE", // Warm Canvas Cream
          lifted: "#FCFBFA",  // Lifted Cream (paper-on-paper)
          bone: "#F4F4F4",    // Soft Bone subregion
          muted: "#E8E2DA",   // Ghost watermark cream
        },
        ink: {
          DEFAULT: "#141413", // Primary Ink Black (warm near-black)
          charcoal: "#262627",
          granite: "#555555",
          graphite: "#565656",
          slate: "#696969",   // Muted slate gray
          taupe: "#D1CDC7",   // Whisper dust taupe
        },
        signal: {
          orange: "#CF4500", // Signal Orange (legal / consent / deficit actions)
          light: "#F37338",  // Light Signal Orange (orbital arcs & trajectory cues)
          clay: "#9A3A0A",   // Clay Brown (secondary rust link buttons)
        },
        link: {
          blue: "#3860BE",   // Deep Link Blue
        },
        // Semantic Regulatory Adjudication Tokens
        verdict: {
          compliant: {
            DEFAULT: "#065f46", // Deep Emerald
            text: "#065f46",
            bg: "#EBF7F2",      // Soft sage-cream tint
            border: "#A7F3D0",
            dot: "#10b981",
          },
          noncompliant: {
            DEFAULT: "#CF4500", // Signal Orange / Deficit Rust
            text: "#9A3400",
            bg: "#FFF1EB",      // Warm tinted peach
            border: "#FFC2A8",
            dot: "#CF4500",
          },
          review: {
            DEFAULT: "#9A3A0A", // Clay Brown / Amber Review
            text: "#9A3A0A",
            bg: "#FFF8EB",
            border: "#FDE68A",
            dot: "#D97706",
          },
          inconclusive: {
            DEFAULT: "#555555", // Granite Inconclusive
            text: "#333333",
            bg: "#ECE9E4",
            border: "#D1CDC7",
            dot: "#696969",
          },
          exemption: {
            DEFAULT: "#3860BE", // Link Blue Exemption
            text: "#2A4B99",
            bg: "#EDF2FF",
            border: "#BFDBFE",
            dot: "#3860BE",
          },
        },
      },
      borderRadius: {
        cta: "20px",       // Mastercard Signature Primary & Secondary Button Radius
        consent: "24px",   // Signal Orange Pill Radius
        stadium: "40px",   // Iconic 40pt Stadium Container & Hero Radius
        pill: "999px",     // Floating Nav Pill & Carousel Cards
      },
      boxShadow: {
        lift: "0px 4px 24px 0px rgba(0, 0, 0, 0.04)",    // Level 1: Floating Nav Pill
        halo: "0px 24px 48px 0px rgba(0, 0, 0, 0.08)",   // Level 2: Stadium Media & Cards
        deep: "0px 70px 110px 0px rgba(0, 0, 0, 0.18)",  // Level 3: Dramatic Elevation
      },
      letterSpacing: {
        headline: "-0.02em", // Mastercard -2% negative tracking on headlines
        eyebrow: "0.04em",   // Mastercard +4% uppercase tracking on eyebrows
        tightest: "-0.03em",
      },
      fontFamily: {
        sans: [
          "var(--font-sofia)",
          "Sofia Sans",
          "Inter",
          "-apple-system",
          "BlinkMacSystemFont",
          "sans-serif",
        ],
        mono: [
          "JetBrains Mono",
          "ui-monospace",
          "monospace",
        ],
      },
    },
  },
  plugins: [],
};

export default config;
