"""Auditable dataset curation with duplicate-connected split groups."""
import argparse
import hashlib
import json
import random
import re
import unicodedata
from pathlib import Path

def normalize(text):
    return ' '.join(re.findall(r'\w+', unicodedata.normalize('NFKC', text).casefold()))

def similarity(a, b):
    a, b = set(normalize(a).split()), set(normalize(b).split())
    return len(a & b) / len(a | b) if a | b else 1.0

def audit(rows, threshold=0.85, eval_fraction=0.25, seed=7):
    if not 0 < threshold <= 1 or not 0 < eval_fraction < 1:
        raise ValueError('threshold and eval fraction must be in range')
    ids = set()
    for row in rows:
        if not isinstance(row, dict): raise ValueError('rows must be objects')
        if not all(isinstance(row.get(k), str) and row[k].strip() for k in ('id','text','family','source')):
            raise ValueError('every row requires nonempty id, text, family, source strings')
        if not normalize(row['text']): raise ValueError('text must contain lexical tokens')
        if row['id'] in ids: raise ValueError('duplicate row ID')
        ids.add(row['id'])
    parent = list(range(len(rows)))
    def find(i):
        while i != parent[i]:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    def union(i,j): parent[find(j)] = find(i)
    duplicates = []
    for i in range(len(rows)):
        for j in range(i):
            score = similarity(rows[i]['text'], rows[j]['text'])
            exact = normalize(rows[i]['text']) == normalize(rows[j]['text'])
            if rows[i]['family'] == rows[j]['family'] or score >= threshold: union(i,j)
            if score >= threshold:
                duplicates.append({'a': rows[j]['id'], 'b': rows[i]['id'], 'score': score, 'kind': 'exact' if exact else 'near'})
    groups = {}
    for i in range(len(rows)): groups.setdefault(find(i), []).append(i)
    components = sorted(groups.values(), key=lambda g: min(rows[i]['id'] for i in g))
    random.Random(seed).shuffle(components)
    split = {}; count = 0; target = max(1, round(len(rows)*eval_fraction)) if rows else 0
    # Keep at least one component in train; never break a duplicate-connected group.
    for pos, group in enumerate(components):
        label = 'eval' if count < target and pos < len(components)-1 else 'train'
        if label == 'eval': count += len(group)
        for i in group: split[rows[i]['id']] = label
    manifest = [{'id': r['id'], 'family': r['family'], 'source': r['source'], 'split': split[r['id']],
                 'sha256': hashlib.sha256(r['text'].encode()).hexdigest()} for r in rows]
    return {'rows': len(rows), 'duplicates': duplicates, 'manifest': manifest,
            'seed': seed, 'threshold': threshold, 'requested_eval_fraction': eval_fraction,
            'actual_eval_fraction': count/len(rows) if rows else 0,
            'warnings': ['Insufficient independent groups for evaluation'] if len(components)<2 else [],
            'limitation': 'Token-set Jaccard detects lexical overlap, not semantic equivalence. O(n squared); designed for small datasets. No LLM has been trained.'}

def curriculum(failures, limit=5):
    """Prioritize development failures only, never final-test labels."""
    if type(limit) is not int or limit < 1: raise ValueError('limit must be a positive integer')
    counts = {}
    for f in failures:
        if f.get('split') != 'development': raise ValueError('curriculum accepts development failures only')
        if not isinstance(f.get('skill'), str) or not f['skill'].strip(): raise ValueError('skill required')
        counts[f['skill']] = counts.get(f['skill'], 0) + 1
    return [{'skill': skill, 'failures': count, 'exercise': 'Create a new scenario and independent answer for: '+skill}
            for skill, count in sorted(counts.items(), key=lambda kv: (-kv[1],kv[0]))[:limit]]

def demo():
    texts = [('a','Extract order quantity and shipping address','orders'),('b','EXTRACT order quantity and shipping address!','orders-copy'),
             ('c','Classify refund eligibility by purchase date','refunds'),('d','Find meeting start time and timezone','calendar'),
             ('e','Identify duplicate inventory SKU records','inventory'),('f','Resolve cancellation exception in policy','exceptions')]
    return [{'id': i,'text': t,'family': f,'source': 'synthetic-demo'} for i,t,f in texts]

def export_split(rows, report, directory):
    """Write a fresh directory, refusing to overwrite any earlier dataset."""
    directory = Path(directory)
    assignments = {r['id']: r['split'] for r in report['manifest']}
    directory.mkdir(parents=True, exist_ok=False)
    for split in ('train', 'eval'):
        selected = [r for r in rows if assignments[r['id']] == split]
        (directory / (split + '.jsonl')).write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in selected), encoding='utf-8')
    (directory / 'manifest.json').write_text(json.dumps(report, indent=2), encoding='utf-8')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path);p.add_argument('--seed',type=int,default=7);p.add_argument('--threshold',type=float,default=.85)
    p.add_argument('--export-dir', type=Path, help='Create a new directory with train/eval JSONL and an audit manifest')
    a=p.parse_args();rows=demo() if a.input is None else [json.loads(s) for s in a.input.read_text().splitlines() if s.strip()]
    report = audit(rows, seed=a.seed, threshold=a.threshold)
    if a.export_dir is not None: export_split(rows, report, a.export_dir)
    print(json.dumps(report,indent=2))
if __name__=='__main__': main()
