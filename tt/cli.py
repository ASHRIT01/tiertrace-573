import typer

app = typer.Typer(no_args_is_help=True, help="TierTrace-573")


@app.command()
def fetch(years: str = "2015-2026", rate: float = 1.0):
    """Polite crawl (blocked on the Week 1 URL-enumeration gate)."""
    from tt.fetch.nhtsa import candidate_urls  # noqa: F401
    raise typer.Exit("fetch not implemented: resolve the Week 1 URL-enumeration gate first")


@app.command("fetch-list")
def fetch_list(url_file: str = "config/golden_urls.txt", out: str = "data/raw", rate: float = 1.0):
    """Download the PDFs listed in a file (one URL per line), politely, into `out`."""
    from pathlib import Path
    from tt.fetch.nhtsa import PoliteFetcher
    f = PoliteFetcher(Path("data/cache"), rate)
    Path(out).mkdir(parents=True, exist_ok=True)
    for u in Path(url_file).read_text().split():
        b = f.get(u)
        typer.echo(f"{u.rsplit('/', 1)[1]}: {'ok' if b else 'FAILED'}")
        if b:
            (Path(out) / u.rsplit("/", 1)[1]).write_bytes(b)


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
