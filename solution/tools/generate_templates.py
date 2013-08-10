import sys
import argparse
import time

from . import build_formula_index

parser = argparse.ArgumentParser()

parser.add_argument("index_basedir")
parser.add_argument("-s", type=int, dest='max_size', default=20)
args = parser.parse_args()

index_basedir = args.index_basedir

index = build_formula_index.TreeTemplatesIndex(index_basedir)

start = time.time()
index.generate_missing_templates(args.max_size)
elapsed = time.time() - start

print 'DONE IN %.3f SECONDS.' % elapsed
