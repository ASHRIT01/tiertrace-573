"""Export the text a labeller sees for one filing: header, Component Manufacturer block, cause, chronology (line breaks kept).
These files are the ONLY input given to the blind Pass B and the Pass C adjudicator."""
from pathlib import Path

from tt.parse.block import raw_block
from tt.parse.pdf import extract_text
from tt.parse.sections import parse_header, split_sections


def filing_text(pdf: Path) -> str:
    t, _ = extract_text(pdf)
    h = parse_header(t)
    s = split_sections(t, collapse=False)
    return "\n".join([f"FILE: {pdf.name}", f"FILER: {h['filer']}", f"FILING DATE: {h['filing_date']}", f"CAMPAIGN: {h['campaign']}", "",
                      "=== COMPONENT MANUFACTURER BLOCK ===", raw_block(t).strip() or "(no block found)", "",
                      "=== DESCRIPTION OF THE CAUSE ===", s.get("cause", "").strip() or "(empty)", "",
                      "=== CHRONOLOGY ===", s.get("chronology", "").strip() or "(empty)", ""])


def export(files: list[str], pdf_dir: Path, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for f in files:
        p = out_dir / (f.rsplit(".", 1)[0] + ".txt")
        p.write_text(filing_text(pdf_dir / f))
        paths.append(p)
    return paths
