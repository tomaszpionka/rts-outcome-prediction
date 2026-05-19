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
