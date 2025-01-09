#!/usr/bin/env bash
# sort.sh
samtools sort -@ 8 -m 4G ${1}/SRR6808334.sam -o ${1}/SRR6808334.bam.sorted \
    1>logs/sort.log 2>logs/sort.err &
