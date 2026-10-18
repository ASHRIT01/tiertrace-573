"""component_manufacturer_kind for a filing: external / filer_itself / filer_affiliate / blank.

RULE (deterministic; names compared after tt.norm.aliases.squash: lowercase, punctuation and corporate suffixes removed):
 blank           the block has no supplier name (NR, N/A, empty, or no block).
 filer_itself    the block name equals the filer name after squashing and singularising tokens (PDF header filer; flat-file
                 MFGNAME as fallback).
 filer_affiliate not filer_itself, and EITHER one name contains the other (usually a foreign parent vs its US subsidiary,
                 e.g. 'Mercedes-Benz AG' vs 'Mercedes-Benz USA'), OR both names contain an alias of the same group in config/affiliates.csv
                 (seed table, UNVERIFIED), OR they share a first significant word (>= 4 chars, not a generic word such as
                 'general', 'american', 'national', 'international', 'united', 'global', 'advanced', 'standard').
 external        everything else.
Known weaknesses: containment sometimes means the same entity ('Blue Bird' vs 'Blue Bird Body Company' is called an
affiliate); the shared-first-word test joins unrelated companies with a common brand word (e.g. Volvo Car and Volvo
Trucks are different groups); the group table is a hand-written seed; a name mentioned only by brand is not linked."""
import csv
from pathlib import Path

from tt.norm.aliases import squash

GENERIC = {"general", "american", "national", "international", "united", "global", "advanced", "standard", "universal", "first",
           "north", "american", "great", "premier", "precision", "quality", "custom", "industrial", "automotive"}


def load_groups(path: str | Path = "config/affiliates.csv") -> list[tuple[str, str]]:
    rows = []
    for line in Path(path).read_text().splitlines():
        if not line.strip() or line.startswith("#") or line.startswith("group,"):
            continue
        g, a = line.split(",", 1)
        rows.append((g, _sg(squash(a))))
    return rows


def _sg(sq: str) -> str:
    """Strip a trailing plural 's' from each token (len > 3) so 'trucks' == 'truck'."""
    return " ".join(t[:-1] if len(t) > 3 and t.endswith("s") else t for t in sq.split())


def _has(sq: str, alias: str) -> bool:
    return bool(alias) and f" {alias} " in f" {sq} "


def _groups_of(sq: str, groups) -> set[str]:
    return {g for g, a in groups if _has(sq, a)}


def kind(name: str | None, filer: str, groups) -> tuple[str, str]:
    """-> (kind, reason)"""
    if not name:
        return "blank", "no supplier name in block"
    a, f = _sg(squash(name)), _sg(squash(filer or ""))
    if a and f and a == f:
        return "filer_itself", "equal"
    if a and f and (a in f or f in a):
        return "filer_affiliate", "name contained in the other (parent or regional entity)"
    shared = _groups_of(a, groups) & _groups_of(f, groups)
    if shared:
        return "filer_affiliate", f"same group: {sorted(shared)[0]}"
    wa, wf = a.split(), f.split()
    if wa and wf and wa[0] == wf[0] and len(wa[0]) >= 4 and wa[0] not in GENERIC:
        return "filer_affiliate", f"shared first word: {wa[0]}"
    return "external", ""
