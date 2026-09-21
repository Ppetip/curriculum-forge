# Reading dataset audit results

A zero CLI exit code means the audit ran; it does not certify a leak-free or useful training dataset.

- `rows` counts input rows and `duplicates` lists flagged lexical pairs, not the number of unique duplicate clusters.
- Count `manifest[].split` to see the actual train/eval row counts. Indivisible groups can prevent the requested fraction.
- `warnings` identifies insufficient independent groups. Zero warnings does not prove semantic duplicates are absent.
- The synthetic default currently has six rows, one flagged pair, and a 5/1 train/eval split.

Jaccard overlap is a lexical heuristic. Review semantic paraphrases and task families before training. Jev review is advisory. The tool does not train an LLM or measure downstream quality. Export checks verify content/provenance consistency with the supplied manifest.
