#!/bin/sh

python -m cProfile -s tottime ../simple_fintool/cmdline/root.py process --source example_long2.txt --pandas > perfdata/perflog2_pandas.txt
