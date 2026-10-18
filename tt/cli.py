import typer

app = typer.Typer(no_args_is_help=True, help="TierTrace-573")


@app.command()
def fetch(years: str = "2015-2026", rate: float = 1.0):
    """Polite crawl (blocked on the Week 1 URL-enumeration gate)."""
    from tt.fetch.nhtsa import candidate_urls  # noqa: F401
    raise typer.Exit("fetch not implemented: resolve the Week 1 URL-enumeration gate first")


@app.command()
def parse(path: str):
    """Parse one PDF: report text-layer status and block fields."""
    from tt.parse.pdf import extract_text
    from tt.parse.sections import split_sections
    from tt.parse.block import parse_block
    text, empty = extract_text(path)
    secs = split_sections(text)
    typer.echo(f"chars={len(text)} pages_without_text={empty} sections={list(secs)}")
    typer.echo(parse_block(secs.get("block", "")).asdict())


if __name__ == "__main__":
    app()
