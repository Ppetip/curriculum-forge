# Curriculum Forge

A training-data workshop that builds lessons from model failures and checks whether the lessons transfer.

## Problem

More synthetic examples can amplify duplicate data and benchmark leakage without improving the target skill.

## Approach

Cluster failures by skill, generate controlled variations, deduplicate and assign provenance, then compare targeted curricula against random examples at equal token budgets. Hold out task families before generation.

## Demo concept

Teach a small local model to extract structured orders with exceptions; inspect which targeted examples improve unseen formats.

## First implementation

JSONL dataset validator, exact and near-duplicate detection, provenance manifest, group-aware train/eval split and synthetic fixtures. Clearly mark that the first version does not train an LLM.

## Evaluation

Report split leakage, precision/recall of duplicate detection on labeled pairs, downstream held-out accuracy, training tokens and random-seed variation. Do not select examples using the final test set.

## Milestones

1. Dataset audit and group-aware splitting
2. Skill taxonomy and local teacher generation
3. Small-model adapter training after hardware and license checks
4. Equal-budget curriculum ablations and dataset card

## Your contribution

Choose a task you know well enough to judge examples, such as support tickets, product extraction, or tool calls.

## Status and license

Design brief only; no implementation or measured results yet. Original code will use GPL-3.0-only.
