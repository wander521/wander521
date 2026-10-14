"""Render real public GitHub contribution cells as a self-contained SVG snake."""
import argparse
import datetime as dt
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import urllib.request

class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = []
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if data.get('data-date') and data.get('data-level') is not None:
            date = dt.date.fromisoformat(data['data-date'])
            self.cells.append({'date': date.isoformat(), 'x': int(data['data-ix']),
                               'y': (date.weekday() + 1) % 7, 'level': int(data['data-level'])})

def render(cells, dark, animated):
    colors = ['#161b22', '#0e4429', '#006d32', '#26a641', '#39d353'] if dark else ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39']
    stroke = '#30363d' if dark else '#d1d9e0'
    ink = '#bcc9d8' if dark else '#59636e'
    origin, step, size = 20, 16, 11
    width = origin * 2 + 53 * step
    path = [(0, 3)]
    targets = sorted([c for c in cells if c['level']], key=lambda c:(c['x'],c['y']))
    targets += [{'x': 52, 'y': 6}, {'x': 0, 'y': 6}, {'x': 0, 'y': 3}]
    for target in targets:
        x, y = path[-1]
        while x != target['x']:
            x += 1 if x < target['x'] else -1
            path.append((x,y))
        while y != target['y']:
            y += 1 if y < target['y'] else -1
            path.append((x,y))
    point = lambda p: (origin + p[0]*step + size/2, 38 + p[1]*step + size/2)
    motion = 'M' + ' L'.join(f'{point(p)[0]},{point(p)[1]}' for p in path)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="176" viewBox="0 0 {width} 176" role="img" aria-label="Public GitHub contributions for wander521, animated as a snake">',
           '<title>Public GitHub Activity · wander521</title>',
           '<desc>Cells come from the public GitHub contribution calendar. The snake consumes the existing contribution cells; counts are not fabricated.</desc>',
           f'<text x="20" y="18" fill="{ink}" font-family="Arial,sans-serif" font-size="12">PUBLIC CONTRIBUTIONS</text>',
           f'<text x="{width-20}" y="18" fill="{ink}" text-anchor="end" font-family="Arial,sans-serif" font-size="12">{cells[0]["date"]} — {max(c["date"] for c in cells)}</text>']
    for c in cells:
        x,y = origin+c['x']*step,38+c['y']*step
        out.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="2" fill="{colors[c["level"]]}" stroke="{stroke}" stroke-width=".5"><title>{c["date"]}: contribution level {c["level"]}</title>')
        if animated and c['level'] and (c['x'],c['y']) in path:
            fraction=path.index((c['x'],c['y'])) / (len(path)-1)
            t=max(.001,min(.94,fraction))
            out.append(f'<animate attributeName="fill" values="{colors[c["level"]]};{colors[c["level"]]};{colors[0]};{colors[0]};{colors[c["level"]]}" keyTimes="0;{t:.5f};{t+.001:.5f};.98;1" dur="22s" repeatCount="indefinite"/>')
        out.append('</rect>')
    if animated:
        for i in range(5,-1,-1):
            out.append(f'<rect x="-5.5" y="-5.5" width="11" height="11" rx="3" fill="{"#a78bfa" if i else "#c4b5fd"}" opacity="{1-i*.105}"><animateMotion path="{motion}" dur="22s" begin="{-i*.13}s" repeatCount="indefinite"/></rect>')
    out += [f'<text x="20" y="172" fill="{ink}" font-family="Arial,sans-serif" font-size="11">A little motion for the work behind the code.</text>', '</svg>']
    return '\n'.join(out)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--html')
    args = parser.parse_args()
    if args.html:
        source = Path(args.html).read_text()
    else:
        request = urllib.request.Request('https://github.com/users/wander521/contributions',headers={'User-Agent':'wander521-profile-activity'})
        with urllib.request.urlopen(request,timeout=30) as response:
            source = response.read().decode()
    calendar = Calendar()
    calendar.feed(source)
    if len(calendar.cells) < 300:
        raise RuntimeError('Contribution calendar missing or incomplete; preserve the previous images.')
    root = Path(__file__).resolve().parents[1] / 'assets'
    root.mkdir(exist_ok=True)
    for dark in [False,True]:
        for animated in [False,True]:
            name = 'activity-' + ('dark' if dark else 'light') + ('' if animated else '-static') + '.svg'
            (root / name).write_text(render(calendar.cells,dark,animated))
    (root / 'activity-data.json').write_text(json.dumps({'source':'https://github.com/users/wander521/contributions','cells':calendar.cells},indent=2)+'\n')
    print(f'Generated snake from {len(calendar.cells)} real calendar cells; {sum(c["level"]>0 for c in calendar.cells)} active days.')
