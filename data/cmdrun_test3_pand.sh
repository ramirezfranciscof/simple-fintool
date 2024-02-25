#!/bin/sh

python -m cProfile -s tottime ../simple_fintool/cmdline/root.py process --source example_long3.txt --pandas > perfdata/perflog3_pandas.txt
