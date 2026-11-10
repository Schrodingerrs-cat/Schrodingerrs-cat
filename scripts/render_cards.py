#!/usr/bin/env python3
"""Animated GitHub profile SVG cards for Schrodingerrs-cat.

Layout matches the "Three Worlds" card stack pattern:
  hero → contribution heatmap → monthly activity → three link tiles

Cards are shown through <img>, so they only use inline CSS keyframes, SMIL,
and fonts subset with pyftsubset and embedded as base64 WOFF. No featured
repo cards. Contribution data comes from data/contributions.json.

Usage:
  python scripts/render_cards.py --fetch
  python scripts/render_cards.py
  STATIC=1 python scripts/render_cards.py
"""
from __future__ import annotations

import argparse
import base64
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
import html
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / 'cards'
DATA = ROOT / 'data' / 'contributions.json'
USERNAME = 'Schrodingerrs-cat'

# Brand tokens — dark navy / lime, approximating aryanshah.work
BG = '#0B1220'
PANEL = '#111C2E'
PANEL_2 = '#152338'
BORDER = '#2B3C53'
TEXT = '#EAF3F8'
MUTED = '#91A8BA'
INK_SOFT = '#C5D4E0'
ACCENT = '#A7F36D'
ACCENT_2 = '#65D6CF'
ACCENT_3 = '#F0C35A'
W = 880
GAP = 12
BOTTOM = 12

STATIC = os.environ.get('STATIC') == '1'


def system_font(name, fallback):
    try:
        return subprocess.check_output(['fc-match', '-f', '%{file}', name], text=True).strip() or fallback
    except (OSError, subprocess.CalledProcessError):
        return fallback


FONT_REG = os.environ.get('FONT_REG') or system_font('Inter:style=Regular', '/usr/share/fonts/truetype/inter/Inter-Regular.otf')
FONT_BOLD = os.environ.get('FONT_BOLD') or system_font('Inter:style=Bold', '/usr/share/fonts/truetype/inter/Inter-Bold.otf')
FONT_MONO = os.environ.get('FONT_MONO') or system_font('DejaVu Sans Mono', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')

SANS = 'InterCard, system-ui, sans-serif'
MONO = 'MonoCard, ui-monospace, monospace'

BASE_CSS = """
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes pop{0%{opacity:0;transform:scale(.3)}70%{opacity:1;transform:scale(1.15)}100%{opacity:1;transform:none}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes nudge{0%,100%{transform:none}50%{transform:translateX(4px)}}
@keyframes nudgeup{0%,100%{transform:none}50%{transform:translate(3px,-3px)}}
@keyframes tilein{0%{opacity:0;transform:translateY(90px) scale(.6) rotate(-9deg)}55%{opacity:1;transform:translateY(-10px) scale(1.05) rotate(2deg)}75%{transform:translateY(3px) scale(.98) rotate(-.8deg)}90%{transform:translateY(-1px) scale(1.01) rotate(.2deg)}100%{opacity:1;transform:none}}
@keyframes slidein{from{opacity:0;transform:translateX(-26px)}to{opacity:1;transform:none}}
@keyframes arrowin{0%{opacity:0;transform:translateX(-30px)}60%{opacity:1;transform:translateX(6px)}100%{opacity:1;transform:none}}
@keyframes sheen{0%{transform:translateX(-260px) skewX(-20deg)}22%,100%{transform:translateX(420px) skewX(-20deg)}}
@keyframes ring{0%{opacity:.7;transform:scale(.2)}100%{opacity:0;transform:scale(2.4)}}
.r{opacity:0;animation:rise .8s cubic-bezier(.2,.7,.2,1) both;transform-box:fill-box}
.f{opacity:0;animation:fade .9s ease-out both}
.g{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:grow .8s cubic-bezier(.2,.7,.2,1) both}
.p{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .4s ease-out both}
.live{animation:pulse 1.6s ease-in-out infinite}
.n{transform-box:fill-box;animation:nudge 1.8s ease-in-out infinite}
.nu{transform-box:fill-box;animation:nudgeup 1.8s ease-in-out infinite}
.ti{opacity:0;transform-box:fill-box;transform-origin:50% 60%;animation:tilein 1.1s cubic-bezier(.2,.8,.2,1) both}
.sl{opacity:0;transform-box:fill-box;animation:slidein .6s cubic-bezier(.2,.7,.2,1) both}
.ai{opacity:0;transform-box:fill-box;animation:arrowin .7s cubic-bezier(.2,.7,.2,1) both}
.sh{animation:sheen 5s ease-in-out infinite}
.rg{opacity:0;transform-box:fill-box;transform-origin:center;animation:ring 1s ease-out both}
@media (prefers-reduced-motion: reduce){
  .r,.f,.g,.p,.live,.n,.nu,.ti,.sl,.ai,.rg{animation:none!important;opacity:1!important;transform:none!important}
  .sh,.rg{display:none}
}
"""


def esc(value):
    return html.escape(str(value), quote=True)


def d(seconds):
    return f'style="animation-delay:{seconds:.2f}s"'


def fetch_data():
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not token:
        raise RuntimeError('Set GH_TOKEN (or GITHUB_TOKEN) for --fetch')
    start = (datetime.now(timezone.utc) - timedelta(days=365)).date().isoformat()
    end = datetime.now(timezone.utc).date().isoformat()
    query = '''query($login:String!,$from:DateTime!,$to:DateTime!){
      user(login:$login){ contributionsCollection(from:$from,to:$to){
        contributionCalendar { totalContributions weeks {
          contributionDays { date contributionCount contributionLevel }
        } }
      } }
    }'''
    payload = json.dumps({'query': query, 'variables': {
        'login': USERNAME, 'from': start + 'T00:00:00Z', 'to': end + 'T23:59:59Z'
    }}).encode()
    req = Request('https://api.github.com/graphql', payload,
                  {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json',
                   'User-Agent': 'profile-svg-card-builder'}, method='POST')
    with urlopen(req, timeout=40) as r:
        response = json.load(r)
    if response.get('errors') or not response.get('data', {}).get('user'):
        raise RuntimeError('GitHub GraphQL error: ' + repr(response.get('errors')))
    cal = response['data']['user']['contributionsCollection']['contributionCalendar']
    days = sorted(({'date': day['date'], 'count': day['contributionCount']}
                   for week in cal['weeks'] for day in week['contributionDays']),
                  key=lambda item: item['date'])
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps({
        'username': USERNAME,
        'retrieved_at': datetime.now(timezone.utc).isoformat(),
        'source': 'GitHub GraphQL contributionsCollection.contributionCalendar',
        'total_contributions': cal['totalContributions'],
        'days': days,
    }, indent=2) + '\n', encoding='utf-8')
    print('Fetched', len(days), 'days of GitHub activity')


def load_data():
    if not DATA.exists():
        return {'days': [], 'total_contributions': 0}
    raw = json.loads(DATA.read_text(encoding='utf-8'))
    if raw.get('username') != USERNAME:
        raise ValueError('contributions.json username mismatch')
    days = raw.get('days', [])
    seen = set()
    for item in days:
        date.fromisoformat(item['date'])
        if item['date'] in seen or not isinstance(item['count'], int) or item['count'] < 0:
            raise ValueError('invalid or duplicated contribution date')
        seen.add(item['date'])
    days = sorted(days, key=lambda item: item['date'])
    total = raw.get('total_contributions')
    if not isinstance(total, int):
        total = sum(item['count'] for item in days)
    return {'days': days, 'total_contributions': total}


def subset_font(path, chars):
    if not Path(path).exists() or not shutil.which('pyftsubset'):
        raise RuntimeError(f'Font missing or pyftsubset unavailable: {path}')
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / 'subset.woff'
        subset_chars = Path(td) / 'chars.txt'
        subset_chars.write_text(chars, encoding='utf-8')
        cmd = ['pyftsubset', path, f'--output-file={out}', '--flavor=woff',
               f'--text-file={subset_chars}', '--layout-features=*',
               '--no-hinting', '--ignore-missing-unicodes']
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        return base64.b64encode(out.read_bytes()).decode('ascii')


def font_css(keys=('reg', 'bold', 'mono')):
    chars = ''.join(chr(i) for i in range(32, 127)) + '–—·’→↗×°≥≤Σéöꞏ✓•'
    mapping = {
        'reg': ('InterCard', 'normal', 400, FONT_REG),
        'bold': ('InterCard', 'normal', 700, FONT_BOLD),
        'mono': ('MonoCard', 'normal', 400, FONT_MONO),
    }
    out = []
    for key in keys:
        fam, style, weight, path = mapping[key]
        b64 = subset_font(path, chars)
        out.append(
            f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{weight};"
            f"src:url(data:font/woff;base64,{b64}) format('woff')}}"
        )
    return ''.join(out)


def svg(name, width, height, body, fonts, label, left=0, right=0, bottom=BOTTOM, extra_css=''):
    if left:
        body = f'<g transform="translate({left:.3f} 0)">{body}</g>'
    width = width + left + right
    height = height + bottom
    css = fonts + BASE_CSS + extra_css
    if STATIC:
        css += ('.r,.f,.g,.p,.live,.n,.nu,.ti,.sl,.ai{animation:none!important;'
                'opacity:1!important;transform:none!important}.sh,.rg{display:none}')
    content = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.3f}" height="{height}" '
        f'viewBox="0 0 {width:.3f} {height}" role="img" aria-label="{esc(label)}">'
        f'<title>{esc(label)}</title><style>{css}</style>{body}</svg>'
    )
    path = CARDS / name
    path.write_text(content, encoding='utf-8')
    print(f'Wrote {path.relative_to(ROOT)} ({path.stat().st_size // 1024} KB)')


def wrap(text, n):
    lines, line = [], ''
    for word in text.split():
        if line and len(line) + 1 + len(word) > n:
            lines.append(line)
            line = word
        else:
            line = f'{line} {word}'.strip()
    return lines + [line] if line else lines


def text_lines(x, y, lines, lh, attrs):
    return ''.join(
        f'<text x="{x}" y="{y + i * lh}" {attrs}>{esc(line)}</text>'
        for i, line in enumerate(lines)
    )


def stats(days):
    counts = {item['date']: item['count'] for item in days}
    today = datetime.now(timezone.utc).date()
    eligible = [date.fromisoformat(day) for day, count in counts.items()
                if count > 0 and date.fromisoformat(day) <= today]
    active = len(eligible)
    busiest = max(days, key=lambda item: item['count']) if days else None
    cursor = today if counts.get(today.isoformat(), 0) > 0 else today - timedelta(days=1)
    streak = 0
    while counts.get(cursor.isoformat(), 0) > 0:
        streak += 1
        cursor -= timedelta(days=1)
    months = defaultdict(int)
    for item in days:
        months[item['date'][:7]] += item['count']
    return active, streak, busiest, months


def hero(fonts):
    h = 360
    body = f'''
<defs>
  <linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="600" y2="0">
    <stop offset="0" stop-color="{TEXT}"/>
    <stop offset=".42" stop-color="{TEXT}"/>
    <stop offset=".5" stop-color="{ACCENT}"/>
    <stop offset=".58" stop-color="{TEXT}"/>
    <stop offset="1" stop-color="{TEXT}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-600 0;600 0;600 0"
      keyTimes="0;.45;1" dur="7s" begin="1.6s" repeatCount="indefinite"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{h}" rx="16" fill="{BG}"/>
<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="15" fill="none" stroke="{BORDER}"/>
<g class="f" {d(0)}>
  <rect class="live" x="44" y="46" width="8" height="8" rx="2" fill="{ACCENT}"/>
  <text x="62" y="54" font-family="{MONO}" font-size="12" letter-spacing="1.2" fill="{MUTED}">ROBOTICS / PERCEPTION / EMBODIED AI</text>
</g>
<text class="r" {d(0.15)} x="40" y="150" font-family="{SANS}" font-weight="700" font-size="78" letter-spacing="-2" fill="{TEXT}">Aryan</text>
<text class="r" {d(0.3)} x="40" y="230" font-family="{SANS}" font-weight="700" font-size="78" letter-spacing="-2" fill="url(#shine)">Shah</text>
<g class="r" {d(0.55)}>
  {text_lines(44, 278, [
      'i teach machines to see, reason, and occasionally',
      'avoid running into things.',
  ], 24, f'font-family="{SANS}" font-size="17" fill="{INK_SOFT}"')}
</g>
<g class="f" {d(0.85)}>
  <text x="44" y="336" font-family="{MONO}" font-size="13" fill="{ACCENT_2}">WPI</text>
  <text x="84" y="336" font-family="{MONO}" font-size="13" fill="{MUTED}">/</text>
  <text x="100" y="336" font-family="{MONO}" font-size="13" fill="{MUTED}">SCHRÖDINGER’S VISION  ·  2026</text>
  <text x="760" y="336" font-family="{MONO}" font-size="13" fill="{MUTED}">aryanshah.work</text>
  <text class="nu" x="888" y="336" text-anchor="end" font-family="{MONO}" font-size="13" fill="{ACCENT}">↗</text>
</g>
'''
    svg('hero.svg', W, h, body, fonts,
        'Aryan Shah — Robotics, Perception and Embodied AI')


GREEN = [PANEL_2, '#1E2C3D', '#355C42', '#588F50', '#79BA5D', ACCENT]


def level_for(count):
    if count <= 0:
        return 0
    if count < 2:
        return 1
    if count < 4:
        return 2
    if count < 7:
        return 3
    if count < 12:
        return 4
    return 5


def heatmap(data, fonts):
    days = data['days']
    if not days:
        body = f'''
<rect width="{W}" height="220" rx="16" fill="{BG}"/>
<rect x="1" y="1" width="{W-2}" height="218" rx="15" fill="none" stroke="{BORDER}"/>
<text class="r" {d(0.8)} x="42" y="70" font-family="{SANS}" font-weight="700" font-size="28" fill="{TEXT}">Every day, <tspan fill="{ACCENT}">in lime</tspan></text>
<text class="f" {d(1.0)} x="42" y="120" font-family="{SANS}" font-size="16" fill="{MUTED}">Waiting for GitHub GraphQL contribution data.</text>
'''
        svg('contributions.svg', W, 220, body, fonts, 'Contribution graph placeholder')
        return

    first = date.fromisoformat(days[0]['date'])
    lead = (first.weekday() + 1) % 7
    cell, step, gx, gy = 11, 14, 42, 92
    cells, months, seen = [], [], set()
    for i, day in enumerate(days):
        k = i + lead
        col, row = divmod(k, 7)
        current = date.fromisoformat(day['date'])
        if current.day <= 7 and (current.year, current.month) not in seen and row == 0:
            seen.add((current.year, current.month))
            months.append((col, current.strftime('%b')))
        count = day['count']
        delay = 1.0 + col * 0.03 + row * 0.02
        cells.append(
            f'<rect class="p" style="animation-delay:{delay:.2f}s" '
            f'x="{gx + col * step}" y="{gy + row * step}" width="{cell}" height="{cell}" '
            f'rx="2.5" fill="{GREEN[level_for(count)]}">'
            f'<title>{day["date"]}: {count} contribution{"s" if count != 1 else ""}</title></rect>'
        )
    ncols = (len(days) + lead + 6) // 7
    right = gx + ncols * step - 3
    labels = ''.join(
        f'<text x="{gx + col * step}" y="{gy + 7 * step + 16}" font-family="{MONO}" '
        f'font-size="11" fill="{MUTED}">{month}</text>'
        for col, month in months if col < ncols - 8
    )
    legend_x = right - len(GREEN) * 14
    legend = ''.join(
        f'<rect x="{legend_x + i * 14}" y="{gy + 7 * step + 6}" width="11" height="11" '
        f'rx="2.5" fill="{color}"/>'
        for i, color in enumerate(GREEN)
    )
    h = gy + 7 * step + 44
    total = data['total_contributions']
    body = f'''
<rect width="{W}" height="{h}" rx="16" fill="{BG}"/>
<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="15" fill="none" stroke="{BORDER}"/>
<text class="r" {d(0.8)} x="42" y="58" font-family="{SANS}" font-weight="700" font-size="30" fill="{TEXT}">Every day, <tspan fill="{ACCENT}">in lime</tspan></text>
<text class="f" {d(0.8)} x="{right}" y="56" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="1" fill="{MUTED}">REFRESHED DAILY</text>
{''.join(cells)}
<g class="f" {d(2.4)}>{labels}
<text x="{legend_x - 8}" y="{gy + 7 * step + 16}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUTED}">less</text>
{legend}
<text x="{legend_x + len(GREEN) * 14 + 2}" y="{gy + 7 * step + 16}" font-family="{MONO}" font-size="11" fill="{MUTED}">more</text></g>
'''
    svg('contributions.svg', W, h, body, fonts,
        f'Contribution graph: {total:,} contributions in the last year')


def activity(data, fonts):
    days = data['days']
    active, streak, busiest, monthly = stats(days)
    h = 340
    keys = sorted(monthly)[-12:] if monthly else []
    values = [monthly[key] for key in keys]
    bars = []
    if keys:
        peak = max(1, max(values))
        best_i = max(range(len(values)), key=lambda i: values[i])
        x0, x1, base, maxh, gap = 40, 600, 292, 140, 10
        bw = (x1 - x0 - gap * (len(keys) - 1)) / len(keys)
        for i, (key, value) in enumerate(zip(keys, values)):
            bh = max(4, round(value / peak * maxh)) if value else 3
            x = x0 + i * (bw + gap)
            fill = ACCENT if i == best_i else ('#2A3B4F' if i == len(keys) - 1 else '#6F8A74')
            label = datetime.strptime(key + '-01', '%Y-%m-%d').strftime('%b')
            bars.append(
                f'<rect class="g" style="animation-delay:{2.2 + i * 0.07:.2f}s" '
                f'x="{x:.1f}" y="{base - bh}" width="{bw:.1f}" height="{bh}" rx="4" fill="{fill}">'
                f'<title>{label}: {value:,}</title></rect>'
                f'<text class="f" style="animation-delay:{2.2 + i * 0.07:.2f}s" '
                f'x="{x + bw / 2:.1f}" y="{base + 22}" text-anchor="middle" '
                f'font-family="{MONO}" font-size="11" fill="{MUTED}">{label}</text>'
            )
            if i == best_i:
                bars.append(
                    f'<text class="p" style="animation-delay:3.2s" x="{x + bw / 2:.1f}" '
                    f'y="{base - bh - 10}" text-anchor="middle" font-family="{MONO}" '
                    f'font-size="11" fill="{ACCENT}">{value:,}</text>'
                )

    total = data['total_contributions'] if days else 0
    side_stats = [
        (f'{streak}', 'current streak, days'),
        (f'{active}', 'days with a contribution'),
        (f'{busiest["count"] if busiest else "—"}', 'on the busiest day'),
    ]
    side = []
    for i, (big, small) in enumerate(side_stats):
        y = 104 + i * 92
        side.append(
            f'<g class="r" {d(2.6 + i * 0.15)}>'
            f'<text x="650" y="{y}" font-family="{SANS}" font-weight="700" font-size="40" fill="{TEXT}">{big}</text>'
            f'<text x="650" y="{y + 24}" font-family="{SANS}" font-size="13" fill="{MUTED}">{esc(small)}</text></g>'
        )
        if i < 2:
            side.append(f'<rect class="f" {d(2.6)} x="650" y="{y + 44}" width="190" height="1" fill="{BORDER}"/>')

    headline = f'{total:,} contributions' if days else 'Waiting for data'
    body = f'''
<rect width="{W}" height="{h}" rx="16" fill="{BG}"/>
<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="15" fill="none" stroke="{BORDER}"/>
<text class="f" {d(1.9)} x="40" y="52" font-family="{MONO}" font-size="12" letter-spacing="1" fill="{MUTED}">THE LAST 12 MONTHS ON GITHUB</text>
<text class="r" {d(2.0)} x="38" y="104" font-family="{SANS}" font-weight="700" font-size="42" fill="{TEXT}">{esc(headline)}</text>
{''.join(bars)}
{''.join(side)}
'''
    svg('activity.svg', W, h, body, fonts,
        f'{total:,} contributions in the last year, {streak}-day streak')


TILE_W = W / 3 - 8
TILE_H = 210


def tile(name, label, color, on, title, blurb, delay, pos, fonts):
    lines = wrap(blurb, 28)
    blurb_svg = ''.join(
        f'<text class="r" {d(delay + 0.75 + i * 0.1)} x="24" y="{148 + i * 20}" '
        f'font-family="{SANS}" font-size="14" fill="{on}" opacity=".92">{esc(line)}</text>'
        for i, line in enumerate(lines)
    )
    body = f'''
<defs>
  <clipPath id="card"><rect width="{TILE_W}" height="{TILE_H}" rx="16"/></clipPath>
  <linearGradient id="gl" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#fff" stop-opacity=".28"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
</defs>
<g class="ti" {d(delay)}>
  <g clip-path="url(#card)">
    <rect width="{TILE_W}" height="{TILE_H}" fill="{color}"/>
    <circle class="rg" {d(delay + 0.5)} cx="{TILE_W - 40}" cy="{TILE_H - 40}" r="60"
      fill="none" stroke="{on}" stroke-opacity=".45" stroke-width="2"/>
    <rect class="sh" style="animation-delay:{delay + 1.4:.2f}s" x="0" y="-20" width="90"
      height="{TILE_H + 40}" fill="url(#gl)" transform="translate(-260 0)"/>
  </g>
  <text class="sl" {d(delay + 0.35)} x="24" y="38" font-family="{MONO}" font-size="12"
    letter-spacing="1.2" fill="{on}">{label}</text>
  <g class="ai" {d(delay + 0.5)}>
    <text class="n" style="animation-delay:{delay + 1.3:.2f}s" x="{TILE_W - 28}" y="38"
      font-family="{MONO}" font-size="14" fill="{on}">→</text>
  </g>
  <text class="r" {d(delay + 0.5)} x="24" y="108" font-family="{SANS}" font-weight="700"
    font-size="34" fill="{on}">{esc(title)}</text>
  {blurb_svg}
</g>
'''
    svg(f'{name}.svg', TILE_W, TILE_H, body, fonts, f'{label}: {title}. {blurb}',
        left=4 * pos, right=8 - 4 * pos)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fetch', action='store_true', help='Refresh data from GitHub GraphQL first')
    args = parser.parse_args()
    if args.fetch:
        fetch_data()
    CARDS.mkdir(parents=True, exist_ok=True)
    data = load_data()
    fonts = font_css()
    hero(fonts)
    heatmap(data, fonts)
    activity(data, fonts)
    tile('tile-work', 'WORK', ACCENT, BG, 'Projects',
         'Browse repositories and selected engineering builds.', 3.1, 0, fonts)
    tile('tile-site', 'SITE', ACCENT_2, BG, 'Portfolio',
         'Research, experience, and writing on aryanshah.work.', 3.35, 1, fonts)
    tile('tile-contact', 'TALK', ACCENT_3, BG, 'Let’s talk',
         'Robotics, collaboration, and roles — get in touch.', 3.6, 2, fonts)


if __name__ == '__main__':
    main()
