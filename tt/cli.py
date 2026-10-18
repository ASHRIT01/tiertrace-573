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
