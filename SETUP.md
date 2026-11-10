# Setup

1. Copy this repository's contents into your **public** `Schrodingerrs-cat/Schrodingerrs-cat` profile repository.
2. Confirm repository **Settings → Actions → General → Workflow permissions** allows **Read and write permissions**. The provided job requests `contents: write`.
3. Run the **Refresh profile cards** workflow manually for the first fetch. The scheduled run refreshes every day at **05:17 UTC**.
4. To generate locally, install `fonttools[woff]`, `fonts-inter` and `fonts-dejavu-core`; then `python scripts/render_cards.py`.
5. For screenshots, run `STATIC=1 python scripts/render_cards.py`. **Do not commit the static versions** unless you want a non-animated profile: run `python scripts/render_cards.py` to restore them.
6. To change branding, edit `BG`, `PANEL`, `TEXT`, `MUTED`, `ACCENT`, and font paths near the start of `scripts/render_cards.py`.
7. Optional portrait: save a small PNG at `assets/portrait.png` (cropped circle in the hero). The default hero is typography-first, no portrait.

## Data semantics

The workflow uses the authenticated GitHub GraphQL `contributionsCollection.contributionCalendar` API. `data/contributions.json` contains the daily counts of contributions exposed to the workflow token. This is **not a commit-only metric**, and private contribution counts depend on GitHub visibility/permissions.

`CURRENT STREAK` counts consecutive contribution days through **today UTC**, or through **yesterday UTC** if nothing has been recorded today. `ACTIVE DAYS` is the number of days with at least one contribution in the returned 365-day calendar. `BUSIEST DAY` is the highest-count day in the calendar. Monthly columns include every calendar month intersecting the last year (up to 12 most recent months).

If the local JSON file is absent, the chart says that data is not yet available; no fake statistics are generated.

## Caveats

- Website CSS was not inspectable through the available page reader. The supplied dark navy/lime palette and Inter font are **configurable approximations**, not a verified exact match to `aryanshah.work`.
- A browser loading an SVG through `<img>` cannot run JavaScript, fetch external images/fonts, or activate links inside the SVG. Each tile is linked by an HTML `<a>` wrapping the `<img>`.
- Declarative CSS keyframe animations are supported by modern browsers, but GitHub's proxies, caching, and accessibility settings can affect display. Every card uses reduced-motion CSS with the fully visible final state.
- Staggering uses local animation delays. Browser image loading does **not** guarantee precise synchronization across separate `<img>` instances.
- The script uses CSS animation instead of SMIL so the `prefers-reduced-motion` rule can reliably disable all motion.
- A WOFF font is embedded in **each SVG** using `pyftsubset`; this trades file size for portable appearance. Actual rendering may still differ between SVG implementations.
