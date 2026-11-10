# Setup

1. Copy this repository's contents into your **public** `Schrodingerrs-cat/Schrodingerrs-cat` profile repository.
2. Confirm repository **Settings → Actions → General → Workflow permissions** allows **Read and write permissions**. The provided job requests `contents: write`.
3. Run the **Refresh profile cards** workflow manually for the first fetch. The scheduled run refreshes every day at **05:17 UTC**.
4. To generate locally, run `python scripts/render_cards.py`. Fonts are the subset WOFFs in `fonts/` (Instrument Serif, Geist, Geist Mono; SIL OFL).
5. For screenshots, run `STATIC=1 python scripts/render_cards.py`. **Do not commit the static versions** unless you want a non-animated profile: run `python scripts/render_cards.py` to restore them.
6. To change branding, edit `PAPER`, `INK`, `TECH`, `STUDIO`, `LEARN`, and the `FONT_FILES` map near the start of `scripts/render_cards.py`.
7. Optional portrait: save a small PNG at `assets/portrait.png` if you later wire portrait embedding back in. The default hero is typography-first.

## Data semantics

The workflow uses the authenticated GitHub GraphQL `contributionsCollection.contributionCalendar` API. `data/contributions.json` contains the daily counts of contributions exposed to the workflow token. This is **not a commit-only metric**, and private contribution counts depend on GitHub visibility/permissions.

`CURRENT STREAK` counts consecutive contribution days through **today UTC**, or through **yesterday UTC** if nothing has been recorded today. `ACTIVE DAYS` is the number of days with at least one contribution in the returned 365-day calendar. `BUSIEST DAY` is the highest-count day in the calendar. Monthly columns include every calendar month intersecting the last year (up to 12 most recent months).

If the local JSON file is absent, the chart says that data is not yet available; no fake statistics are generated.

## Caveats

- Visual language is the paper / ink / Instrument Serif + Geist stack from the Three Worlds README pattern, with WORK blue, SITE red, and TALK yellow tiles.
- Layout order is hero → contribution heatmap → monthly activity → three link tiles. Keep README cards tight (no blank lines between rows) so GitHub spacing matches the baked SVG gaps.
- A browser loading an SVG through `<img>` cannot run JavaScript, fetch external images/fonts, or activate links inside the SVG. Each tile is linked by an HTML `<a>` wrapping the `<img>`.
- Cards use CSS keyframes plus limited SMIL (name shine). Every animation turns off under `prefers-reduced-motion`.
- Staggering uses local animation delays. Browser image loading does **not** guarantee precise synchronization across separate `<img>` instances.
- Subset WOFF fonts from `fonts/` are embedded in each SVG as data URIs for portable appearance.
