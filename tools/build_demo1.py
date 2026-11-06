"""Build the Demo 1 section of index.html from data/demo1.json.

Usage (from the site root):
  python tools/build_demo1.py            # rebuild index.html
  python tools/build_demo1.py --sync     # copy renders from sync.source_root first
  python tools/build_demo1.py --watch    # rebuild whenever the data or assets change
"""
import argparse
import json
import shutil
import time
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- DEMO1:START -->", "<!-- DEMO1:END -->"
STATE_LABELS = {"new": "新增", "updated": "更新", "used": "调用", "kept": "保留"}
LOOP_LABELS = ["观察", "判断", "改 harness", "工作区结果"]

# Each scene is a tiny wireframe: action -> result. Stages pick one by name in demo1.json.
SCENES = {
    "loop": '''<div class="scene scene-loop">
  <svg class="loop-ring" viewBox="0 0 126 118"><path class="loop-path" pathLength="1" d="M63 26a33 33 0 1 1-28.6 16.5"/><path class="loop-arrow" pathLength="1" d="m31 36 3 8 8-3"/></svg>
  <span class="agent-node"></span>
  <span class="slot slot-a"></span><span class="slot slot-b"></span><span class="slot slot-c"></span>
</div>''',
    "tool": '''<div class="scene scene-tool">
  <span class="mini-card tool-card"><i class="tool-glyph"></i><i class="bar heading w34"></i><i class="bar w28"></i></span>
  <span class="connector"></span>
  <span class="mini-window deck-window"><span class="tabstrip"><i class="tab active"></i><i class="tab"></i></span><i class="bar heading w34"></i><i class="bar w42"></i><i class="bar w30"></i><i class="result-line"></i></span>
</div>''',
    "review": '''<div class="scene scene-review">
  <span class="mini-window review-window"><span class="tabstrip"><i class="tab active"></i></span><i class="bar heading w52"></i><i class="bar w62"></i><i class="metric m1"></i><i class="metric m2"></i><i class="missing-art"></i></span>
  <span class="lens"></span><span class="issue-ring"></span>
</div>''',
    "extend": '''<div class="scene scene-extend">
  <span class="mini-card builder-stack"><i class="version-dot d1"></i><i class="version-dot d2"></i><i class="version-dot d3"></i><i class="version-dot d4"></i><i class="bar heading w30"></i><i class="bar w24"></i></span>
  <span class="mini-window art-window"><span class="tabstrip"><i class="tab active"></i></span><i class="bar heading w38"></i><i class="art-slot"><i class="art-sun"></i><i class="art-hill"></i></i><i class="check-badge"></i></span>
</div>''',
    "gate": '''<div class="scene scene-gate">
  <span class="mini-window checklist"><span class="tabstrip"><i class="tab active"></i></span><i class="check-row r1"><b></b><i class="bar w42"></i></i><i class="check-row r2"><b></b><i class="bar w34"></i></i><i class="check-row r3"><b></b><i class="bar w38"></i></i><i class="check-row r4"><b></b><i class="bar w28"></i></i></span>
  <span class="mini-card file-card"><i class="file-fold"></i><i class="bar heading w24"></i><i class="bar w18"></i></span>
</div>''',
    "auditor": '''<div class="scene scene-auditor">
  <span class="mini-window final-deck"><span class="tabstrip"><i class="tab active"></i></span><i class="bar heading w34"></i><i class="bar w30"></i><i class="final-art"></i><i class="approval-seal"></i></span>
  <span class="mini-card auditor-card"><i class="eye"></i><i class="bar w18"></i></span>
</div>''',
}
ICONS = {
    "loop": '<path pathLength="1" d="M19 8a8 8 0 1 0 1.2 8"/><path pathLength="1" d="M19 3v5h-5"/>',
    "tool": '<path pathLength="1" d="M14 6l4 4-8 8H6v-4z"/><path pathLength="1" d="M12 8l4 4"/>',
    "review": '<circle pathLength="1" cx="10.5" cy="10.5" r="5.5"/><path pathLength="1" d="m15 15 4.5 4.5"/>',
    "extend": '<path pathLength="1" d="m12 3 8 4-8 4-8-4z"/><path pathLength="1" d="m4 12 8 4 8-4"/><path pathLength="1" d="m4 17 8 4 8-4"/>',
    "gate": '<path pathLength="1" d="M12 3 19 6v5c0 5-3 8-7 10-4-2-7-5-7-10V6z"/><path pathLength="1" d="m8.5 12 2.4 2.4 4.8-5"/>',
    "auditor": '<path pathLength="1" d="M3 12s3.5-6 9-6 9 6 9 6-3.5 6-9 6-9-6-9-6z"/><circle pathLength="1" cx="12" cy="12" r="2.5"/>',
}


def load(data_path):
    data = json.loads(data_path.read_text(encoding="utf-8"))
    lanes = {lane["id"] for lane in data["lanes"]}
    problems = []
    for key, comp in data["components"].items():
        if comp["lane"] not in lanes:
            problems.append(f"component {key}: unknown lane {comp['lane']}")
    assets = [stage["workspace"]["image"] for stage in data["stages"]]
    assets += [stage["workspace"].get("link") for stage in data["stages"]]
    assets += [data["proof"]["before"][1], data["proof"]["after"][1], data["proof"]["link"]]
    assets += [comp.get("link") for comp in data["components"].values()]
    for n, stage in enumerate(data["stages"]):
        if stage["scene"] not in SCENES:
            problems.append(f"stage {n}: unknown scene {stage['scene']} (choose from {', '.join(SCENES)})")
        for key, state in stage["harness"].items():
            if key not in data["components"]:
                problems.append(f"stage {n}: unknown component {key}")
            if not set(state.split()) <= STATE_LABELS.keys():
                problems.append(f"stage {n}: unknown state '{state}' for {key}")
        for event in stage["events"]:
            if event.get("lane", "prompts") not in lanes:
                problems.append(f"stage {n}: unknown event lane {event['lane']}")
    problems += [f"missing asset: {path}" for path in assets if path and not (ROOT / path).exists()]
    if problems:
        raise SystemExit("demo1.json has problems:\n  " + "\n  ".join(problems))
    return data


def render(data):
    e = escape
    comps, lanes, stages = data["components"], data["lanes"], data["stages"]
    out = [f'''<section class="evo section" id="demo-ppt">
  <header class="evo-intro">
    <div><div class="eyebrow dark">{e(data["eyebrow"])}</div><h2>{data["title"]}</h2></div>
    <p>{e(data["intro"])}</p>
  </header>
  <div class="evo-metrics" aria-label="Demo 1 演进结果">''']
    out += [f'    <span><b>{e(v)}</b>{e(label)}</span>' for v, label in data["metrics"]]
    out.append(f'''  </div>

  <div class="feature-grid" aria-label="Demo 1 的 {len(stages)} 个演进阶段">''')
    for n, s in enumerate(stages):
        out.append(f'''    <a class="feature-tile" href="#stage-{n}" data-tile data-stage="{n}">
      <div class="art-panel" aria-hidden="true">
        {SCENES[s["scene"]]}
      </div>
      <div class="tile-copy">
        <span class="icon-chip" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONS[s["scene"]]}</svg></span>
        <span class="tile-kicker">{n:02d} · {e(s["batches"])}</span>
        <h3>{e(s["label"])}</h3>
        <p>{e(s["tile_text"])}</p>
        <div class="tile-delta"><span>{e(s["tile_delta"][0])}</span><span>{e(s["tile_delta"][1])}</span></div>
      </div>
    </a>''')
    out.append('''  </div>

  <div class="studio" id="demo1-studio" data-studio>
    <div class="studio-bar">
      <div class="stepper" role="tablist" aria-label="选择阶段">''')
    for n, s in enumerate(stages):
        out.append(f'        <button type="button" role="tab" id="stage-{n}" data-step="{n}" aria-controls="stage-panel-{n}" aria-selected="{str(n == 0).lower()}"><b>{n:02d}</b><span>{e(s["label"])}</span></button>')
    out.append(f'''      </div>
      <div class="studio-controls">
        <button type="button" data-prev aria-label="上一阶段">←</button>
        <button type="button" data-play aria-pressed="false"><span>自动回放</span></button>
        <button type="button" data-next aria-label="下一阶段">→</button>
      </div>
    </div>
    <div class="studio-progress" aria-hidden="true"><i></i></div>
    <div class="studio-panels">''')
    previous_count = 0
    dirs = {lane["id"]: lane["dir"] for lane in lanes}
    for n, s in enumerate(stages):
        harness, ws = s["harness"], s["workspace"]
        count = sum(1 for key in harness if comps[key].get("counted", True))
        used = [key for key, state in harness.items() if "used" in state.split()]
        changed = [key for key, state in harness.items() if {"new", "updated"} & set(state.split())]
        used_chips = "".join(f'<span class="chip lane-{comps[k]["lane"]}">{e(dirs[comps[k]["lane"]] + comps[k]["path"])}</span>' for k in used) or '<span class="none">无</span>'
        out.append(f'''      <article class="stage-panel" id="stage-panel-{n}" role="tabpanel" aria-labelledby="stage-{n}"{" data-active" if n == 0 else ""}>
        <header class="stage-head">
          <div class="stage-copy"><span class="stage-kicker">{n:02d} · {e(s["batches"])}</span><h3>{e(s["title"])}</h3><p>{e(s["summary"])}</p></div>
          <div class="stage-side">
            <div class="stage-count"><b>{previous_count} → {count}</b><span>Agent 组件 · {len(changed)} 个变更 · {len(used)} 个被调用</span></div>
            <div class="stage-used"><b>本阶段调用</b>{used_chips}</div>
          </div>
        </header>
        <div class="stage-grid">
          <section class="pane trace-pane" aria-label="Agent 轨迹">
            <div class="pane-head"><b>AGENT TRACE</b><span>一次 loop 的四步</span></div>
            <ol class="loop-steps">''')
        previous_count = count
        out += [f'              <li style="--i:{i}"><span>{LOOP_LABELS[i]}</span><p>{e(text)}</p></li>' for i, text in enumerate(s["loop"])]
        out.append('''            </ol>
            <div class="pane-head sub"><b>EVENTS</b><span>运行记录（UTC）</span></div>
            <ol class="events">''')
        for i, ev in enumerate(s["events"]):
            lane = ev.get("lane", "runtime")
            fail = ' class="fail"' if ev.get("fail") else ""
            out.append(f'              <li style="--i:{i + 4}"{fail}><time>{e(ev["time"])}</time><span class="chip lane-{lane}">{e(ev["tag"])}</span><p>{e(ev["text"])}</p></li>')
        checks = "".join(f"<li>{e(c)}</li>" for c in ws["checks"])
        out.append(f'''            </ol>
          </section>
          <section class="pane work-pane" aria-label="工作区交付件">
            <div class="pane-head"><b>WORKSPACE</b><strong class="work-label">{e(ws["label"])}</strong></div>
            <ul class="checks">{checks}</ul>
            <div class="rail-row"><ol class="rail">''')
        for i, name in enumerate(data["rail"]):
            state = "current" if i == ws["rail"] else "done" if i < ws["rail"] else ""
            out.append(f'              <li class="{state}">{e(name)}</li>')
        link = f'<a class="work-link" href="{e(ws["link"])}" target="_blank" rel="noopener">打开 deck.html ↗</a>' if ws.get("link") else ""
        out.append(f'            </ol>{link}</div>')
        if ws["image"]:
            mark = ""
            if ws.get("highlight"):
                x, y, w, h = ws["highlight"]
                mark = f'<span class="slide-mark" style="left:{x}%;top:{y}%;width:{w}%;height:{h}%"><b>p14</b></span>'
            figure = f'<figure class="sheet"><img src="{e(ws["image"])}" alt="{e(ws["label"])}：全部幻灯片缩略图" loading="lazy" width="1440" height="1470">{mark}</figure>'
        else:
            lines = "".join(f"<span>{e(line)}</span>" for line in ws["source"])
            figure = f'<figure class="sheet source-sheet"><div class="source-doc"><i></i><i></i><i></i><i></i><i></i><i></i></div><figcaption>{lines}</figcaption></figure>'
        out.append(f'''            <div class="sheet-box">{figure}</div>
          </section>
          <section class="pane tree-pane" aria-label="Harness 文件树">
            <div class="pane-head"><b>HARNESS</b><span>harness/ · 当前组件</span></div>
            <ul class="tree">''')
        for lane in lanes:
            keys = [key for key in comps if comps[key]["lane"] == lane["id"] and key in harness]
            out.append(f'              <li class="dir lane-{lane["id"]}"><div class="dir-row"><span class="dot"></span><b>{e(lane["dir"])}</b><small>{e(lane["label"])} · {len(keys)}</small></div><ul>')
            if not keys:
                out.append('                <li class="file empty"><code>（空）</code></li>')
            for key in keys:
                comp, states = comps[key], harness[key].split()
                badges = "".join(f'<em class="st-{st}">{STATE_LABELS[st]}</em>' for st in states)
                version = f'<span class="ver">{e(s["versions"][key])}</span>' if key in s["versions"] else ""
                name = f'<a href="{e(comp["link"])}" target="_blank" rel="noopener">{e(comp["path"])}</a>' if comp.get("link") else e(comp["path"])
                kind = "file"
                if isinstance(comp["summary"], list):
                    kind = "file mem"
                    notes = '<ul class="notes">' + "".join(f"<li>{e(note)}</li>" for note in comp["summary"]) + "</ul>"
                else:
                    notes = f'<p># {e(comp["summary"])}</p>'
                out.append(f'                <li class="{kind} {" ".join("is-" + st for st in states)}"><div class="file-row"><code>{name}</code>{version}{badges}</div>{notes}</li>')
            out.append('              </ul></li>')
        out.append('''            </ul>
          </section>
        </div>
      </article>''')
    p = data["proof"]
    out.append(f'''    </div>
  </div>

  <section class="proof-panel" aria-labelledby="proof-title">
    <div class="proof-copy">
      <span class="eyebrow dark">WORKSPACE RESULT</span>
      <h3 id="proof-title">{e(p["title"])}</h3>
      <p>{e(p["text"])}</p>
      <a class="button dark-button" href="{e(p["link"])}" target="_blank" rel="noopener">打开 deck.html <span>↗</span></a>
    </div>
    <div class="proof-compare">
      <figure><span>{e(p["before"][0])}</span><img src="{e(p["before"][1])}" alt="{e(p["before"][2])}" loading="lazy"></figure>
      <i aria-hidden="true">→</i>
      <figure class="after"><span>{e(p["after"][0])}</span><img src="{e(p["after"][1])}" alt="{e(p["after"][2])}" loading="lazy"></figure>
    </div>
  </section>

  <p class="evo-footnote">{e(data["footnote"])}</p>
</section>''')
    return "\n".join(out)


def build(data_path, page_path):
    data = load(data_path)
    page = page_path.read_text(encoding="utf-8")
    if START not in page or END not in page:
        raise SystemExit(f"{page_path} needs {START} and {END} markers around the Demo 1 section")
    head, rest = page.split(START, 1)
    tail = rest.split(END, 1)[1]
    page_path.write_text(f"{head}{START}\n{render(data)}\n{END}{tail}", encoding="utf-8", newline="\n")
    print(f"built {page_path.name}: {len(data['stages'])} stages, {len(data['components'])} components")
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data", type=Path, default=ROOT / "data" / "demo1.json")
    parser.add_argument("--page", type=Path, default=ROOT / "index.html")
    parser.add_argument("--sync", action="store_true", help="copy files listed in sync.files from sync.source_root")
    parser.add_argument("--watch", action="store_true", help="rebuild when the data file or referenced assets change")
    args = parser.parse_args()

    if args.sync:
        sync = json.loads(args.data.read_text(encoding="utf-8"))["sync"]
        for src, dest in sync["files"]:
            source = Path(sync["source_root"]) / src
            if not source.exists():
                raise SystemExit(f"sync source missing: {source}")
            (ROOT / dest).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, ROOT / dest)
            print(f"synced {dest}")

    build(args.data, args.page)
    if not args.watch:
        return
    print("watching data/demo1.json, assets/ and components/ (Ctrl+C to stop)")
    watched = lambda: {p: p.stat().st_mtime for d in ("data", "assets", "components") for p in (ROOT / d).rglob("*") if p.is_file()}
    seen = watched()
    while True:
        time.sleep(1)
        now = watched()
        if now != seen:
            seen = now
            try:  # keep watching while the JSON is mid-edit
                build(args.data, args.page)
            except (SystemExit, ValueError, KeyError) as error:
                print(f"not rebuilt: {error!r}")


if __name__ == "__main__":
    main()
