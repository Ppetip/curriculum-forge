# SPDX-License-Identifier: GPL-3.0-only
"""Compare two label reviews without detector scores or automatic adjudication."""
import argparse
import json
from pathlib import Path
from app import normalize
from pair_evaluation import validate_pairs


def compare_reviews(left, right):
    def index(rows):
        validate_pairs(rows, allow_unreviewed=True)
        return {tuple(sorted((normalize(row["left"]), normalize(row["right"])))): row for row in rows}
    first, second = index(left), index(right)
    counts = {name: 0 for name in ("agreement", "disagreement", "unreviewed", "left_only", "right_only")}
    pairs = []
    for key in dict.fromkeys([*first, *second]):
        a, b = first.get(key), second.get(key)
        if a is None:
            status = "right_only"
        elif b is None:
            status = "left_only"
        elif a["duplicate"] is None or b["duplicate"] is None:
            status = "unreviewed"
        else:
            status = "agreement" if a["duplicate"] == b["duplicate"] else "disagreement"
        counts[status] += 1
        pairs.append({"left_id": a["id"] if a is not None else None,
                      "right_id": b["id"] if b is not None else None,
                      "left_label": a["duplicate"] if a is not None else None,
                      "right_label": b["duplicate"] if b is not None else None, "status": status})
    both_labeled = counts["agreement"] + counts["disagreement"]
    return {"mode": "label-review-comparison", "pairs": len(pairs), "counts": counts,
            "both_labeled": both_labeled,
            "agreement_rate": counts["agreement"] / both_labeled if both_labeled else None,
            "decisions": pairs,
            "limitation": "Agreement is not correctness or proof of independent review. No labels are merged or adjudicated. Missing and null labels are excluded from the agreement denominator. Matching uses normalized unordered text pairs, not IDs; no detector scores are computed."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--left", type=Path, required=True)
    parser.add_argument("--right", type=Path, required=True)
    args = parser.parse_args()
    try:
        left = json.loads(args.left.read_text(encoding="utf-8-sig"))
        right = json.loads(args.right.read_text(encoding="utf-8-sig"))
        result = compare_reviews(left, right)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
