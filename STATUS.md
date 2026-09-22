# Status

Stage: command-line prototype with optional live Jev integration.
Verified: 38 offline tests pass; dry run and live synthetic Jev workflow pass.

Latest: Labeled-pair evaluation reports confusion counts, precision, recall and per-pair errors.

Next: Have independently reviewed pairs before tuning duplicate thresholds.

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
