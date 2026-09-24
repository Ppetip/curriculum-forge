# Pair label review

These four fictional support-ticket pairs are unreviewed. No model scores or suggested answers are supplied. The `duplicate` fields in `examples/review-pairs.json` are null on purpose; the evaluator rejects them until a reviewer supplies boolean judgments.

Define duplicate as: the same requested action, material constraints and intended outcome. Similar wording alone is insufficient. Decide how your workflow treats pauses, cancellation, refunds, store credit and negation before labeling.

1. Copy the template to a local review file; keep the original blank template intact.
2. Judge each pair without viewing similarity scores. Set `duplicate` to true or false only when you can justify it. Record your rationale separately and omit unresolved pairs from the scored file.
3. If another reviewer disagrees, adjudicate before evaluation; do not take the detector's answer as ground truth.
4. Run `python pair_evaluation.py --input /absolute/path/to/reviewed-pairs.json --threshold 0.85`.
5. Inspect false positives and false negatives. This small review set is development data, not a final test set or a representative precision/recall estimate. Freeze a separate reviewed holdout before threshold tuning.

No labels have been approved by a human yet. Do not count the template as labeled evaluation evidence or publish private reviewer notes without authorization.

## Compare independent label reviews

After reviewers label separate local copies, run `python review_agreement.py --left /absolute/path/reviewer-a.json --right /absolute/path/reviewer-b.json`. This read-only command reports agreement, disagreement, unreviewed pairs (at least one null label), and pairs present in only one review. It computes no detector scores, chooses no winning label and writes no merged dataset. Invalid labels, duplicate IDs or repeated normalized pairs stop the command with an error.

Pairs match by normalized unordered text, so reversed text order or different reviewer IDs still match. The same ID on different text is reported as separate unmatched pairs. Each decision keeps both IDs and labels but omits source text and extra reviewer metadata. `agreement_rate` divides agreements by pairs with boolean labels in both reviews; it is null if that denominator is zero. Report coverage and disagreements alongside the rate: missing work must not look like agreement.

Agreement does not prove correctness or independent review. Adjudicate disagreements using the task definition before running the detector evaluation. `evaluate_pairs` still rejects null labels. The CLI smoke check compares the blank synthetic template with itself only to exercise the unreviewed path; it is not a second review or evidence of human agreement. Reviewer files and notes stay local unless separately authorized for publication.
