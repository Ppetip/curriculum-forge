# Reading dataset audit results

A zero CLI exit code means the audit ran; it does not certify a leak-free or useful training dataset.

- `rows` counts input rows and `duplicates` lists flagged lexical pairs, not the number of unique duplicate clusters.
- Count `manifest[].split` to see the actual train/eval row counts. Indivisible groups can prevent the requested fraction.
- `warnings` identifies insufficient independent groups. Zero warnings does not prove semantic duplicates are absent.
- The synthetic default currently has six rows, one flagged pair, and a 5/1 train/eval split.

Jaccard overlap is a lexical heuristic. Review semantic paraphrases and task families before training. Jev review is advisory. The tool does not train an LLM or measure downstream quality. Export checks verify content/provenance consistency with the supplied manifest.

## Saved-check freshness in the local AI Lab workflow

When using the optional AI Lab workspace integration, run `python lab.py status` from the workspace root. This reads saved results without rerunning tests or inference and lists the latest checks for every tool. The shared runner is a local integration, not part of a standalone clone of this repository; standalone checks remain documented in README.

`check_passed` records command/test completion. `freshness` is separate:

- `current`: the explicit source inputs and Python runtime match the completed check.
- `source-or-runtime-changed`: rerun checks after relevant code or runtime changes.
- `changed-during-checks`: inputs changed while checks ran; that run cannot verify one stable version.
- `unverified-legacy`: an older result has no source fingerprint.
- `not-run`: no saved check exists for this tool.

Fingerprints cover project Python files, tests, checked-in example JSON/JSONL paths, workflow YAML and shared runner Python files. They omit documentation, .env, databases, private run outputs and arbitrary analysis input files. Current does not prove unchanged external dependencies or OS state. Saved reports are private local cache records, not signed attestations. A later demo never replaces a check result, and a current failing check is still a failure.

A current check validates the audit/export code and its fixtures. It does not re-audit an external dataset or approve the unfinished human-review labels.

## Compare independent label reviews

After reviewers label separate local copies, run `python review_agreement.py --left /absolute/path/reviewer-a.json --right /absolute/path/reviewer-b.json`. This read-only command reports agreement, disagreement, unreviewed pairs (at least one null label), and pairs present in only one review. It computes no detector scores, chooses no winning label and writes no merged dataset. Invalid labels, duplicate IDs or repeated normalized pairs stop the command with an error.

Pairs match by normalized unordered text, so reversed text order or different reviewer IDs still match. The same ID on different text is reported as separate unmatched pairs. Each decision keeps both IDs and labels but omits source text and extra reviewer metadata. `agreement_rate` divides agreements by pairs with boolean labels in both reviews; it is null if that denominator is zero. Report coverage and disagreements alongside the rate: missing work must not look like agreement.

Agreement does not prove correctness or independent review. Adjudicate disagreements using the task definition before running the detector evaluation. `evaluate_pairs` still rejects null labels. The CLI smoke check compares the blank synthetic template with itself only to exercise the unreviewed path; it is not a second review or evidence of human agreement. Reviewer files and notes stay local unless separately authorized for publication.
