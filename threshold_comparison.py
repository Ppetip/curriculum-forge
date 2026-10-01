# SPDX-License-Identifier: GPL-3.0-only
"""Compare explicit lexical thresholds without selecting or applying one."""
import argparse
import json
from pathlib import Path
from pair_evaluation import evaluate_pairs, validate_pairs, _summarize_scores


def compare_thresholds(pairs, thresholds):
    if not isinstance(thresholds, list) or not 1 <= len(thresholds) <= 20:
        raise ValueError('thresholds must be an array of 1 to 20 distinct numbers')
    if any(type(t) not in (int, float) or not 0 < t <= 1 for t in thresholds):
        raise ValueError('each threshold must lie in (0, 1]')
    if len(set(thresholds)) != len(thresholds):
        raise ValueError('thresholds must be distinct')
    validate_pairs(pairs)  # Reject missing labels and repeated pairs before scoring.
    first = evaluate_pairs(pairs, thresholds[0])
    scored = [(d['id'], d['score'], d['expected_duplicate']) for d in first['decisions']]
    comparisons = []
    for index, threshold in enumerate(thresholds):
        result = first if index == 0 else _summarize_scores(scored, threshold)
        comparisons.append({k: result[k] for k in ('threshold', 'counts', 'precision', 'recall')})
        comparisons[-1].update(
            false_positive_ids=[d['id'] for d in result['decisions'] if d['bucket'] == 'fp'],
            false_negative_ids=[d['id'] for d in result['decisions'] if d['bucket'] == 'fn'])
    return {'mode': 'threshold-comparison', 'pairs': len(pairs), 'comparisons': comparisons,
            'selected_threshold': None,
            'limitation': 'No threshold is selected or applied. Labels require independent review. Compare on development data; keep final test data untouched until the threshold is fixed. Lexical overlap is not semantic equivalence, and repeated comparisons are not independent quality estimates.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--thresholds', type=float, nargs='+', required=True)
    args = parser.parse_args()
    try:
        result = compare_thresholds(json.loads(args.input.read_text(encoding='utf-8-sig')), args.thresholds)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print(json.dumps({'data': 'caller-supplied-labels', **result}, indent=2))


if __name__ == '__main__':
    main()
