"""Print reproducible policy metrics; --gate fails on a regression against a saved run."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from secure_ai.evaluation import run_evaluation

parser=argparse.ArgumentParser()
parser.add_argument('--split',choices=['dev','test'],default='test')
parser.add_argument('--gate',type=Path)
args=parser.parse_args()
result=run_evaluation(args.split)
print(json.dumps(result,indent=2))
if args.gate:
    prior=json.loads(args.gate.read_text())
    if prior['dataset_sha256']!=result['dataset_sha256']:
        raise SystemExit('Dataset changed. Review and explicitly refresh the benchmark baseline.')
    if result['defended']['attack_success_rate']>prior['defended']['attack_success_rate'] or result['defended']['legitimate_task_success']<prior['defended']['legitimate_task_success']:
        raise SystemExit('Policy evaluation regressed.')
