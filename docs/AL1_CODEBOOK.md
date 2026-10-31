# AL-1 codebook

Lineage labels for a cross-version event pair: one event followed from one version of a Part 573 filing to the **next** version of the same filing. Protocol: `reports/AL1_PROTOCOL.md`.

**Every example is made up.** The company, part and dates are invented, and no text comes from an AL-1 filing.

An event is a dated happening in the chronology, with a date, a type and a supporting sentence. The types are the frozen ones in `docs/LABELING_RULES.md`.

Judge from the two versions' own text. If the PDF and the shown text differ, the PDF decides. A later version stating something differently does not show which version is true; these labels describe the change, not who was right.

## The five labels

### NEW
The event is in the later version and nothing in the earlier version reports it.

- Earlier: *(no such entry)*
- Later: "May 2, 2031: Zephyr Parts told Northwind Motors that a batch of hinges failed a salt test."

### UNCHANGED
The same event, with the same date and type, in both versions. Different wording or layout does not matter. It also applies when the words are in both versions but the extractor claimed the event in only one of them (`text_carried`).

- Earlier: "On May 2, 2031, Zephyr Parts notified Northwind Motors of the hinge test failure."
- Later: "May 2, 2031: Northwind Motors was notified by Zephyr Parts of the hinge test failure."

### DATE_CORRECTION
The same event, with a different date. A more or less precise date counts ("May 2031" becoming "May 2, 2031"). If the type changed too, the label is still DATE_CORRECTION; date takes priority. The name describes the change only: it does not say the earlier date was an error.

- Earlier: "On May 2, 2031, Zephyr Parts notified Northwind Motors of the hinge test failure."
- Later: "On May 9, 2031, Zephyr Parts notified Northwind Motors of the hinge test failure."

### TYPE_CHANGE
The same event and date, but it has a different event type, because the later version describes what happened differently.

- Earlier: "On June 3, 2031, Northwind Motors began reviewing the hinge test results." (`INVESTIGATION_START`)
- Later: "On June 3, 2031, the review of the hinge test results led Northwind Motors to decide to recall." (`DECISION`)

The type being judged is the one the sheet shows for each side. If the wording supports the same type on both sides and only the shown type differs, mark UNCHANGED.

### RETRACTED
The event is in the earlier version and the later version no longer reports it. The name describes absence only: the filer need not have withdrawn it on purpose.

- Earlier: "On July 8, 2031, a dealer in Ohio reported a loose hinge."
- Later: *(no such entry, and no entry describing the same report)*

Check the whole of the later chronology before choosing RETRACTED or NEW. If the event appears elsewhere in that chronology, it is not RETRACTED or NEW.

## Two further marks

These are for the author's marks only. The matcher never predicts them.

- **NOT_SAME_EVENT:** the sheet presents two sentences as one event, but they describe different events.
- **UNSURE:** the text does not settle it.

## Order of decisions

1. Is the event reported in both versions? If only in the later one, **NEW**. If only in the earlier one, **RETRACTED**. If the sheet paired two different events, **NOT_SAME_EVENT**.
2. Do the dates differ? **DATE_CORRECTION**.
3. Do the types differ? **TYPE_CHANGE**.
4. Otherwise, **UNCHANGED**.

## Words not to use

The labels are not findings about any company. Do not write that a filer was late, at fault, or hid or corrected an error. A supplier is "named in the filing", never "responsible" or "the cause".
