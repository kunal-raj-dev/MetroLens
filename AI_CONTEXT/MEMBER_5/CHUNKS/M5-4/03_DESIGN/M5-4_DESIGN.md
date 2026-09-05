# METROLENS AI — MEMBER 5 (CHUNK M5-4)
## Design System Tokens & UI Specifications

### 1. Visual Philosophy & Token Architecture
Following the M5-1 foundation, M5-4 enforces an editorial, sovereign magazine aesthetic influenced by high-trust design standards (Mastercard-inspired extreme pill radii, high-contrast typography, and purposeful state indicators).

#### Design Tokens Used:
- **Pill Badges (`rounded-pill`)**: Used for statutory tags (`RULE 6 PASS`, `RULE DEFICIT`, `MANUAL REVIEW`).
- **Stadium Containers (`rounded-stadium` / `40px` radius)**: Used for the primary workstation cards, modals, and preview zones.
- **Signal Colors**:
  - `signal-orange` (`#EA580C`): Primary action accent, selected token highlight.
  - `emerald-600` / `emerald-700`: Compliant / Confirmed states.
  - `red-600` / `red-700`: Deficit / Flagged states.
  - `amber-500`: Suspect review & Synthetic Demo indicators.
  - `blue-600` (`#2563EB`): Multi-token declaration linking outlines on canvas.
  - `indigo-600`: Manual Two-Point Reference Caliper tool active state.

### 2. Declaration Table Responsive Layout
- **Desktop View (>= 768px)**:
  - Clean semantic `<table>` with columns: Mandatory Field, Observed OCR Text, Legal Status, Confidence, Metric Numeral, Actions.
  - Horizontal scroll protection with subtle overflow indicators.
- **Mobile View (< 768px)**:
  - Responsive card stack (`space-y-3.5`).
  - Each declaration rendered as an individual inspection card with stacked field title, observed text code snippet, verdict badge, and full-width action buttons.

### 3. Accessibility & Keyboard Navigation (WCAG 2.1 AA)
- Full keyboard support: Table rows navigable via Arrow keys; actions focusable and triggerable via Enter/Space.
- Modal adheres to WAI-ARIA `dialog` pattern: focus trap, Escape key to close, `aria-modal="true"`, and return focus to previous trigger button.
- Live announcements via `aria-live="polite"` on review submission and status updates.
- Minimum 44x44px touch targets on all interactive controls.
