#!/usr/bin/env python3
"""Self-contained GitHub profile SVG card builder + contribution fetcher.

Usage:
  python scripts/render_cards.py --fetch     # GH_TOKEN or GITHUB_TOKEN required
  python scripts/render_cards.py             # reads data/contributions.json
  STATIC=1 python scripts/render_cards.py    # final animation frame

No third-party Python packages needed. Font embedding requires `pyftsubset`.
Font paths and colors are explicit configuration, not scraped website claims.
"""
from __future__ import annotations

import argparse
import base64
import calendar
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

# EDIT THESE after inspecting your portfolio's actual CSS variables.
# The live portfolio HTML did not expose verifiable CSS tokens in this environment.
BG = '#0B1220'
PANEL = '#111C2E'
PANEL_2 = '#152338'
BORDER = '#2B3C53'
TEXT = '#EAF3F8'
MUTED = '#91A8BA'
ACCENT = '#A7F36D'       # brand color — single source of truth
ACCENT_2 = '#65D6CF'
def system_font(name, fallback):
    try:
        return subprocess.check_output(['fc-match','-f','%{file}', name], text=True).strip() or fallback
    except (OSError, subprocess.CalledProcessError):
        return fallback

FONT_REG = os.environ.get('FONT_REG') or system_font('Inter:style=Regular','/usr/share/fonts/truetype/inter/Inter-Regular.otf')
FONT_BOLD = os.environ.get('FONT_BOLD') or system_font('Inter:style=Bold','/usr/share/fonts/truetype/inter/Inter-Bold.otf')
FONT_MONO = os.environ.get('FONT_MONO') or system_font('DejaVu Sans Mono','/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')
STATIC = os.environ.get('STATIC') == '1'

PROJECTS = [
    ('vision', 'Schrödinger’s Vision', 'MULTI-CAMERA / AUTONOMY',
     '4 cameras · 13 driving sequences · 15+ models',
     'Lane & object detection / tracking / depth / optical flow',
     'https://github.com/Schrodingerrs-cat/MultiCam-AutonomousDriving-Perception'),
    ('vio', 'Visual–Inertial Odometry', 'ESTIMATION / DEEP + CLASSICAL',
     'CNN + LSTM versus S-MSCKF',
     'Synthetic Blender training / EuRoC + Vicon evaluation',
     'https://aryanshah.work/'),
    ('cansat', 'CanSat · Team Dyaus', 'EMBEDDED / FLIGHT HARDWARE',
     '8-person team · 2nd nationally · SMOPS 2023',
     'Reaction wheels / RF telemetry / sensor fusion',
     'https://aryanshah.work/'),
    ('quad', 'Crazyflie Controls', 'CONTROL / UAV',
     'Cascaded PD + SO(3) attitude control',
     '18+ gain sweeps / 3–4.5 s settling time',
     'https://aryanshah.work/'),
    ('nerf', 'NeRF + Structure from Motion', '3D VISION / RECONSTRUCTION',
     'Volumetric rendering / hierarchical sampling',
     'Camera geometry / pose estimation / bundle adjustment',
     'https://aryanshah.work/'),
]


def esc(value):
    return html.escape(str(value), quote=True)


def fetch_data():
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not token:
        raise RuntimeError('Set GH_TOKEN (or GITHUB_TOKEN) for --fetch')
    # GitHub's calendar is returned in the API account's configured date boundaries.
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
    days = sorted(({'date': d['date'], 'count': d['contributionCount']}
                   for w in cal['weeks'] for d in w['contributionDays']), key=lambda d: d['date'])
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps({'username': USERNAME,
        'retrieved_at': datetime.now(timezone.utc).isoformat(),
        'source': 'GitHub GraphQL contributionsCollection.contributionCalendar',
        'days': days}, indent=2) + '\n', encoding='utf-8')
    print('Fetched', len(days), 'days of GitHub activity')


def load_data():
    if not DATA.exists():
        return []
    raw = json.loads(DATA.read_text(encoding='utf-8'))
    if raw.get('username') != USERNAME:
        raise ValueError('contributions.json username mismatch')
    days = raw.get('days', [])
    seen = set()
    for d in days:
        date.fromisoformat(d['date'])
        if d['date'] in seen or not isinstance(d['count'], int) or d['count'] < 0:
            raise ValueError('invalid or duplicated contribution date')
        seen.add(d['date'])
    return sorted(days, key=lambda d: d['date'])


def subset_font(path, chars):
    """Subset font into WOFF, embedding only glyphs actually used in cards."""
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


def font_css():
    # All written copy, numbers, labels and potential month/day names are in this whitelist.
    chars = ''.join(chr(i) for i in range(32, 127)) + '–—·’→×°≥≤Σéöꞏ✓•'
    regular = subset_font(FONT_REG, chars)
    bold = subset_font(FONT_BOLD, chars)
    mono = subset_font(FONT_MONO, chars)
    return (f"@font-face{{font-family:InterCard;src:url(data:font/woff;base64,{regular}) format('woff');font-weight:400}}"
            f"@font-face{{font-family:InterCard;src:url(data:font/woff;base64,{bold}) format('woff');font-weight:700}}"
            f"@font-face{{font-family:MonoCard;src:url(data:font/woff;base64,{mono}) format('woff')}}")


def text(x,y,s,size=16,color=TEXT,weight=400,family='InterCard',extra=''):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" {extra}>{esc(s)}</text>')


def svg(name, width, height, content, delay=0, fonts=''):
    css = f'''{fonts}
    .enter{{opacity:1;transform:none}}
    .grow{{transform:scaleY(1);transform-box:fill-box;transform-origin:center bottom}}
    .fade{{opacity:1}}
    .scan{{opacity:.3}}
    @keyframes rise{{from{{opacity:0;transform:translateY(17px)}}to{{opacity:1;transform:translateY(0)}}}}
    @keyframes grow{{from{{transform:scaleY(.06)}}to{{transform:scaleY(1)}}}}
    @keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
    @keyframes pulse{{0%,100%{{opacity:.12}}50%{{opacity:.5}}}}
    @keyframes sweep{{from{{transform:translateX(-100%)}}to{{transform:translateX(180%)}}}}
    '''
    if not STATIC:
        css += f'''
        .enter{{opacity:0;animation:rise .8s cubic-bezier(.18,.7,.15,1) {delay:.2f}s both}}
        .fade{{opacity:0;animation:fade .85s ease {delay+.2:.2f}s both}}
        .grow{{transform:scaleY(.06);animation:grow .85s cubic-bezier(.15,.75,.2,1) {delay+.3:.2f}s both}}
        .scan{{opacity:.12;animation:pulse 4s ease-in-out {delay:.2f}s infinite}}
        .sweep{{animation:sweep 4.4s ease-in-out {delay:.2f}s infinite}}
        '''
    css += '''@media (prefers-reduced-motion: reduce){
       *,*::before,*::after{animation:none!important;transition:none!important}
       .enter,.fade{opacity:1!important;transform:none!important}
       .grow{transform:scaleY(1)!important}
       .scan{opacity:.3!important}
    }'''
    # CSS only: SMIL intentionally excluded since SMIL reductions are not uniformly controllable.
    result = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
              f'viewBox="0 0 {width} {height}" role="img" aria-label="{esc(name)}">'
              f'<title>{esc(name)}</title><style>{css}</style>'
              f'<rect width="{width}" height="{height}" rx="22" fill="{BG}"/>'
              f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="21" fill="none" stroke="{BORDER}"/>'
              f'{content}</svg>')
    path = CARDS / (name + '.svg')
    path.write_text(result, encoding='utf-8')
    print(f'Wrote {path.relative_to(ROOT)} ({path.stat().st_size // 1024} KB)')


def grid_lines(w,h):
    return ''.join(f'<path d="M{x} 0V{h}" stroke="{ACCENT}" stroke-opacity=".045"/>'
                   for x in range(40,w,42))


def hero(fonts):
    content = grid_lines(960,272)
    content += f'<rect x="36" y="34" width="8" height="8" rx="4" fill="{ACCENT}"/>'
    content += text(58,43,'ROBOTICS / PERCEPTION / EMBODIED AI',12,ACCENT,family='MonoCard')
    content += '<g class="enter">' + text(35,126,'ARYAN SHAH',72,TEXT,700) + '</g>'
    content += '<g class="enter">' + text(38,173,'i teach machines to see, reason, and occasionally avoid running into things.',20,MUTED) + '</g>'
    content += f'<path d="M38 205 H922" stroke="{BORDER}"/>'
    content += text(38,237,'WPI  /  ROBOCARE LAB',13,ACCENT_2,family='MonoCard')
    content += text(922,237,'SCHRÖDINGER’S VISION  /  2026',12,MUTED,family='MonoCard',extra='text-anchor="end"')
    # Optional PNG/JPEG portrait may be embedded as a data URL, never externally fetched.
    portrait = ROOT / 'assets' / 'portrait.png'
    if portrait.exists():
        raw = base64.b64encode(portrait.read_bytes()).decode()
        content += '<defs><clipPath id="portraitClip"><circle cx="845" cy="100" r="58"/></clipPath></defs>'
        content += f'<image href="data:image/png;base64,{raw}" x="787" y="42" width="116" height="116" preserveAspectRatio="xMidYMid slice" clip-path="url(#portraitClip)"/>'
    svg('hero',960,272,content,0.15,fonts)


def tile(name,title,subtitle,number,delay,fonts):
    content = (f'<circle cx="41" cy="41" r="7" fill="{ACCENT}"/>'
               + text(26,107,title,27,TEXT,700)
               + text(26,145,subtitle,13,MUTED)
               + f'<path d="M26 169H274" stroke="{BORDER}"/>')
    content += text(26,194,number,12,ACCENT,family='MonoCard')
    content += text(278,52,'↗',23,ACCENT,extra='text-anchor="end"')
    svg(name,300,220,'<g class="enter">'+content+'</g>',delay,fonts)


def stats(days):
    counts = {d['date']:d['count'] for d in days}
    today = datetime.now(timezone.utc).date()
    eligible = [date.fromisoformat(d) for d,c in counts.items() if c>0 and date.fromisoformat(d)<=today]
    active = len(eligible)
    busiest = max(days, key=lambda d:d['count']) if days else None
    # A current streak continues through yesterday if there are no contributions today.
    cursor = today if counts.get(today.isoformat(),0)>0 else today-timedelta(days=1)
    streak = 0
    while counts.get(cursor.isoformat(),0)>0:
        streak += 1
        cursor -= timedelta(days=1)
    months = defaultdict(int)
    for d in days:
        months[d['date'][:7]] += d['count']
    return active, streak, busiest, months


def activity(days,fonts):
    active,streak,busiest,monthly = stats(days)
    loaded = bool(days)
    if loaded:
        keys = sorted(monthly)[-12:]
        values = [monthly[k] for k in keys]
    else:
        keys,values = [],[]
    content = text(35,51,'ACTIVITY / LAST 12 MONTHS',15,ACCENT,family='MonoCard')
    content += text(35,88,'Contribution rhythm',30,TEXT,700)
    content += f'<path d="M35 110H925" stroke="{BORDER}"/>'
    headings = [('CURRENT STREAK',str(streak) if loaded else '—'),
                ('ACTIVE DAYS',str(active) if loaded else '—'),
                ('BUSIEST DAY',str(busiest['count']) if loaded and busiest else '—')]
    for i,(head,val) in enumerate(headings):
        x = 38+i*300
        content += '<g class="enter">'+text(x,151,head,12,MUTED,family='MonoCard')+text(x,195,val,42,TEXT,700)+'</g>'
        if i==2 and busiest:
            content += text(x+72,190,busiest['date'],13,MUTED,family='MonoCard')
    content += f'<path d="M35 216H925" stroke="{BORDER}"/>'
    for i in range(5):
        y=390-i*34
        content += f'<path d="M38 {y}H924" stroke="{BORDER}" stroke-dasharray="3 7"/>'
    if loaded and keys:
        peak = max(1,max(values))
        gap = 11
        bw = (876 - gap*(len(keys)-1)) / len(keys)
        for i,(key,value) in enumerate(zip(keys,values)):
            x=42+i*(bw+gap)
            bh=max(3,145*value/peak) if value>0 else 2
            content += (f'<rect class="grow" x="{x:.1f}" y="{390-bh:.1f}" width="{bw:.1f}" '
                        f'height="{bh:.1f}" rx="4" fill="{ACCENT}" fill-opacity="{.95 if value else .25}"/>')
            content += text(x+bw/2,417,key[5:],11,MUTED,family='MonoCard',extra='text-anchor="middle"')
        content += text(921,240,f'PEAK {peak} / MONTH',11,MUTED,family='MonoCard',extra='text-anchor="end"')
    else:
        content += text(480,320,'Waiting for GitHub GraphQL contribution data',16,MUTED,extra='text-anchor="middle"')
    content += text(38,457,'Source: GitHub contribution calendar  /  UTC daily snapshot',12,MUTED,family='MonoCard')
    svg('activity',960,480,content,1.05,fonts)


def project_card(i,p,fonts):
    slug,title,kicker,metric,detail,url=p
    y=45
    content = f'<circle cx="39" cy="42" r="5" fill="{ACCENT}"/>'
    content += text(57,47,kicker,12,ACCENT,family='MonoCard')
    content += '<g class="enter">' + text(35,109,title,33,TEXT,700) + '</g>'
    content += text(37,157,metric,19,ACCENT_2)
    content += text(37,195,detail,16,MUTED)
    content += f'<path d="M35 224H925" stroke="{BORDER}"/>'
    content += text(37,253,'SELECTED BUILD  /  '+str(i+1).zfill(2),12,MUTED,family='MonoCard')
    content += text(920,253,'VIEW PROJECT ↗',12,ACCENT,family='MonoCard',extra='text-anchor="end"')
    svg('repo-'+slug,960,278,content,1.65+i*.25,fonts)


def contributions(days,fonts):
    content = text(35,50,'CONTRIBUTION MAP',15,ACCENT,family='MonoCard')
    content += text(35,87,'A year in commits and other contributions',26,TEXT,700)
    content += text(925,87,'GitHub / daily activity',12,MUTED,family='MonoCard',extra='text-anchor="end"')
    counts = {d['date']:d['count'] for d in days}
    if counts:
        end = max(date.fromisoformat(k) for k in counts)
        start = end-timedelta(days=364)
        # Align to week columns starting Sunday (no fake days counted).
        start -= timedelta(days=(start.weekday()+1)%7)
        week_count = ((end-start).days//7)+1
        cell = min(13.4, 865/week_count-3)
        gap = 3
        left = 46
        top = 137
        for n in range((end-start).days+1):
            d=start+timedelta(days=n)
            value=counts.get(d.isoformat())
            if value is None:
                color=PANEL_2
            elif value==0: color='#1E2C3D'
            elif value<3: color='#355C42'
            elif value<6: color='#588F50'
            elif value<10: color='#79BA5D'
            else: color=ACCENT
            x = left+(n//7)*(cell+gap)
            y = top+(n%7)*(cell+gap)
            if x+cell>927: break
            content += f'<rect class="fade" x="{x:.2f}" y="{y:.2f}" width="{cell:.2f}" height="{cell:.2f}" rx="2.2" fill="{color}"/>'
        content += text(37,281,'DARKER  /  LESS',11,MUTED,family='MonoCard')
        for i,c in enumerate(['#1E2C3D','#355C42','#588F50','#79BA5D',ACCENT]):
            content += f'<rect x="{175+i*21}" y="270" width="13" height="13" rx="2" fill="{c}"/>'
        content += text(292,281,'MORE',11,MUTED,family='MonoCard')
    else:
        content += text(37,171,'No contribution snapshot yet. The daily Action will populate this graph.',16,MUTED)
    svg('contributions',960,309,content,3.05,fonts)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--fetch',action='store_true',help='Refresh data from GitHub GraphQL first')
    args=parser.parse_args()
    if args.fetch:fetch_data()
    CARDS.mkdir(parents=True,exist_ok=True)
    days=load_data()
    fonts=font_css()
    hero(fonts)
    tile('tile-work','PROJECTS','Selected engineering builds','01 / EXPLORE',.45,fonts)
    tile('tile-site','PORTFOLIO','Research / experience / writing','02 / EXPLORE',.55,fonts)
    tile('tile-contact','LET’S TALK','Robotics / collaboration / roles','03 / CONNECT',.65,fonts)
    activity(days,fonts)
    for i,p in enumerate(PROJECTS):project_card(i,p,fonts)
    contributions(days,fonts)

if __name__=='__main__': main()
