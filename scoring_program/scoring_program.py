import sys
import json
import os
import csv
import statistics
from typing import List, Tuple
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--ref", type=str, default="./data/ADoBo-Validation/input.csv")
parser.add_argument("--res", type=str, default="../results.csv")
parser.add_argument("--scores", type=str, default="../scores.json")
args = parser.parse_args()

def normalize_spans(spans: List[str]) -> List[str]:
	normalized_spans = []
	for span in spans:
		if not span:  # if span is empty we skip it
			continue
		span = span.lower() # span to lowercase
		span = span.strip(' \"\'') # remove trailing whitespaces and quotation marks
		normalized_spans.append(span)
	return normalized_spans

def p_r_f1(tp: int, fp: int, fn: int) -> Tuple[float, float, float]:
    p = tp / (fp + tp) if (fp + tp) > 0 else 0.0
    r = tp / (fn + tp) if (fn + tp) > 0 else 0.0
    f1 = statistics.harmonic_mean([p, r])
    return p, r, f1

print('Reading reference and prediction')

fp = 0
fn = 0
tp = 0

with open(args.ref, mode='r', encoding='utf-8', newline='') as goldstandard, \
     open(args.res, mode='r', encoding='utf-8', newline='') as prediction:
	reader_gold = csv.reader(goldstandard, delimiter=';')
	reader_pred = csv.reader(prediction, delimiter=';')

	for row_gold, row_pred in zip(reader_gold, reader_pred):
		if row_gold[0] != row_pred[0]: # sentences for the gold and pred files must match
			print(row_gold[0])
			print(row_pred[0])
			raise Exception("Sentences for the gold and pred files must match!")
		else:
			spans_gold = set(normalize_spans(row_gold[1:]))
			spans_pred = set(normalize_spans(row_pred[1:]))

		print(f"correct spans: {spans_gold} \guessed spans: {spans_pred}")
		tp = tp + len(spans_gold & spans_pred)
		fp = fp + len(spans_pred - spans_gold)
		fn = fn + len(spans_gold - spans_pred)

precision, recall, f1 = p_r_f1(tp, fp, fn)

print('Scores:')

scores = {
    'precision': precision,
    'recall': recall,
    'f1': f1
}

print(scores)

with open(args.scores, 'w') as score_file:
    score_file.write(json.dumps(scores))
