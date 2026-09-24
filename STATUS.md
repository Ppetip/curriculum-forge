# Status

Stage: command-line prototype with optional live Jev integration.
Verified: 51 tests and four offline CLI paths pass locally; all four hosted checks pass. Jev smoke results remain historical; no new live calls.

Latest: Compare two label reviews without detector scores or automatic adjudication.

Next: Obtain independent judgments for the blank pair template before tuning thresholds.

Repository: https://github.com/Ppetip/curriculum-forge
Budget: one shared $3 cumulative Jev allowance across the portfolio, never per project or cycle.
No other paid compute authorized. Eight initial calls across all projects used 3,303 input tokens;
estimated total $0.000138726, with $0.08 conservatively reserved. See README for limits.
Live smoke responses are not production benchmarks. No model training performed.

2026-09-21 CI pass: added pinned, read-only Windows/Linux Python 3.11/3.13 checks for unit tests and offline CLI contracts. Local checks and all four hosted Windows/Linux Python 3.11/3.13 jobs pass. No additional Jev calls.

Hosted verification: https://github.com/Ppetip/curriculum-forge/actions/runs/35590271849

2026-09-21 14:42 UTC budget fix: live clients require an existing ledger; explicit initialization refuses overwrite. Added four regression cases for missing/deleted/empty ledgers and preserved spending. All local tests, CLI checks, and four hosted Windows/Linux Python 3.11/3.13 jobs pass. No additional Jev calls.

Budget-fix hosted verification: https://github.com/Ppetip/curriculum-forge/actions/runs/35614378665

2026-09-21 18:44 UTC: Dataset export checks row IDs, source, family, text hashes and split labels before creating output. Local tests, offline CLI checks, and all four hosted matrix jobs pass. No additional Jev calls.

Feature-pass verification: https://github.com/Ppetip/curriculum-forge/actions/runs/35640890162

2026-09-21 22:45 UTC: documented how to interpret this tool's outcomes separately from command success. The local Codex runner now shows a concise outcome summary for this project. Verified through common-runner checks and synthetic demo output; histories stay local.

2026-09-22 02:46 UTC: Labeled-pair evaluation reports confusion counts, precision, recall and per-pair errors. Common-runner checks, new route and all four hosted jobs pass. No new Jev calls.

Evaluation-path verification: https://github.com/Ppetip/curriculum-forge/actions/runs/35681194785

2026-09-22 10:48 UTC: Pair evaluation rejects repeated normalized text pairs, including reversed pairs and contradictory labels under different IDs. Each unordered normalized pair is counted once; remove duplicate rows and adjudicate conflicting labels before evaluation. Different pairs may share one text, so this guard does not guarantee statistical independence or prevent cross-split leakage. Published and verified: local checks and all four hosted matrix jobs pass. No new Jev calls.

Reliability verification: https://github.com/Ppetip/curriculum-forge/actions/runs/35718640295

2026-09-22 22:50 UTC: Added `examples/review-pairs.json` and [label-review instructions](docs/LABEL_REVIEW.md). Four synthetic support-ticket pairs have null labels and no similarity scores, so a reviewer can judge intent before seeing detector output. The evaluator intentionally rejects the unfinished template. Independent labels remain missing; no threshold tuning or new quality estimate is claimed. Common-runner checks pass. Documentation only; prior hosted code checks remain applicable. No new Jev calls.

2026-09-23 06:53 UTC: Export recomputes duplicate edges at the declared audit threshold and rejects cross-split family/duplicate assignments, even when all content hashes still match. Missing/invalid thresholds fail closed. Four regression tests cover exact duplicates, family links, custom thresholds and invalid threshold metadata; rejected exports create no destination. Common-runner checks: 45 tests and 3 offline CLI paths pass. Run ID: `ae94f89edbea4bbdbc0b02564108d9f3`. Hosted verification passed on all four OS/Python combinations. No API calls or independent pair judgments were added; label collection remains pending.

2026-09-23 10:54 UTC verification follow-up: Published code and all four hosted jobs verified after the earlier approval-review usage-limit interruption. Existing check suites were not rerun solely to create history. Run: https://github.com/Ppetip/curriculum-forge/actions/runs/35829387901

2026-09-23 14:55 UTC: Added guidance for interpreting saved-check freshness in the optional local Codex runner. A current check validates the audit/export code and its fixtures. It does not re-audit an external dataset or approve the unfinished human-review labels. The shared runner now records check-source fingerprints and provides read-only status. All five current app checks passed (234 tests total), along with 24 local runner regressions. Run ID: 811900b822db42e390b5e1714afbbe25. App implementation unchanged; this documentation update skips redundant hosted CI. No live calls or new performance claim.

2026-09-24 19:00 UTC: Added read-only reviewer comparison with normalized pair matching, coverage counts, explicit disagreements and null agreement rate when no pair has two labels. No labels were supplied or approved; the original blank template remains unchanged. Local check bcb0447e92c3448a8f831c4445e3f44c passed. All four hosted Windows/Linux Python 3.11/3.13 jobs pass. No live calls or training.

Review-agreement verification: https://github.com/Ppetip/curriculum-forge/actions/runs/36045698676
