#!/bin/sh

python -m cProfile -s tottime ../simple_fintool/cmdline/root.py process --source example_long2.txt > perfdata/perflog2_normal.txt
