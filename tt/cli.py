import typer

app = typer.Typer(no_args_is_help=True, help="TierTrace-573")


@app.command()
def fetch(years: str = "2015-2026", rate: float = 1.0):
    """Polite crawl (blocked on the Week 1 URL-enumeration gate)."""
    raise typer.Exit("fetch not implemented: resolve the Week 1 URL-enumeration gate first")


@app.command("fetch-list")
def fetch_list(url_file: str = "config/golden_urls.txt", out: str = "data/raw", rate: float = 1.0):
    """Download the PDFs listed in a file (one URL per line), politely, into `out`."""
    from pathlib import Path
    from tt.fetch.nhtsa import PoliteFetcher
    f = PoliteFetcher(Path("data/cache"), rate)
    Path(out).mkdir(parents=True, exist_ok=True)
    from tt.fetch.nhtsa import Blocked
    for u in Path(url_file).read_text().split():
        try:
            b = f.get(u)
        except Blocked as e:
            typer.echo(f"BLOCKED: {e}. Not retrying.")
            raise typer.Exit(2)
        typer.echo(f"{u.rsplit('/', 1)[1]}: {'ok' if b else 'FAILED'}")
        if b:
            (Path(out) / u.rsplit("/", 1)[1]).write_bytes(b)


@app.command("flat-index")
def flat_index(zip_path: str = "data/flat/FLAT_RCL_POST_2010.zip", out: str = "data/processed/campaigns.csv",
               first_year: int = 2015):
    """One row per campaign from the LOCAL flat file (no download)."""
    from tt.data.flat import load_campaigns, write_csv
    rows = load_campaigns(zip_path, first_year, "VECT")
    write_csv(rows, out)
    typer.echo(f"{len(rows)} campaigns from {first_year} -> {out}")


@app.command()
def sample(per_year: int = 25, max_try: int = 40, seed: int = 0, rate: float = 1.0):
    """Stratified sample: list_573 per candidate campaign (1 req/s, stops on 401/403/429)."""
    import csv, json
    from pathlib import Path
    from tt.fetch.api import ApiClient
    from tt.fetch.nhtsa import Blocked
    from tt.fetch.sample import build_sample
    camps = list(csv.DictReader(open("data/processed/campaigns.csv")))
    for c in camps:
        c["year"] = int(c["year"])
    client = ApiClient(rate_s=rate)
    try:
        st = build_sample(client, camps, per_year, max_try, seed)
    except Blocked as e:
        typer.echo(f"BLOCKED: {e}. Not retrying.")
        raise typer.Exit(2)
    rows = [json.loads(l) for l in open("data/processed/sample_573.jsonl")]
    Path("data/processed/sample_urls.txt").write_text("\n".join(r["url"] for r in rows if r["is_latest"]) + "\n")
    typer.echo(json.dumps({**st, "api_requests": client.requests_made}))


@app.command()
def checksheet(per_year: int = 4, seed: int = 0, out: str = "reports/checksheet.md"):
    """Parsed fields next to verbatim source text for a seeded sample, for hand-checking."""
    from pathlib import Path
    from tt.checksheet import build
    md = build(Path("data/processed/sample_573.jsonl"), Path("data/audit_raw"),
               Path("config/checksheet_exclude.txt"), per_year, seed)
    Path(out).parent.mkdir(exist_ok=True)
    Path(out).write_text(md)
    typer.echo(f"wrote {out} ({md.count('## ')} filings)")


@app.command("narrative-gain")
def narrative_gain(out: str = "reports/narrative_gain.md"):
    """How often the narrative names a company/dated event/cause the block and flat file do not."""
    from pathlib import Path
    from tt.narrative import run
    md = run(Path("data/processed/sample_573.jsonl"), Path("data/audit_raw"), Path("data/flat/FLAT_RCL_POST_2010.zip"))
    Path(out).parent.mkdir(exist_ok=True)
    Path(out).write_text(md)
    typer.echo(md)


@app.command("mask-size")
def mask_size(out: str = "reports/mask_recover_size.md"):
    """How many filings have the block supplier also named in the narrative (mask-and-recover test size)."""
    from pathlib import Path
    from tt.maskrecover import run
    from tt.norm.aliases import AliasTable
    md = run(Path("data/processed/sample_573.jsonl"), Path("data/audit_raw"), AliasTable.load("config/aliases.csv"))
    Path(out).parent.mkdir(exist_ok=True)
    Path(out).write_text(md)
    typer.echo(md)


@app.command("add-kind")
def add_kind(out: str = "reports/component_manufacturer_kind.md"):
    """Add component_manufacturer_kind to data/processed/sample_573.jsonl (+ sample_kind.csv) and report counts."""
    import csv, json, random
    from collections import Counter, defaultdict
    from pathlib import Path
    from tt.kind import kind, load_groups
    from tt.parse.block import parse_block, raw_block
    from tt.parse.pdf import extract_text
    from tt.parse.sections import parse_header
    groups = load_groups()
    flat = {r["campaign"]: r["filer"] for r in csv.DictReader(open("data/processed/campaigns.csv"))}
    rows = [json.loads(l) for l in open("data/processed/sample_573.jsonl")]
    recs = []
    for r in rows:
        if not r["is_latest"]:
            r["component_manufacturer_kind"] = None  # earlier versions: PDF not downloaded
            continue
        t = extract_text(Path("data/audit_raw") / r["url"].rsplit("/", 1)[1])[0]
        name, filer = parse_block(raw_block(t)).name, parse_header(t)["filer"] or flat.get(r["campaign"], "")
        k, why = kind(name, filer, groups)
        r["component_manufacturer_kind"] = k
        recs.append({"campaign": r["campaign"], "year": r["year"], "file": r["url"].rsplit("/", 1)[1], "filer": filer,
                     "name": name or "", "kind": k, "why": why})
    Path("data/processed/sample_573.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    with open("data/processed/sample_kind.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(recs[0])); w.writeheader(); w.writerows(recs)
    c = Counter(x["kind"] for x in recs)
    by = defaultdict(Counter)
    for x in recs:
        by[x["year"]][x["kind"]] += 1
    ks = ["external", "filer_itself", "filer_affiliate", "blank"]
    md = ["# component_manufacturer_kind (300 latest-version filings)", "", "Rule (also in tt/kind.py):", "```", __import__("tt.kind", fromlist=["x"]).__doc__.split("RULE")[1].strip(" (\n"), "```", "",
          "Counts: " + ", ".join(f"{k} {c[k]}" for k in ks), "", "| year | " + " | ".join(ks) + " |", "|---|---|---|---|---|"]
    md += [f"| {y} | " + " | ".join(str(by[y][k]) for k in ks) + " |" for y in sorted(by)]
    rng = random.Random(0)
    ex = []
    for k, n in (("external", 3), ("filer_affiliate", 3), ("filer_itself", 2), ("blank", 2)):
        pool = [x for x in recs if x["kind"] == k]; rng.shuffle(pool); ex += pool[:n]
    md += ["", "## 10 random examples (seed 0)", ""] + [f"- **{x['file']}** ({x['year']}) filer `{x['filer']}` / block `{x['name']}` -> **{x['kind']}** {x['why']}" for x in ex]
    aff = [x for x in recs if x["kind"] == "filer_affiliate"]
    md += ["", f"## All {len(aff)} filer_affiliate calls (for checking)", ""] + [f"- {x['file']}: `{x['filer']}` vs `{x['name']}` ({x['why']})" for x in aff]
    Path(out).write_text("\n".join(md))
    typer.echo("\n".join(md))


@app.command("draw-splits")
def draw_splits(seed: int = 0, dev_per_year: int = 50, testa_n: int = 1000):
    """Draw dev and Test-A campaign id lists (IDs + SHA-256 only; no network)."""
    from pathlib import Path
    from tt.splits import draw, eligible, write
    rows = eligible(Path("data/processed/campaigns.csv"), Path("data/processed/sample_573.jsonl"))
    dev, testa, info = draw(rows, dev_per_year, testa_n, seed)
    h = write(dev, testa, Path("data/splits"), info, seed)
    typer.echo(f"eligible {len(rows)}; dev {len(dev)}; testA {len(testa)}; alloc {info['testA_alloc']}")
    typer.echo(h)


@app.command("dev-fetch")
def dev_fetch(rate: float = 1.0):
    """List 573 versions for the DEV ids only, then download the latest version of each (1 req/s; stops on 401/403/429).
    Reads data/splits/dev_ids.txt only; never touches the Test-A list."""
    import csv, json
    from pathlib import Path
    from tt.fetch.api import ApiClient, list_573
    from tt.fetch.nhtsa import Blocked, PoliteFetcher
    ids = Path("data/splits/dev_ids.txt").read_text().split()
    meta = {r["campaign"]: r for r in csv.DictReader(open("data/processed/campaigns.csv"))}
    client, rows, no573 = ApiClient(rate_s=rate), [], []
    try:
        for i, cid in enumerate(ids, 1):
            docs = list_573(client, cid)
            if not docs:
                no573.append(cid)
            for d in docs:
                rows.append({**d, "year": int(meta[cid]["year"]), "type": meta[cid]["type"], "n_versions": len(docs)})
            if i % 50 == 0:
                typer.echo(f"listed {i}/{len(ids)}")
        Path("data/processed/dev_573.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        latest = [r for r in rows if r["is_latest"]]
        f = PoliteFetcher(Path("data/cache"), rate)
        out = Path("data/dev_raw"); out.mkdir(parents=True, exist_ok=True)
        ok = failed = 0
        for r in latest:
            b = f.get(r["url"])
            if b:
                (out / r["url"].rsplit("/", 1)[1]).write_bytes(b); ok += 1
            else:
                failed += 1; typer.echo(f"FAILED {r['url']}")
    except Blocked as e:
        typer.echo(f"BLOCKED: {e}. Not retrying.")
        raise typer.Exit(2)
    typer.echo(json.dumps({"dev_ids": len(ids), "with_573": len(latest), "no_573": len(no573), "multi_version": sum(1 for r in latest if r["n_versions"] > 1),
                           "downloaded": ok, "download_failed": failed, "api_requests": client.requests_made}))


@app.command("dev-bench")
def dev_bench(model: str = typer.Option(..., "--model", help="exact installed tag, e.g. qwen3.5:4b-q4_K_M"), ctx: int = 6144,
              out: str = "", labels: str = "reports/dev_labels_draft.json", pdf_dir: str = "data/dev_raw", resume: bool = False,
              timeout: float = 300.0):
    """Run ONE named model over the 30 dev filings (thinking off, temperature 0 set explicitly), then print JSON-valid rate, tokens/s,
    p50/p95 seconds per filing, and scores vs the UNREVIEWED label drafts. Never pulls a model."""
    import json
    from pathlib import Path
    import ollama
    from tt.agent.run_dev import OPTIONS, run, summarize
    from tt.eval.devscore import score
    try:
        ollama.show(model)
    except Exception as e:
        typer.echo(f"Model {model!r} is not installed or the Ollama server is not running ({e}). Not pulling. Start `ollama serve` / check `ollama list`.")
        raise typer.Exit(2)
    L = json.load(open(labels))
    if "silver" in labels:   # final silver labels: add spans, drop contested events (see tt.labels.protocol.prepare_gold)
        from tt.labels.protocol import prepare_gold
        L = prepare_gold(L, Path(pdf_dir))
    outp = Path(out or f"runs/dev_bench_{model.replace(':', '_').replace('/', '_')}.jsonl")
    outp.parent.mkdir(exist_ok=True)
    typer.echo(f"model={model} think=False options={ {**OPTIONS, 'num_ctx': ctx} } filings={len(L)} -> {outp}")
    recs = run(model, [l["file"] for l in L], Path(pdf_dir), outp, ctx, resume=resume, timeout=timeout,
               progress=lambda i, n, r: typer.echo(f"  {i}/{n} {r['file']} {r['seconds']:.1f}s valid_json={r['extraction'] is not None} truncated={r.get('truncated')} elapsed={r['elapsed']:.0f}s eta={r['eta']:.0f}s"
                                                   + (f" ERROR {r['error'][:80]}" if r.get('error') else ""), flush=True))
    s = summarize(recs)
    typer.echo("\nSPEED / VALIDITY (this machine, this run)")
    typer.echo(f"  JSON-valid rate:        {s['json_valid_rate']:.1%}  ({s['errors']} call errors)")
    typer.echo(f"  generation tokens/s:    {s['generation_tokens_per_s']:.1f}   prompt tokens/s: {s['prompt_tokens_per_s']:.1f}")
    typer.echo(f"  seconds/filing p50/p95: {s['seconds_p50_all']:.1f} / {s['seconds_p95_all']:.1f}  (all {len(recs)}, includes the first cold-load call of {s['first_call_seconds']:.1f}s)")
    typer.echo(f"                          {s['seconds_p50_excl_first']:.1f} / {s['seconds_p95_excl_first']:.1f}  (excluding the first call)")
    sc = score(L, recs, Path(pdf_dir))
    typer.echo("\nSCORES vs SILVER labels (AI-made, not human-verified)")
    for k in ("json_valid_rate", "verifier_pass_rate", "s2_recovery", "unsupported_claim_rate", "event_precision", "event_recall", "event_f1",
              "event_other_f1", "event_fuzzy_recall", "cause_accuracy"):
        typer.echo(f"  {k:24} {sc[k]:.3f}")
    typer.echo(f"  (s2_recovery over {sc['s2_gold_supported']} filings with a supported S2 draft; unsupported_claim_rate over {sc['s2_not_supported_gold']})")
    typer.echo(f"\npredictions saved: {outp}")


@app.command("compare-labels")
def compare_labels_cmd(a: str = "reports/dev_labels_draft.json", b: str = "reports/blind_labels_ai.json", out: str = "reports/ai_vs_ai_agreement.md"):
    """AI-vs-AI agreement between two label sets (not human verification)."""
    import json
    from pathlib import Path
    from tt.eval.compare_labels import compare, render_markdown
    A, B = json.load(open(a)), json.load(open(b))
    md = render_markdown(compare(A, B), A, a, b)
    Path(out).write_text(md)
    typer.echo("\n".join(md.split("\n")[:20]))


@app.command("adjudication")
def adjudication_cmd(a: str = "reports/dev_labels_draft.json", b: str = "reports/blind_labels_ai.json", out: str = "reports/adjudication.md",
                     a_commit: str = "", pdf_dir: str = "data/dev_raw", n_agree: int = 10, seed: int = 0):
    """Build the adjudication sheet (nothing marked). With --a-commit, A is read from that git commit."""
    import json, subprocess
    from pathlib import Path
    from tt.eval.adjudication import build
    A = json.loads(subprocess.run(["git", "show", f"{a_commit}:{a}"], capture_output=True, text=True, check=True).stdout) if a_commit else json.load(open(a))
    B = json.load(open(b))
    name = f"{a} at commit {a_commit}" if a_commit else a
    Path(out).write_text(build(A, B, Path(pdf_dir), name, b, n_agree, seed))
    typer.echo(f"wrote {out}")


@app.command("pass-a")
def pass_a_cmd(selection: str = "config/dev_silver_100.json", drafts: str = "reports/dev_labels_draft.json", out: str = "data/labels/passA_v1.json"):
    """Build Pass A (AI drafter, code-assisted) for the labelled dev set."""
    import json
    from pathlib import Path
    from tt.labels.draft import build_pass_a
    from tt.labels.events import load_overrides
    S = json.load(open(selection))["filings"]
    co = json.load(open("config/claim_overrides.json"))
    recs = build_pass_a(S, json.load(open(drafts)), Path("data/dev_raw"), load_overrides(), co)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(recs, indent=1, ensure_ascii=False))
    typer.echo(f"{len(recs)} filings -> {out}")


@app.command("dev-score")
def dev_score(preds: str, labels: str = "reports/dev_labels_draft.json", pdf_dir: str = "data/dev_raw"):
    """Score a predictions JSONL against the dev label DRAFTS (not gold)."""
    import json
    from pathlib import Path
    from tt.eval.devscore import score
    L = json.load(open(labels))
    P = [json.loads(l) for l in open(preds)]
    typer.echo(json.dumps(score(L, P, Path(pdf_dir)), indent=1))


@app.command("audit")
def audit_cmd(pdf_dir: str = "data/audit_raw", out: str = "reports/audit.md"):
    """Download/text-layer/fill-rate audit of the sampled filings."""
    from pathlib import Path
    from tt.audit import audit
    md = audit(Path("data/processed/sample_573.jsonl"), Path(pdf_dir))
    Path(out).parent.mkdir(exist_ok=True)
    Path(out).write_text(md)
    typer.echo(md)


@app.command("parse-report")
def parse_report_cmd(folder: str = "data/raw", out: str = "reports/parse_report.md"):
    """Parse every PDF in a folder; report failures grouped by layout."""
    from pathlib import Path
    from tt.parse.report import build_report
    md = build_report(Path(folder))
    Path(out).parent.mkdir(exist_ok=True)
    Path(out).write_text(md)
    typer.echo(md)


@app.command()
def parse(path: str):
    """Parse one PDF: report text-layer status and block fields."""
    from tt.parse.pdf import extract_text
    from tt.parse.sections import split_sections
    from tt.parse.block import parse_block, raw_block
    text, empty = extract_text(path)
    secs = split_sections(text)
    typer.echo(f"chars={len(text)} pages_without_text={empty} sections={list(secs)}")
    typer.echo(parse_block(raw_block(text)).asdict())


if __name__ == "__main__":
    app()
