#!/usr/bin/env python3
"""Build the journey map from journeys.md and gap-register.md.

Every number on the map is counted from the register; nothing is typed in by
hand. The script fails loudly on anything it cannot parse, because a silently
skipped row is a wrong number on the page.

Usage:
  python3 build-map.py --journeys journeys.md --register gap-register.md \
      --template journey-map-template.html --out journey-map.html \
      --mode brownfield|greenfield [--title "Product journey map"] [--intro "..."] \
      [--sources "..."] [--summary-heading "What the feature map is missing"]

--mode sets the default intro and summary heading (brownfield: "against what exists
today" / "What the surface is missing"; greenfield: "against the requirements" /
"What the requirements are missing"); --intro and --summary-heading override them.

Parsing contract (also stated in SKILL.md, "File formats the generator reads"):

journeys.md
  ## Part A          persona headings   ### P<n>: <Name>, <one-line descriptor>
                     the name ends at the first comma that is followed by a lowercase
                     word or a number, so "Priya Raman, Jr., a 1900 club player" keeps
                     "Priya Raman, Jr." as the name
  ## Part B          journey headings   ### J<n>: <Title> [ (demanded by ...) ] [ [round n] ]
  ## Part E          core loop lines    - **P<n> <Name>.** <first sentence names the J ids>.

gap-register.md
  walk tables        rows  | <step id> | <tag> | <note> |
                     spaces around the pipes are optional; any line that starts with a
                     pipe and a J id is a row and must have exactly the three cells, or
                     the script fails
                     step id: J<n>.<k> (spine) or J<n>.P<m>.<k> (persona variant); an
                     optional trailing letter (J2.3a) marks a step added in review
                     tag: served | served in part | awkward | missing | does not apply
                     (n/a is accepted as an alias). Only "missing" (or "missing today")
                     may carry a qualifier, and only "; planned" or "; in build",
                     optionally followed by a parenthesised note. Any other text after a
                     tag fails: "served; for a developer" and "served; awkward" are errors.
  ## Part A          optional declaration  Not walked: J<n>, J<m> (reason)
                     a journey heading with no walk rows is an error unless declared here
  ## Part B          ### Theme <n>: <name>
                     - **G<n>.<m> <Title>.** <body naming P ids, J ids and **Blocks** /
                       **Degrades** / **Nice**>
  ## Part D          one-page summary items  **<n>. <title>**

Only the Python standard library is used.
"""
import argparse
import html
import json
import re
import sys

TAG_RE = re.compile(r'^(served in part|served|awkward|missing(?: today)?|does not apply|n/a)(.*)$', re.I)
QUALIFIER_RE = re.compile(r'^\s*;\s*(planned|in build)\s*(\([^()]*\))?\s*$', re.I)
TAG_CLASS = {'served in part': 'part', 'served': 'served', 'awkward': 'awkward',
             'missing': 'missing', 'does not apply': 'na', 'n/a': 'na'}
ROW_START_RE = re.compile(r'^\s*\|\s*J\d')
STEP_ID_RE = re.compile(r'^(J\d+)(?:\.(P\d+))?\.\d+[a-z]?$')
SEV_ORDER = {'blocks': 0, 'degrades': 1, 'nice': 2}


def die(msg):
    sys.exit('build-map: ' + msg)


def section(text, start, end=None):
    i = text.find(start)
    if i < 0:
        die('missing section heading ' + repr(start))
    j = text.find(end, i + len(start)) if end else -1
    return text[i:] if j < 0 else text[i:j]


def clean(s):
    s = re.sub(r'`([^`]*)`', r'\1', s).replace('**', '')
    s = re.sub(r'\s*\[(round|pass) [^\]]*\]', '', s)
    return ' '.join(s.split())


def parse_journeys(J):
    personas = []
    for m in re.finditer(r'^### (P\d+): (.+)$', section(J, '## Part A', '## Part B'), re.M):
        head = m.group(2).strip()
        split = re.search(r',\s+(?=[a-z0-9])', head)
        if split:
            name, desc = head[:split.start()], head[split.end():]
        else:
            name, desc = head, ''
        personas.append((m.group(1), name.strip(), desc.strip()))
    if not personas:
        die('no persona headings (### P<n>: Name, descriptor) under ## Part A')
    titles = {}
    for m in re.finditer(r'^### (J\d+): (.+)$', J, re.M):
        t = m.group(2)
        t = re.sub(r'\s*\((demanded|added)[^)]*\)', '', t)
        t = re.sub(r'\s*\[round \d+[^\]]*\]', '', t).strip()
        titles[m.group(1)] = t
    if not titles:
        die('no journey headings (### J<n>: Title)')
    part_e = section(J, '## Part E')
    core = {}
    for pid, name, _ in personas:
        m = re.search(r'\*\*' + pid + r' [^*]+\*\*\s*(.+?)\.', part_e, re.S)
        if not m:
            die('no core-loop line for ' + pid + ' under ## Part E (- **' + pid + ' Name.** ...)')
        ids = []
        for x in re.findall(r'J\d+', m.group(1)):
            if x not in ids:
                ids.append(x)
        core[pid] = ids
    return personas, titles, core


def classify_tag(sid, tag):
    tm = TAG_RE.match(tag)
    if not tm:
        die('row ' + sid + ' carries a tag outside the vocabulary: ' + repr(tag))
    word, rest = tm.group(1).lower(), tm.group(2)
    if rest.strip():
        if not word.startswith('missing'):
            die('row ' + sid + ' carries text after the tag, which is outside the vocabulary: ' + repr(tag))
        if not QUALIFIER_RE.match(rest):
            die('row ' + sid + ' carries a qualifier outside the vocabulary (only "; planned" or "; in build"): ' + repr(tag))
    return TAG_CLASS[word.replace(' today', '')]


def parse_steps(G):
    steps = []
    for line in G.splitlines():
        if not ROW_START_RE.match(line):
            continue
        body = line.strip()
        if not body.endswith('|'):
            die('walk row does not end with a pipe: ' + repr(line.strip()[:80]))
        cells = [c.strip() for c in body[1:-1].split('|')]
        if len(cells) < 3:
            die('walk row has fewer than three cells (id, tag, note): ' + repr(line.strip()[:80]))
        sid, tag, note = cells[0], cells[1], ' | '.join(cells[2:])
        pm = STEP_ID_RE.match(sid)
        if not pm:
            die('walk row has a malformed step id: ' + repr(sid))
        cls = classify_tag(sid, tag)
        steps.append(dict(id=sid, j=pm.group(1), p=pm.group(2) or 'spine', tag=tag, cls=cls, note=clean(note)))
    if not steps:
        die('no walk rows (| J<n>.<k> | tag | note |) found in the register')
    ids = [s['id'] for s in steps]
    dups = sorted({i for i in ids if ids.count(i) > 1})
    if dups:
        die('duplicate step ids in the walk: ' + ', '.join(dups))
    return steps


def parse_not_walked(G):
    ids = set()
    for m in re.finditer(r'^Not walked:\s*((?:J\d+\s*,?\s*)+)', G, re.M):
        ids.update(re.findall(r'J\d+', m.group(1)))
    return ids


def parse_gaps(G):
    part_b = section(G, '## Part B', '## Part C')
    themes = [(int(t.group(1)), t.group(2).strip(), t.start())
              for t in re.finditer(r'^### Theme (\d+): (.+)$', part_b, re.M)]
    if not themes:
        die('no ### Theme <n>: headings under ## Part B')
    gaps = []
    for gm in re.finditer(r'^- \*\*(G\d+\.\d+) (.+?)\*\*(.*?)(?=^- \*\*G|^### |\Z)', part_b, re.M | re.S):
        gid, title, body = gm.group(1), gm.group(2).strip(), ' '.join(gm.group(3).split())
        sev = re.search(r'\*\*(Blocks|Degrades|Nice)\*\*', body, re.I)
        if not sev:
            die(gid + ' has no bold severity (**Blocks** / **Degrades** / **Nice**)')
        ps = sorted(set(re.findall(r'\bP\d+\b', body)), key=lambda x: int(x[1:]))
        js = sorted(set(re.findall(r'\bJ\d+', body)), key=lambda x: int(x[1:]))
        theme = [t for t in themes if t[2] < gm.start()]
        if not theme:
            die(gid + ' appears before the first theme heading')
        gaps.append(dict(id=gid, title=title.rstrip('.'), sev=sev.group(1).lower(), personas=ps, journeys=js,
                         theme=theme[-1][0], body=clean(body)))
    if not gaps:
        die('no gaps (- **G<n>.<m> Title.** ...) under ## Part B')
    by_id = {g['id']: g for g in gaps}
    for i, g in enumerate(gaps):
        ref = re.search(r'see (G\d+\.\d+)', g['body'])
        if not g['journeys'] and ref and ref.group(1) in by_id:
            g['journeys'] = by_id[ref.group(1)]['journeys']
            g['jref'] = ref.group(1)
        if not g['personas'] and 'same personas' in g['body'] and i > 0:
            g['personas'] = gaps[i - 1]['personas']
            g['pref'] = gaps[i - 1]['id']
    bad = [g['id'] for g in gaps if not (g['personas'] and g['journeys'])]
    if bad:
        die('gaps naming no persona or no journey: ' + ', '.join(bad))
    gaps.sort(key=lambda g: (SEV_ORDER[g['sev']], g['theme'], float(g['id'][1:])))
    return themes, gaps


def parse_summary(G):
    part_d = section(G, '## Part D')
    items = [(m.group(1), clean(m.group(2)).rstrip('.'))
             for m in re.finditer(r'^\*\*(\d+)\. (.+?)\*\*', part_d, re.M | re.S)]
    if not items:
        die('no summary items (**<n>. title**) under ## Part D')
    return items


def replace(page, name, content):
    b, e = '<!--BEGIN:' + name + '-->', '<!--END:' + name + '-->'
    i, j = page.find(b), page.find(e)
    if i < 0 or j < 0:
        die('template lacks the ' + name + ' markers')
    return page[:i + len(b)] + content + page[j:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--journeys', required=True)
    ap.add_argument('--register', required=True)
    ap.add_argument('--template', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--mode', choices=['brownfield', 'greenfield'], required=True)
    ap.add_argument('--title', default='Journey map')
    ap.add_argument('--intro', default=None)
    ap.add_argument('--sources', default='journeys.md (pass 1), gap-register.md (pass 2), review.md (pass 3).')
    ap.add_argument('--summary-heading', default=None)
    a = ap.parse_args()
    mode_words = {'brownfield': ('against what exists today', 'What the surface is missing'),
                  'greenfield': ('against the signed-off requirements', 'What the requirements are missing')}
    against, default_heading = mode_words[a.mode]
    if a.summary_heading is None:
        a.summary_heading = default_heading

    J = open(a.journeys, encoding='utf-8').read()
    G = open(a.register, encoding='utf-8').read()
    page = open(a.template, encoding='utf-8').read()

    personas, titles, core = parse_journeys(J)
    steps = parse_steps(G)
    themes, gaps = parse_gaps(G)
    summary = parse_summary(G)

    journeys = sorted(titles, key=lambda x: int(x[1:]))
    unknown_j = sorted({s['j'] for s in steps} - set(titles))
    if unknown_j:
        die('walk rows for journeys with no heading in journeys.md: ' + ', '.join(unknown_j))
    unknown_p = sorted({s['p'] for s in steps if s['p'] != 'spine'} - {p[0] for p in personas})
    if unknown_p:
        die('walk rows for personas with no heading in journeys.md: ' + ', '.join(unknown_p))
    not_walked = parse_not_walked(G)
    unwalked = sorted(set(titles) - {s['j'] for s in steps} - not_walked, key=lambda x: int(x[1:]))
    if unwalked:
        die('journeys with a heading in journeys.md but no walk rows in the register: ' + ', '.join(unwalked)
            + ' (tag them, or declare them with a "Not walked: J<n>" line in Part A)')
    walked_but_declared = sorted(not_walked & {s['j'] for s in steps})
    if walked_but_declared:
        die('journeys declared "Not walked" that have walk rows: ' + ', '.join(walked_but_declared))

    totals = {c: sum(1 for s in steps if s['cls'] == c) for c in ['served', 'part', 'awkward', 'missing', 'na']}
    E = html.escape

    def dots(cell):
        return ''.join('<i class="d %s" title="%s: %s"></i>' % (s['cls'], E(s['id']), E(s['tag'])) for s in cell)

    cols = ['spine'] + [p[0] for p in personas]
    rows = []
    for j in journeys:
        tds = ['<th scope="row" title="%s"><span class="jid">%s</span> <span class="jt">%s</span></th>' % (E(titles[j]), j, E(titles[j]))]
        for c in cols:
            cell = [s for s in steps if s['j'] == j and s['p'] == c]
            if cell:
                label = '%s %s: %d step%s' % (j, c, len(cell), '' if len(cell) == 1 else 's')
                tds.append('<td><button type="button" class="cell" data-key="%s-%s" aria-label="%s">%s</button></td>' % (j, c, E(label), dots(cell)))
            else:
                tds.append('<td><span class="cell empty" aria-hidden="true"></span></td>')
        rows.append('<tr>' + ''.join(tds) + '</tr>')
    grid = ('<thead><tr><th scope="col">Journey</th><th scope="col" class="sp">Spine</th>'
            + ''.join('<th scope="col" title="%s">%s</th>' % (E(p[1]), p[0]) for p in personas)
            + '</tr></thead><tbody>' + ''.join(rows) + '</tbody>')

    celldata = {}
    for s in steps:
        celldata.setdefault('%s-%s' % (s['j'], s['p']), []).append(dict(id=s['id'], cls=s['cls'], tag=s['tag'], note=s['note']))

    tiles = ''.join('<div class="tile"><b>%s %s</b><span>%s</span><em>Core loop: %s</em></div>'
                    % (pid, E(name), E(desc), ', '.join(core[pid])) for pid, name, desc in personas)

    legend = ''.join([
        '<span><i class="d served"></i> served, filled circle (%d)</span>' % totals['served'],
        '<span><i class="d part"></i> served in part, half circle (%d)</span>' % totals['part'],
        '<span><i class="d awkward"></i> awkward, diamond (%d)</span>' % totals['awkward'],
        '<span><i class="d missing"></i> missing incl. planned or in build, square (%d)</span>' % totals['missing'],
        '<span><i class="d na"></i> does not apply, hollow (%d)</span>' % totals['na']])

    gap_html = ''.join(
        '<details class="gap %s"><summary><span class="sev">%s</span> <b>%s</b> %s<span class="meta">hits %s%s · breaks %s%s · theme %d</span></summary><p>%s</p></details>'
        % (g['sev'], g['sev'], g['id'], E(g['title']), ', '.join(g['personas']),
           (' (via ' + g['pref'] + ')') if g.get('pref') else '', ', '.join(g['journeys']),
           (' (via ' + g['jref'] + ')') if g.get('jref') else '', g['theme'], E(g['body'])) for g in gaps)
    sev_counts = {k: sum(1 for g in gaps if g['sev'] == k) for k in SEV_ORDER}
    register = ('<h2>Gap register, blocks first (%d gaps: %d block, %d degrade, %d nice)</h2>%s'
                '<div class="summary"><h2>%s</h2><ol>%s</ol><ul class="themes">%s</ul></div>'
                % (len(gaps), sev_counts['blocks'], sev_counts['degrades'], sev_counts['nice'], gap_html, E(a.summary_heading),
                   ''.join('<li><b>%s.</b> %s</li>' % (n, E(t)) for n, t in summary),
                   ''.join('<li>%d: %s</li>' % (n, E(t)) for n, t, _ in themes)))

    intro = a.intro or ('%d people, %d journeys, %d tagged steps %s. Click or focus a cell to read its steps; open a gap to read it. The person\'s words throughout.'
                        % (len(personas), len(journeys), len(steps), against))
    footer = ('<p><b>Sources.</b> %s</p>'
              '<p><b>Count method.</b> Every number on this page is a count of rows in the walk tables of %s, one row per step id (%d rows), grouped by the tag in the row\'s second column: '
              '"served in part" counts as served in part; "missing" with any qualifier (planned, in build) counts as missing; "does not apply" (or n/a) is does not apply. '
              'Gap severities, personas and journeys are read from Part B of the same file (%d gaps); the summary items from its Part D (%d items). Nothing here is estimated.</p>'
              % (E(a.sources), E(a.register.split('/')[-1]), len(steps), len(gaps), len(summary)))

    for name, content in [('TITLE', E(a.title)), ('HEADING', E(a.title)), ('INTRO', E(intro)), ('LEGEND', legend),
                          ('PERSONAS', tiles), ('GRID', grid), ('REGISTER', register), ('FOOTER', footer),
                          ('DATA', json.dumps(celldata, ensure_ascii=False).replace('</', '<\\/')),
                          ('NAMES', json.dumps({'personas': {p[0]: p[1] for p in personas}, 'titles': titles}, ensure_ascii=False).replace('</', '<\\/'))]:
        page = replace(page, name, content)
    open(a.out, 'w', encoding='utf-8').write(page)
    print('mode %s personas %d journeys %d (%d not walked by declaration) steps %d totals %s gaps %d (%s) summary %d -> %s'
          % (a.mode, len(personas), len(journeys), len(not_walked), len(steps), json.dumps(totals), len(gaps), json.dumps(sev_counts), len(summary), a.out))


if __name__ == '__main__':
    main()
