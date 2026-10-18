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
