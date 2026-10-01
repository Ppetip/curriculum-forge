# Status

Stage: command-line prototype with optional live Jev integration.
Verified: 62 tests and five offline CLI paths pass locally; all four hosted checks pass. Jev smoke results remain historical; no new live calls.

Latest: Threshold comparisons score each pair once and reuse scores while preserving metrics and error IDs.

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

2026-09-27 07:00 UTC: The optional local AI Lab integration now exposes review-agreement, requiring both --input and --reference for supplied reviews; the default blank example is explicitly unreviewed. Standalone review_agreement.py remains available in this repository. All five common-runner check routes passed (280 app tests and 28 CLI paths total), plus 32 shared-runner regressions. Check run ffd76d632c9246f4969e0cbbbacb538f. Shared integration is local to the AI Lab workspace, not included in a standalone repository clone. Existing app-source hosted results remain applicable; this documentation update skips redundant hosted CI. No paid calls.

2026-09-27 19:00 UTC: The shared-runner change passes existing dataset and review checks; independent pair labels remain pending. All five common checks pass (288 app tests, 29 CLI paths), plus 38 shared-runner regressions. Check run 6cbc7ab369f64438ac08e746849d49a7. Shared integration stays local to the AI Lab workspace. App-source hosted evidence is unchanged; documentation-only update skips redundant CI. No live calls.

2026-09-28 15:00 UTC: Official TypeSafe model pricing rechecked; the pinned Jev rate and free output are unchanged. Review window refreshed to September 28 through October 4 UTC, failing closed October 5. One-cent permanent reservation and the existing shared $3 cap/ledger remain unchanged. Added two mocked date-boundary tests; existing mocked calls now use the review-start date. Local check 10d3bcc5c43a42b1b5bbf4b998834a5e passed. All four hosted Windows/Linux Python 3.11/3.13 jobs pass. No live calls or ledger access during this update; historical smoke results remain historical.

Pricing-review verification: https://github.com/Ppetip/curriculum-forge/actions/runs/36441142826

2026-09-28 23:00 UTC: Added bounded threshold comparison with full preflight, confusion counts, nullable precision/recall and false-positive/false-negative IDs. Six regressions cover tradeoffs, order/parity, invalid thresholds, unfinished/repeated labels, empty data and text/metadata omission. Local check 6253dad59e924841806058d6c3afb1ea passed. All four hosted Windows/Linux Python 3.11/3.13 jobs pass. Synthetic example labels are authored, not independent review; no threshold chosen, training or paid calls.

Threshold-comparison verification: https://github.com/Ppetip/curriculum-forge/actions/runs/36496054658

2026-09-29 23:00 UTC: The optional local runner now exposes threshold-comparison at fixed demonstration values 0.5/0.7/1.0 with authorized --input support and private error-count summaries. No threshold is selected or recommended. All five common checks pass (312 app tests, 31 CLI paths), plus 44 shared-runner regressions. Check run 5e891ea4ba6c48658f9dcb20c00c1d26. Shared integration stays local to the AI Lab workspace; app-source hosted evidence is unchanged. Documentation-only update skips redundant CI. No live calls.

2026-09-30 23:03 UTC: Shared local runner now offers Budget Cortex random-baseline with fixed seed 7, budget 22 and target 0.7; full comparisons and input origin appear in private reports. All five required common checks pass (326 app tests, 33 CLI paths), plus 50 shared-runner regressions. Check run 79735bdda73e449d86dd8b4d521efcb2. App implementation unchanged; prior exact-source hosted evidence retained and this documentation update skips redundant CI. Shared runner is local AI Lab integration, not bundled in standalone repositories. No live calls or ledger changes.

2026-10-01 11:07 UTC: Threshold comparison now computes each lexical score once and reuses validated score/label records within that call. No persistent cache, schema change, automatic selection or raw-text output added. Three new regressions verify two scoring calls for two pairs across twenty thresholds with metric/error-ID parity, fresh scoring after input changes, and invalid late thresholds/labels before scoring. Existing hand-checked confusion-count and boundary tests also pass. Common check cbe849eea5bb4b858a50af0b2a61a923 passes 62 tests and five CLI paths. All four hosted Windows/Linux Python 3.11/3.13 jobs pass. No measured runtime-speedup claim, training, private-data analysis, paid calls or ledger changes.

Score-reuse verification: https://github.com/Ppetip/curriculum-forge/actions/runs/36853864242
