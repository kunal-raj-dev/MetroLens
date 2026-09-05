# CURRENT STATE: MEMBER 5 — DEPENDENCIES
**Project:** MetroLens AI™ (SIH26034)  
**Package:** `apps/web/`  
**Last Updated:** 2026-09-05T18:25:00+05:30  
**Phase:** Chunk M5-5 (Complete)

---

## 1. Production Runtime Dependencies
| Package | Version | Purpose |
| :--- | :--- | :--- |
| `next` | `^14.2.5` | React App Router framework (SSR, standalone output, route handlers) |
| `react` | `^18.3.1` | Core UI library |
| `react-dom` | `^18.3.1` | DOM renderer for React |
| `lucide-react` | `^0.400.0` | Accessible, tree-shakeable UI & status icons |

---

## 2. Development Dependencies
| Package | Version | Purpose |
| :--- | :--- | :--- |
| `typescript` | `^5.5.3` | Type system and compile-time verification |
| `@types/node` | `^20.14.0` | Node.js TypeScript typings |
| `@types/react` | `^18.3.3` | React TypeScript typings |
| `@types/react-dom` | `^18.3.0` | React DOM TypeScript typings |
| `tailwindcss` | `^3.4.4` | Utility-first CSS framework with semantic token extension |
| `postcss` | `^8.4.39` | CSS transformation pipeline |
| `autoprefixer` | `^10.4.19` | Vendor prefix parser |

---

## 3. Architecture & Dependency Principles in Chunk M5-5
- **Zero Heavy PDF Client Libraries**: No client-side `jspdf`, `pdfmake`, or `canvas2pdf`. Reports are generated authoritatively by the backend service at `POST /api/v1/report/pdf`.
- **Zero Heavy Canvas Engines**: No `pixi.js`, `fabric.js`, or `konva`. The Evidence Canvas is built on native HTML5 Canvas 2D context with custom affine transformation math (`canvasTransform.ts`).
- **Zero External UI Bloat**: Clean hand-crafted design system based on Mastercard's tactile aesthetic (putty cream, stadium geometry, pill buttons, signal orange accents).

---

## 4. Node & Tooling Environment
- **Node.js**: `v25.6.1`
- **npm**: `11.9.0`
- **Platform**: Windows 11 AMD64
