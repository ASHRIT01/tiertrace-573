# SC-1 amendments to the protocol (tag `sc-protocol-1`)

The protocol requires every change made after the tag to be listed here, with its date and reason, and the results it affects to be labelled POST HOC. Reference = filer-declared supplier (non-AI, not ground truth).

## SC-A1 (2026-10-29): where a silver supplier claim stores its name

- **What happened.** On its first run, `scripts/sc_check.py` stopped while attaching claims (`KeyError: 'label'`). This was before any claim had been compared with the reference and before any output file existed.
- **Cause.** Protocol C says the silver name is "the text of the label after the first ': '". The 26 S2 claims decided by Pass C (Test-A 16, Test-B 7, unseen 3) have no `label`; they store the name in a `name` field.
- **Change.** The name is `name` when present, otherwise the label text after the first ": " (`silver_name` in `scripts/sc_check.py`). This is how the silver file is written; no definition changes.
- **POST HOC label.** Because it came after the tag, the results for those 26 silver S2 claims depend on this amendment and are labelled POST HOC. The report gives their count.
