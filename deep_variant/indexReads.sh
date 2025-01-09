#!/usr/bin/env bash
# index.sh
samtools index -b ${1}/SRR6808334.bam \
    1>logs/index.log 2>logs/index.err &
