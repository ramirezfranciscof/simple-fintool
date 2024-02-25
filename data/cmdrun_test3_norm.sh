#!/bin/sh

python -m cProfile -s tottime ../simple_fintool/cmdline/root.py process --source example_long3.txt > perfdata/perflog3_normal.txt
