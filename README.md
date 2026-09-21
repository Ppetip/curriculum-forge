# Curriculum Forge

A training-data workshop that builds lessons from model failures and checks whether the lessons transfer.

**v0.1 development prototype Ãƒâ€šÃ‚Â· Python 3.11+ Ãƒâ€šÃ‚Â· GPL-3.0-only**

## What works

Audits JSONL examples, finds normalized exact and token-overlap duplicates, groups duplicate-connected records and task families, and exports train/evaluation splits with provenance hashes. Includes a Python API for prioritizing development-set failure skills.

## Run

No third-party Python dependencies. Clone this repository and run from its root:

```sh
python app.py
python app.py --input examples/dataset.jsonl --export-dir runs/first-split
```

For commands using a file under `runs/`, create that directory first (`mkdir runs`). Generated files are ignored by Git. The default demo is offline and uses invented data.

## Test

```sh
python -m unittest discover -s tests -v
```

35 tests pass on Windows and Linux with Python 3.11 and 3.13 (GitHub Actions).

## Architecture

Normalization uses Unicode NFKC and case folding. Pairwise token-set Jaccard identifies lexical overlap. A union-find joins task families and transitive duplicates before seeded assignment to train/evaluation. Export writes a fresh directory and refuses to overwrite prior data.

## Reproduced example

The six-row synthetic example detects one duplicate pair and assigns both members to the same split. The closest evaluation size is one of six rows (16.7%) versus the requested 25%; tied sizes favor the smaller set.

See [the captured output](examples/demo-output.json). Rerun `python app.py` to reproduce it.

## Limits

No LLM training or generation yet. Similarity is lexical, not semantic; pairwise comparison is quadratic. IDs and declared families do not prove dataset independence or provenance. Small connected groups may prevent the requested split fraction.

## Next experiment

Add labeled duplicate-pair evaluation, better split balancing and a measured curriculum-vs-random experiment.

The [design brief](docs/DESIGN.md) describes the larger goal, including unimplemented milestones.

## Contribute

Choose a task you know well enough to judge examples, such as support tickets, product extraction, or tool calls. Use invented or openly licensed examples. Include expected outcomes, edge cases and data provenance.

## License

Copyright (c) 2026 Ppetip. Original code is licensed under GNU GPL version 3 only; see [LICENSE](LICENSE).

## Latest development pass

Closest attainable group-size splits preserve duplicate and family groups.

Exact subset-sum balances indivisible groups; ties favor the smaller evaluation set. This remains a small-dataset implementation.

## Optional Jev workflow

Run `python jev_workflow.py` to preview the synthetic request without network access.
To opt into live calls, create a local `.env` using `.env.example`, set your TypeSafe key,
and point `JEV_BUDGET_DB` at one absolute SQLite path shared by all five projects.
Then run `python jev_workflow.py --live --env-file /absolute/path/to/.env`.
Do not commit the real configuration. No packages or model downloads are required.

The adapter pins `jev-1.13.0` and sends only the built-in synthetic fixture in this CLI.
Agent Black Box makes four replay calls; each other workflow makes one. The reusable
`Client.evaluate(state, questions)` interface supports bounded Choice questions.
Treat low-confidence decisions as abstentions; its 0.8 cutoff is a heuristic, not calibrated certainty.

The shared ledger allows at most $3 in cumulative reservations: one cent is permanently
reserved **before each attempt**, including timeouts and failed requests. It never retries
automatically. Concurrent processes share an atomic SQLite reservation. Never reset,
delete, replace or split the ledger to regain budget. This guard covers this client,
not unrelated account use. Provider billing remains authoritative.

[Official TypeSafe pricing](https://docs.typesafe.ai/models) checked 2026-09-21 lists
$0.042 per million input tokens and free output. One cent exceeds a full 65,536-input-token
request at that rate; the client also limits serialized input to 16KB. Estimates use
reported input tokens and exclude unknown failed-request usage. Calls fail closed on
2026-09-28 until pricing and the reservation bound are reviewed. Never extend the review
date without checking the provider's current terms.

[The HTTP API](https://docs.typesafe.ai/api) uses the fixed official TypeSafe endpoint.
Redirects are refused, responses are schema-checked, and error bodies/credentials are
not logged. Tests mock the provider and do not spend money.

`examples/jev-live-smoke.json` records a real 2026-09-21 model response on synthetic input.
It is a connectivity and workflow smoke check, not a quality benchmark or evidence of
training, generalization, speed or production reliability. Re-running it may change results.

Jev flags a semantic duplicate despite lexical Jaccard similarity of 0.1. Split generation remains unchanged.

## Continuous verification

[Offline checks](https://github.com/Ppetip/curriculum-forge/actions/workflows/offline.yml) run tests and JSON CLI smoke checks on Windows/Linux with Python 3.11/3.13 for pushes and pull requests. Run `python verify_demos.py` locally. Actions are pinned to immutable commits, use read-only permissions, and receive no provider secrets. Jev tests use mocks; the CLI check uses its default dry run. The workflow does not run live inference.

### First-time budget setup and recovery

For a genuinely new allowance only, run `python jev_client.py --init-budget /absolute/path/to/jev-budget.sqlite3` once, then use that exact path in `JEV_BUDGET_DB` for every app. Initialization refuses existing files, including empty files. Do not initialize a new ledger to replace lost spending history. Existing users keep their existing ledger and skip setup.

Live clients now open existing ledgers only, including at reservation time. A missing, mistyped, or empty ledger stops calls instead of silently recreating a zero balance. Restore missing history from a trusted backup; do not reset it. This prevents accidental recreation, not deliberate administrator modification or substitution of a different valid database.

## Latest reliability improvement

`export_split` now rejects stale content or provenance, duplicate/missing manifest IDs, and unknown split labels before creating the destination. Re-audit edited rows before export. These are consistency checks, not a signature or proof of source truth; they do not defend against coordinated edits to both the rows and manifest.

See [Reading results](docs/RESULTS.md) for outcome fields, denominators, abstentions and the limits of command success.
