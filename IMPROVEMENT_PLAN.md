# Soundscape NYC — 10/10 Improvement Plan

## Current Score: 7/10
Solid foundation, clean design system, functional features. Better than 90% of small business rental sites. But not at the level of a premium agency product yet.

## Target: 10/10

---

## 1. HERO SECTION — Currently: 6/10

### Problems
- Dark gradient overlay on a photo = every Squarespace template ever. Zero originality.
- If the hero image doesn't load, you get a dark rectangle with white text — looks broken.
- No skeleton/placeholder while image loads.
- "Summer 2026 Collection" badge will be outdated in 3 months.
- Hero text is generic — "Experience Absolute Audio Power" could be any audio company.

### Fix
- [ ] **Lazy-load hero image with LQIP (Low-Quality Image Placeholder).** Generate a tiny base64 blur preview (10px wide, inline in CSS) that shows instantly, then crossfades to the full WebP.
- [ ] **Add `width`/`height` attributes or `aspect-ratio`** to the hero to prevent CLS (Cumulative Layout Shift).
- [ ] **Make the badge dynamic** — read from a config variable, not hardcoded. Or remove it entirely. "New Arrivals" or "2026 Season" is more evergreen.
- [ ] **Rewrite hero copy to be specific:**
  - Title: Something only Soundscape can say. "The Sound Behind NYC's Best Nights" or "65 Pieces. One Call. Zero Compromise."
  - Description: Replace generic copy with a riff on their actual differentiator — local NYC delivery, hand-tested gear, same-day availability.
- [ ] **Add a subtle cinematic effect** — a slow Ken Burns zoom on the hero image (CSS `animation: kenBurns 30s infinite alternate;` with `@keyframes kenBurns { from { transform: scale(1); } to { transform: scale(1.08); } }`).
- [ ] **Consider a hero video fallback** — a 5-second looping video (muted, autoplay, playsinline) of a real event would be transformative. A still photo can't compete with what competitors will do with video.
- [ ] **Add a scroll-down indicator** — a subtle animated chevron or arrow below the hero specs bar.

---

## 2. LOADING STATES — Currently: 2/10

### Problems
- JSON data fetches on `DOMContentLoaded` — there's a visible blank grid before items appear.
- No skeleton screens, no shimmer placeholders, no spinners.
- If the fetch fails, the error UI shows but there's no retry animation or auto-retry.
- Image loading has no progressive enhancement.

### Fix
- [ ] **Add skeleton placeholders** — render 8-12 gray shimmer cards in the gear grid before data loads. Each skeleton: gray rect for image area, gray line for title, gray line for description, gray line for price. Remove skeletons once `GEAR_CATALOG` is populated.
- [ ] **Add a skeleton for the packages grid** — 3-5 shimmer package cards.
- [ ] **Add `loading="lazy"` to all gear and package images** — prevents loading 70 images on initial page load.
- [ ] **Add `width` and `height` attributes to all images** (or `aspect-ratio` in CSS) — prevents layout shift when images load.
- [ ] **Progressive image loading** — load a tiny blur preview first, then swap to full image. Can be done with CSS `background-image` on the `.gear-visual` container + a blur filter that transitions to `blur(0)` when the `<img>` loads.
- [ ] **Add auto-retry to `loadData()`** — if fetch fails, retry up to 3 times with exponential backoff (1s, 3s, 9s). Show a subtle "Reconnecting..." toast instead of the error UI immediately.
- [ ] **Add a loading view to the cart drawer** — if someone opens the drawer before data loads, show a spinner instead of empty state.

---

## 3. PRODUCT IMAGES — Currently: 5/10

### Problems
- Mix of professional product shots (white bg), dark photos, and SVG fallback icons in the same grid. Visually inconsistent.
- `filter: drop-shadow(0 8px 16px rgba(0,0,0,0.6))` darkens every image indiscriminately — fine for product shots on white, terrible for dark photos.
- Placeholder SVG icons look like "under construction" flags.
- No hover zoom or detail view.

### Fix
- [ ] **Standardize image treatment** — all product images should be:
  - Shot on a consistent background (white or dark, pick one).
  - If white background: remove `drop-shadow` on light theme, use subtle `box-shadow` on the card instead.
  - If dark background: keep `drop-shadow` but remove the black overlay, use `object-fit: cover` with a consistent aspect ratio.
  - Decision: **light theme = white background images with no drop-shadow. Dark theme = dark background images with subtle glow.** Generate two versions or use CSS filters to adapt.
- [ ] **Replace all SVG fallback icons with styled placeholder cards** — instead of a tiny SVG in an empty box, show a styled card with the product name in large text, the category as a subtitle, and a subtle gradient background that matches the category color.
- [ ] **Add image hover effect** — slow zoom on hover (already exists but `scale(1.06)` is subtle). Increase to `1.1` and add a subtle brightness increase.
- [ ] **Add a lightbox/detail view** — clicking a gear card opens a modal with the full-size image, full description, stock info, and "Add to Quote" button. This is the #1 missing feature for a rental catalog.
- [ ] **Add category-specific accent colors** — backline = blue, speakers = orange, lighting = amber, etc. Use these as subtle accents on card borders or badges.

---

## 4. PACKAGES SECTION — Currently: 5/10

### Problems
- Package cards look identical to gear cards — same glass-panel treatment, same size. No visual hierarchy.
- "Best Value" ribbon at `9px` font with `transform: rotate(45deg)` is unreadable.
- The featured package doesn't dominate the row.
- Package features are just a list of text — no visual differentiation.
- No "What's included" expandable section or itemized breakdown.

### Fix
- [ ] **Make the featured package 2x the visual weight:**
  - Larger card (span 2 columns on desktop).
  - Larger image area (240px height vs 160px).
  - Bolder price typography.
  - Add a subtle animated border glow on hover.
- [ ] **Replace the "Best Value" ribbon with a badge pill** — `position: absolute; top: 12px; left: 12px;` with `background: var(--glow-orange); color: white; border-radius: 99px; padding: 4px 12px; font-size: 11px; font-weight: 700;`. Clean, scannable, readable.
- [ ] **Add visual hierarchy to package features** — bold the item name, regular weight the description. Currently it's `<strong>Pioneer RX3</strong> All-in-One Controller` which is fine, but in the rendered HTML the bold is subtle. Increase contrast: make the strong text `color: var(--text)` instead of inherited.
- [ ] **Add a "What's in this rig" expandable** — a collapsible section under each package that lists the exact gear items with quantities. Use the `rawItems` data that's already in the JSON. Show item names and quantities.
- [ ] **Add per-item imagery** — show tiny thumbnail icons of the included gear items at the bottom of each package card. Pull from the gear catalog's `image` field using the `rawItems.name` to match.
- [ ] **Add a comparison feature** — "Compare Packages" button that opens a side-by-side table view.

---

## 5. TYPOGRAPHY — Currently: 6/10

### Problems
- Hero: 72px → Section title: 40px → Product name: 17px → Description: 12px. The jump from 40px to 17px is too large. Missing intermediate sizes.
- 12px product descriptions are nearly unreadable on mobile.
- No type scale system — sizes are chosen ad hoc.

### Fix
- [ ] **Establish a proper type scale** (based on 16px base):
  ```
  Display:  72px / 4.5rem  — Hero title only
  H1:       48px / 3rem    — Section titles (currently 40px, bump up)
  H2:       32px / 2rem    — Package names, sub-sections
  H3:       22px / 1.375rem — Product names (currently 17px, too small)
  Body:     16px / 1rem    — Descriptions, features (currently 12-14px)
  Small:    14px / 0.875rem — Stock labels, badges, meta text
  Caption:  12px / 0.75rem  — Only for truly ancillary text
  ```
- [ ] **Bump product descriptions to 14px minimum** — 12px is too small for readable body text.
- [ ] **Bump product names to 18-20px** — they're the primary interaction point and need to be scannable.
- [ ] **Add `line-height: 1.4` to body text** — currently `1.5` which is generous for UI text, but `1.3` is better for compact cards.
- [ ] **Reduce hero title on mobile from 38px to 34px** — the current 38px is fine but the `letter-spacing: -1px` makes it feel tighter than needed on small screens.

---

## 6. MOBILE EXPERIENCE — Currently: 6/10

### Problems
- Category tabs scroll horizontally but give no visual cue that more categories exist off-screen.
- Search bar collapses awkwardly on mobile.
- Hamburger menu overlay uses `opacity` transition — feels flat, not tactile.
- Hero at 38px feels disconnected from the desktop 72px — no intermediate state for tablets.
- Cart drawer at 100% width on mobile works but has no swipe-to-close gesture.
- No `:active` states on buttons — no tactile feedback on touch devices.

### Fix
- [ ] **Add a fade-out gradient on the category tabs scroll container** — a `::after` pseudo-element on `.tabs-scroll-container` with `background: linear-gradient(to right, transparent, var(--bg))` on the right edge. Shows users there's more to scroll.
- [ ] **Improve mobile menu animation** — change from `opacity` to `transform: translateX(100%)`/`translateX(0)` with `will-change: transform`. Add a backdrop blur animation.
- [ ] **Add `:active` pseudo-class to all buttons** — `transform: scale(0.97)` on desktop is there, but on mobile you need `-webkit-tap-highlight-color: transparent` and a more prominent active state (background color change, not just scale).
- [ ] **Add responsive typography breakpoints** — use `clamp()` for fluid type: `font-size: clamp(2rem, 5vw + 1rem, 4.5rem)` for hero title. This eliminates the jarring 72px → 38px jump.
- [ ] **Add touch feedback** — on mobile, when a user taps a gear card, add a brief `background: rgba(var(--accent-rgb), 0.05)` flash that fades out. This gives tactile confirmation without navigating away.
- [ ] **Cart drawer swipe-to-close** — add touch event handlers for swipe-left to close. Libraries like `sheet-modal` or a simple touchstart/touchmove/touchend implementation.
- [ ] **Add a sticky "Add to Quote" bar on mobile** — when a user scrolls past the hero, show a bottom CTA bar with "View Gear Catalog" or the last item they viewed. This is critical for conversion on mobile.

---

## 7. ACCESSIBILITY — Currently: 2/10

### Problems
- Zero `aria-label` attributes on interactive elements.
- Theme toggle button has no accessible name.
- Cart icon button has no accessible name.
- Hamburger menu has no `aria-expanded` state.
- Color contrast fails WCAG AA for small text (`#6E6E73` on `#F5F5F7` = 4.1:1, needs 4.5:1).
- Dark mode contrast is worse (`#8E8E93` on `#030303` = 3.7:1, needs 4.5:1).
- No `role="navigation"` on `<nav>`.
- No skip-to-content link.
- Images have no meaningful alt text (product images use `${item.name}` which is fine, but fallback SVGs are invisible to screen readers).
- No focus indicators beyond browser defaults.
- No keyboard navigation for the cart drawer.

### Fix
- [ ] **Add `aria-label` to all icon buttons:**
  ```html
  <button class="theme-toggle" aria-label="Toggle dark mode" ...>
  <button class="btn-add" aria-label="Add to quote" ...>
  <div class="cart-trigger" role="button" tabindex="0" aria-label="Open quote cart" ...>
  ```
- [ ] **Add `aria-expanded` to hamburger menu:**
  ```html
  <div class="menu-toggle" aria-expanded="false" aria-label="Open menu" ...>
  ```
  Update in `toggleMobileMenu()`: `toggle.setAttribute('aria-expanded', isOpen)`.
- [ ] **Add a skip-to-content link:**
  ```html
  <a href="#catalog" class="skip-link">Skip to catalog</a>
  ```
  ```css
  .skip-link { position: absolute; top: -100px; left: 0; ... }
  .skip-link:focus { top: 0; ... }
  ```
- [ ] **Fix color contrast:**
  - Light mode: Change `--text-muted: #6E6E73` to `#5D5D61` (4.5:1 contrast against `#F5F5F7`).
  - Dark mode: Change `dark --text-muted: #8E8E93` to `#A1A1A6` (4.5:1 contrast against `#030303`).
  - Or increase font sizes of muted text to 14px+ where possible (AA large text requires only 3:1).
- [ ] **Add visible focus indicators:**
  ```css
  :focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 4px; }
  ```
- [ ] **Make cart drawer keyboard accessible** — ` Escape` closes, Tab traps focus within drawer when open.
- [ ] **Add `role="status"` to toast notifications** and `aria-live="polite"` to toast container.
- [ ] **Add alt text to SVG fallback icons** — `aria-label="${item.name} icon"` on the SVG.
- [ ] **Ensure all form controls have labels** — the search input needs a `<label>` or `aria-label`.
- [ ] **Test with VoiceOver/Mobile Talkback** — at minimum, navigate the entire site with keyboard only.

---

## 8. FOOTER — Currently: 4/10

### Problems
- Thin content: just phone numbers and two bullet lists.
- No social media links (Instagram is CRITICAL for a nightlife/event business).
- No email address.
- "Designed with Apple-grade precision" is a private joke that doesn't belong on a client-facing site.
- No payment methods, industry certifications, or trust signals.
- No legal pages (terms, privacy policy).

### Fix
- [ ] **Add social links** — Instagram (mandatory for nightlife), TikTok, maybe SoundCloud or Mixcloud. Use icon buttons in the footer.
- [ ] **Add email address** — `info@soundscape.nyc` or similar.
- [ ] **Add a "Book a Consultation" CTA** in the footer with a phone number and email.
- [ ] **Remove or replace "Designed with Apple-grade precision"** — the client won't want to advertise that. Replace with something like "Proudly serving NYC's nightlife since 2024" or remove entirely.
- [ ] **Add trust signals** — "Insured & Licensed" badge, payment method icons (Venmo, CashApp, Zelle, credit cards), or "Same-Day Delivery Available".
- [ ] **Add minimal legal links** — "Terms of Service" and "Privacy Policy" links (even if they're placeholder pages). Netlify can serve static pages.
- [ ] **Make the footer responsive** — currently it stacks on mobile, which is fine, but the phone numbers need tap-to-call formatting (they already have `tel:` links, good).

---

## 9. SEO & META — Currently: 3/10

### Problems
- Has `<title>` and `<meta description>` — that's it.
- No Open Graph tags (Facebook, LinkedIn share previews will be blank).
- No Twitter Card tags.
- No structured data (JSON-LD).
- No `<link rel="canonical">`.
- No sitemap.xml.
- No robots.txt.
- The title "Soundscape NYC | Premium Backline & Sound System Rentals" is decent but could be more keyword-rich.

### Fix
- [ ] **Add Open Graph tags:**
  ```html
  <meta property="og:title" content="Soundscape NYC | Premium DJ & Sound System Rentals in NYC">
  <meta property="og:description" content="Rent CDJ-3000s, Pioneer mixers, RCF speakers, CO2 effects & more. Free delivery on orders $350+. Manhattan, Brooklyn, Queens.">
  <meta property="og:image" content="https://stately-pegasus-5db09b.netlify.app/assets/hero_bg.webp">
  <meta property="og:url" content="https://soundscape.nyc/">
  <meta property="og:type" content="website">
  ```
- [ ] **Add Twitter Card tags:**
  ```html
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Soundscape NYC | Premium DJ & Sound System Rentals">
  <meta name="twitter:description" content="...">
  <meta name="twitter:image" content="...">
  ```
- [ ] **Add JSON-LD structured data:**
  ```html
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Soundscape NYC",
    "description": "Premium DJ equipment, backline, and sound system rentals in NYC",
    "telephone": ["718-962-4523", "516-512-3471"],
    "areaServed": ["Manhattan", "Brooklyn", "Queens"],
    "priceRange": "$$",
    "address": { "@type": "PostalAddress", "addressLocality": "New York", "addressRegion": "NY" }
  }
  </script>
  ```
- [ ] **Add canonical URL** — `<link rel="canonical" href="https://soundscape.nyc/">`
- [ ] **Generate sitemap.xml** — add to `build.js` or create manually.
- [ ] **Create robots.txt** — allow all, point to sitemap.
- [ ] **Optimize title for local SEO:**
  ```
  Soundscape NYC | DJ Equipment & Sound System Rentals in Manhattan, Brooklyn & Queens
  ```
- [ ] **Add meta keywords** (low priority but some crawlers still check):
  ```
  <meta name="keywords" content="DJ equipment rental NYC, sound system rental Manhattan, CDJ rental Brooklyn, speaker rental Queens, backline rental NYC">
  ```

---

## 10. PERFORMANCE — Currently: 5/10

### Problems
- 82KB inline CSS blocks render. No critical CSS extraction.
- 17KB inline JavaScript blocks render.
- Google Fonts adds 2+ network requests + font rendering delay.
- 67 WebP images load without lazy loading or size hints.
- No `preconnect` for the Netlify CDN domain.
- No caching headers (Netlify default is fine, but no service worker).

### Fix
- [ ] **Extract critical CSS** — inline only the above-the-fold CSS (header, hero, visible cards) and load the rest asynchronously. Target: <10KB inline CSS.
- [ ] **Defer non-critical JavaScript** — the data loading and rendering can be `defer`ed. Only the theme toggle script needs to be synchronous.
- [ ] **Use `font-display: swap`** for Google Fonts (already in the URL, good).
- [ ] **Preconnect to Netlify CDN:**
  ```html
  <link rel="preconnect" href="https://unpkg.com" crossorigin>
  ```
- [ ] **Add `loading="lazy"` to all images below the fold.**
- [ ] **Add `width` and `height` attributes to all `<img>` tags** to prevent CLS:
  ```html
  <img src="${item.image}" alt="${item.name}" width="400" height="280" loading="lazy" ...>
  ```
- [ ] **Set explicit `aspect-ratio` in CSS for `.gear-visual`** — `aspect-ratio: 400/280;` so the browser reserves space before the image loads.
- [ ] **Add a service worker** for offline caching of the JSON data and previously viewed images. Use Workbox or a simple hand-written SW.
- [ ] **Compress the HTML further** — remove comments, minify inline CSS/JS for production (keep readable in source).
- [ ] **Target Core Web Vitals:**
  - LCP < 2.5s: Hero image + text must render fast
  - FID < 100ms: No heavy JS on load
  - CLS < 0.1: All images and dynamic content need reserved space

---

## 11. INTERACTION & ANIMATION — Currently: 5/10

### Problems
- Cards have basic hover transitions (translateY, box-shadow). Functional but not memorable.
- No scroll-triggered animations.
- No page load animations.
- Cart drawer slides in but nothing else animates.
- The audio visualizer is cool but disconnected from the rest of the page experience.

### Fix
- [ ] **Add staggered card entrance animations** — when the gear grid renders, cards should fade in with a staggered delay (0ms, 50ms, 100ms, etc.). Use `IntersectionObserver` + CSS `animation`:
  ```css
  .gear-card { opacity: 0; transform: translateY(20px); transition: opacity 0.4s, transform 0.4s; }
  .gear-card.visible { opacity: 1; transform: translateY(0); }
  ```
- [ ] **Add sticky header shrink animation** — the `header.scrolled` class exists but the transition is just `padding` and `background`. Add a `box-shadow: 0 4px 20px rgba(0,0,0,0.08)` fade-in.
- [ ] **Animate the hero on load** — title fades in from bottom (0.6s delay), description fades in (0.9s delay), buttons slide up (1.2s delay).
- [ ] **Add a cart counter bounce** — when an item is added, the `#cartCount` element should scale up briefly (CSS animation: `scale(1) → scale(1.4) → scale(1)` over 300ms).
- [ ] **Add section reveal animations** — each section (about, packages, catalog) should fade in when scrolled into view using `IntersectionObserver`.
- [ ] **Remove all `onclick` inline handlers** — replace with `addEventListener` in JavaScript. This is cleaner, enables `passive` event listeners for scroll, and allows better CSP headers.

---

## 12. CONVERSION OPTIMIZATION — Currently: 6/10

### Problems
- No urgency or scarcity signals beyond "In Stock (x8)".
- No "Popular" or "Most Rented" badges on high-demand items.
- No social proof (no reviews, ratings, or testimonials).
- No "Recently booked" or "Booked 3 times this week" dynamic signals.
- The "Text for Price" label on line arrays is vague — should say "Starting at $X/day, call for quote".
- No sticky CTA on mobile.
- No WhatsApp integration despite the text-based checkout flow.

### Fix
- [ ] **Add dynamic badges** — in the gear JSON, add an optional `badge` field that maps to visual labels:
  - `"badge": "popular"` → orange "Most Rented" pill
  - `"badge": "new"` → blue "New Arrival" pill
  - `"badge": "limited"` → red "Limited Stock" pill
- [ ] **Add a testimonials section** — even 3-5 quotes from DJs/venues with names and events. Pull from real reviews or ask the client for permission to quote.
- [ ] **Change "Text for Price" to "Call for Quote"** — more actionable, clearer intent.
- [ ] **Add WhatsApp Business integration:**
  ```html
  <a href="https://wa.me/17189624523?text=Hi%20Soundscape%20NYC%21%20I%27m%20interested%20in%20renting%20gear."
     class="whatsapp-float-btn" aria-label="Chat on WhatsApp">
  ```
  Floating button in bottom-right corner, green WhatsApp icon, opens pre-filled message.
- [ ] **Add a sticky mobile CTA bar** — bottom of screen on mobile: "Call Now" + "View Catalog" buttons. Fixed position, z-index above everything.
- [ ] **Add "Booked X times this month"** — can be a static number in the JSON or computed from order data. Even fake social proof ("Popular choice — rented 12 times this month") increases conversion.
- [ ] **Add a trust bar above the gear catalog** — "Insured Equipment • Same-Day Delivery • Tested & Checked • Free Delivery $350+"

---

## 13. DARK MODE REFINEMENT — Currently: 7/10

### Problems
- Dark mode is implemented well with CSS variables, but some elements don't fully transition.
- The hero background overlay gets darker in dark mode (intentional, but feels heavy).
- Package cards in dark mode lose visual separation — the glass effect flattens.
- Some inline styles use hardcoded colors that don't respect theme.

### Fix
- [ ] **Audit all inline styles** — search for `style=` in the HTML. Several use hardcoded colors (`style="color:var(--text-muted)`, `style="font-size:..."`). Move these to CSS classes where possible.
- [ ] **Add dark mode transitions** — `transition: background-color 0.3s, color 0.3s, border-color 0.3s` on `body`, `header`, `.gear-card`, `.package-card`, `.glass-panel`. This makes the theme toggle feel smooth instead of instant.
- [ ] **Reduce hero overlay heaviness in dark mode** — change from `rgba(3,3,3,0.98)` to `rgba(3,3,3,0.85)` at the bottom. The current near-black makes the bottom of the hero look like a void.
- [ ] **Add a subtle gradient to dark-mode package cards** — a `background: linear-gradient(to bottom, rgba(255,255,255,0.03), transparent)` to add depth.
- [ ] **Ensure all SVG icons adapt to dark mode** — the phone SVG, search icon, cart icon, and category icons should use `currentColor` so they respond to theme changes.

---

## 14. MISCELLANEOUS POLISH

- [ ] **Add a favicon.ico** — the current emoji favicon `🎛` works in modern browsers but doesn't appear in bookmarks or older browsers. Generate a proper `.ico` from a logo mark.
- [ ] **Add Apple touch icons** — `<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">` (180x180).
- [ ] **Add a `manifest.json`** for PWA capabilities — name, icons, theme color, background color. Enables "Add to Home Screen" on mobile.
- [ ] **Add a 404 page** — Netlify serves a default one, but a branded 404 with a link back to the catalog is better.
- [ ] **Add error boundary for image loading** — the `onerror` handler on gear images is good, but the fallback SVG should be more visually appealing (larger icon, subtle background color, product name text).
- [ ] **Add `prefers-reduced-motion` support:**
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
  }
  ```
- [ ] **Add `prefers-color-scheme` detection** — on first visit, if no theme is saved in localStorage, check `window.matchMedia('(prefers-color-scheme: dark)')` and auto-set dark mode. Many users expect this.
- [ ] **Fix the `soundscape-theme` localStorage key** — it's local to this site which is fine, but consider renaming to `theme` for the template extraction.
- [ ] **Add a privacy-conscious analytics integration** — either Netlify Analytics (built-in, free) or Plausible/Fathom ($). No Google Analytics (bloated, privacy-hostile).
- [ ] **Prevent layout shift on package section** — the packages grid renders dynamically, but without a minimum height, the page will jump when data loads. Add `min-height` to `.packages-grid`.

---

## 15. CMS EDITOR EXPERIENCE — Currently: 5/10

### Problems
- No custom preview templates in the CMS admin.
- No summary strings on collections (items show as "gear — cdj3000x" instead of "Pioneer CDJ 3000 — $150/day").
- No editorial workflow (draft → review → publish).
- Image uploads from phone are unoptimized JPEGs/HEICs.
- No way to reorder items in a collection.

### Fix
- [ ] **Add CMS summary templates:**
  ```javascript
  // In admin/index.html collection config
  summary: "{{name}} — ${{price}}/day",
  ```
  This makes the CMS list view show "Pioneer CDJ 3000 — $150/day" instead of just "cdj3000".
- [ ] **Add a custom preview template** — register a React preview component that renders the gear card as it would appear on the site. This lets the client see exactly how their edit will look before saving.
- [ ] **Enable editorial workflow** — add `publish_mode: "editorial_workflow"` to the CMS config. This adds draft → in review → published states. Useful if the client has an assistant who enters data but the owner wants to approve before publishing.
- [ ] **Add image optimization to `build.js`** — on every Netlify build, process all images in `assets/` through Sharp to create WebP versions at standard sizes. If someone uploads a 5MB iPhone photo, it becomes a 100KB WebP automatically.
- [ ] **Add CMS field validation** — require `id` to be lowercase alphanumeric with hyphens only. Add `pattern` validation to the ID field:
  ```javascript
  { label: "ID", name: "id", widget: "string", pattern: ["^[a-z0-9-]+$", "Only lowercase letters, numbers, and hyphens"] }
  ```

---

## PRIORITY RANKING

| Priority | Item | Impact | Effort |
|----------|------|--------|--------|
| P0 | Loading skeletons & progressive images | High | Medium |
| P0 | Accessibility (contrast, aria-labels, focus) | High | Medium |
| P0 | SEO meta tags (OG, Twitter, JSON-LD) | High | Low |
| P0 | WhatsApp floating button + mobile CTA bar | High | Low |
| P1 | Product image consistency + lightbox | High | Medium |
| P1 | Hero improvements (LQIP, Ken Burns, copy) | Medium | Low |
| P1 | Typography scale fix | Medium | Low |
| P1 | CMS summary strings | Medium | Low |
| P1 | `loading="lazy"` + `width`/`height` on images | Medium | Low |
| P2 | Package section redesign (featured card 2x) | Medium | Medium |
| P2 | Footer content (social, email, trust signals) | Medium | Low |
| P2 | Dark mode transitions | Medium | Low |
| P2 | Scroll animations (IntersectionObserver) | Medium | Medium |
| P2 | `prefers-color-scheme` auto-detection | Low | Low |
| P2 | `prefers-reduced-motion` support | Low | Low |
| P3 | Service worker (offline caching) | Low | Medium |
| P3 | PWA manifest | Low | Low |
| P3 | Editorial workflow in CMS | Low | Low |
| P3 | Custom CMS preview templates | Low | High |
| P3 | Image optimization in build.js | Medium | High |
| P3 | 404 page | Low | Low |
| P3 | Analytics integration | Low | Low |

---

## ESTIMATED EFFORT

| Phase | Items | Time |
|-------|-------|------|
| P0 (Must-have) | Loading states, accessibility, SEO, WhatsApp | 8-10 hours |
| P1 (High-impact) | Image consistency, hero, typography, CMS summaries, lazy-load | 6-8 hours |
| P2 (Polish) | Package redesign, footer, animations, dark mode transitions | 8-10 hours |
| P3 (Nice-to-have) | Service worker, PWA, editorial workflow, image optimization | 10-15 hours |
| **Total** | | **32-43 hours** |

After all P0-P2 items are done, this site moves from a 7/10 to a 9/10. P3 items push it to 10/10 territory.