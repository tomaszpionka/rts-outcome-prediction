# Plan critique — docs/thesis-bialecki2023-author-correction

reviewer: reviewer-adversarial (Category F mandatory pre-execution gate)
base_ref: 3238addb8d01b6baa7d642384e0d4f28e249f481

## Round 1 — reviewer-adversarial plan gate (2026-05-19): APPROVE-WITH-CONDITIONS

Round 1 — reviewer-adversarial plan gate. VERDICT: APPROVE-WITH-CONDITIONS. The corrective premise is independently confirmed: Crossref (structured given/family) and arXiv concordantly give authors 3–4 as Paweł Dobrowolski and Piotr Białecki, whereas `references.bib:6` cross-swaps their given names (`Dobrowolski, Piotr and Białecki, Paweł`); no bib convention or dataset erratum defends the current state, so the 1-line author swap is correct and the unchanged key keeps all citation sites valid. The plan's lineage discipline is sound in intent — correction-in-place (not deletion) of the five false #225 statements at report L332/L338/L508–513/L546–552, supersede-not-retro-edit for CHANGELOG `[3.60.0]`, and verbatim retention of the L564–565 Sources block (correct, since the DOI/PMC/arXiv corroboration was right and only the author parsing was wrong) — and following it produces an honest post-merge correction rather than history-tampering. Conditions: the recorded root cause must state #225 verified surname+count+order but never compared given-name tokens (Piotr/Paweł both collapse to "P." under initial-only matching), with that correction placed at L338 itself; the new `[3.61.0]` entry must explicitly cross-reference and supersede the falsified `[3.60.0]` sentence; and the eventual FINAL reviewer-adversarial gate must be appended under a separate heading in this file rather than overwrite this Round-1 record. No BLOCKER; PROCEED to execution once these conditions are reflected in the plan.

### Binding execution conditions (from Round 1)
1. Root-cause precision recorded at report L338 itself (not only CHANGELOG): #225 verified surname + count + order, never given-name tokens; Piotr/Paweł → "P.".
2. All load-bearing false sites corrected in place, none deleted: report L64, the `### Bialecki2023` subsection (heading L332 + table row L338 + prose L341–345), L508–513 clause, C5 item L546–552.
3. L564–565 fenced Sources kept verbatim (DOI/PMC/arXiv corroboration was correct; only author parsing was wrong).
4. CHANGELOG `[3.61.0]` explicitly cross-references and supersedes the falsified `[3.60.0]` sentence by version; `[3.60.0]` not retro-edited.
Nits: branch-first ordering (master guard hook) — mandatory; critique file Round 2 (FINAL gate) must be appended under a distinct heading, never overwrite Round 1.

## Round 2 — reviewer-adversarial FINAL gate (2026-05-19): APPROVE

VERDICT: APPROVE. The full diff base..HEAD is exactly the 7 intended files with zero
bytes under thesis/chapters/**, thesis/reviews_and_others/**, src/**, tests/**,
notebooks/**, or data/**; thesis/references.bib is exactly +1/-1 with only the
author line changed (key/title/journal/volume/number/pages/year/doi and the other
six names byte-identical, no key rename, no other entry touched). The applied bib
line now reads `Dobrowolski, Paweł and Białecki, Piotr` at positions 3–4, matching
the concordant Crossref (10.1038/s41597-023-02510-7) and arXiv (2207.03428) records
that the Round-1 gate independently confirmed. All four Round-1 binding conditions
are SATISFIED: root-cause precision (surname+initial collapse of Piotr/Paweł to "P.")
is recorded at the `### Bialecki2023` per-field subsection itself, not only in the
CHANGELOG; every load-bearing false site (master-table row, subsection heading +
per-field row + prose, the audit-only-assertion follow-up clause, the C5 item) is
corrected in place with none deleted and a new honest superseded-note added; the
fenced Sources block is byte-unchanged; and CHANGELOG `[3.61.0]` explicitly
supersedes the falsified `[3.60.0]` by version while `[3.60.0]` itself is
byte-unchanged. The critique.md −139 deletions are the prior PR #225 reviewer-deep
critique legitimately replaced for this new branch, not an overwrite of this PR's
Round-1 reviewer-adversarial record, which is present and intact and leaves Round 2
to be appended under a separate heading. An examiner diffing this branch against
#225 would read an honest, traceable post-merge correction — prior wrong conclusion
still visible, explicitly retracted, root cause named — not history-tampering. Only
non-gating nit: the `(PR #NNN)` CHANGELOG placeholder, resolved post-open by the
established number-recording follow-up. PROCEED to open the PR (NOT merge).
