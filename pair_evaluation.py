# SPDX-License-Identifier: GPL-3.0-only
"""Evaluate lexical duplicate detection on explicitly labeled pairs; no training."""
import argparse
import json
from pathlib import Path
from app import similarity, normalize


def evaluate_pairs(pairs, threshold=.85):
    if type(threshold) not in (int, float) or not 0 < threshold <= 1:
        raise ValueError("threshold must lie in (0, 1]")
    if not isinstance(pairs, list):
        raise ValueError("pairs must be an array")
    pair_keys = set()
    ids, counts, decisions = set(), {"tp":0,"fp":0,"fn":0,"tn":0}, []
    for pair in pairs:
        if (not isinstance(pair, dict) or not isinstance(pair.get("id"), str) or not pair["id"]
                or pair["id"] in ids or type(pair.get("duplicate")) is not bool
                or any(not isinstance(pair.get(k), str) or not normalize(pair[k]) for k in ("left","right"))):
            raise ValueError("unique IDs, nonempty text pairs and boolean labels required")
        key = tuple(sorted((normalize(pair["left"]), normalize(pair["right"]))))
        if key in pair_keys:
            raise ValueError("repeated normalized text pair; each pair must be evaluated once")
        pair_keys.add(key)
        ids.add(pair["id"])
        score = similarity(pair["left"], pair["right"])
        predicted, actual = score >= threshold, pair["duplicate"]
        bucket = "tp" if predicted and actual else "fp" if predicted else "fn" if actual else "tn"
        counts[bucket] += 1
        decisions.append({"id":pair["id"],"score":score,"predicted_duplicate":predicted,"expected_duplicate":actual,"bucket":bucket})
    tp,fp,fn = counts["tp"],counts["fp"],counts["fn"]
    return {"pairs":len(pairs),"threshold":threshold,"counts":counts,
            "precision":tp/(tp+fp) if tp+fp else None,"recall":tp/(tp+fn) if tp+fn else None,
            "decisions":decisions,"limitation":"Labels require independent review. Do not tune on a final test set; lexical similarity is not semantic equivalence."}


def fixtures():
    return [{"id":"exact","left":"Cancel my plan","right":"CANCEL my plan!","duplicate":True},
            {"id":"paraphrase","left":"Cancel my monthly subscription","right":"Stop renewing this membership","duplicate":True},
            {"id":"unrelated","left":"Find a meeting time","right":"Refund a broken order","duplicate":False}]

if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--input",type=Path);p.add_argument("--threshold",type=float,default=.85);a=p.parse_args()
    print(json.dumps({"data":"user-labeled-pairs" if a.input else "author-labeled-synthetic-fixtures",**evaluate_pairs(json.loads(a.input.read_text(encoding="utf-8")) if a.input else fixtures(),a.threshold)},indent=2))
