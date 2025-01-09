#!/usr/bin/env bash
# alignReads.sh
# Usage: bash scripts/alignReads.sh 1>results/logs/alignReads.log 2>results/logs/alignReads.err &
mkdir -p results

function alignReads {
    gsnap \
    -A sam \
    -D /data \
    -d AiptasiaGmapDb \
    -N 1 \
    /data/trimmed/paired/Aip02.R1.paired.fastq \
    /data/trimmed/paired/Aip02.R2.paired.fastq \
    1>/results/sam/Aip02.sam
}
alignReads
