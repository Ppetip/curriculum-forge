# Curriculum Forge

A training-data workshop that builds lessons from model failures and checks whether the lessons transfer.

**v0.1 development prototype · Python 3.11+ · GPL-3.0-only**

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

13 tests passed locally on Python 3.13. Other Python versions have not yet been exercised.

## Architecture

Normalization uses Unicode NFKC and case folding. Pairwise token-set Jaccard identifies lexical overlap. A union-find joins task families and transitive duplicates before seeded assignment to train/evaluation. Export writes a fresh directory and refuses to overwrite prior data.

## Reproduced example

The six-row synthetic example detects one duplicate pair and assigns both members to the same split. Group indivisibility produces a 50% evaluation split despite a requested 25%; the report exposes both fractions.

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
