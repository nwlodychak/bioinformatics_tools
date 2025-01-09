#!/usr/bin/env bash
#indexSam.sh
# Usage: bash scripts/indexSam.sh 1>results/logs/indexSam.log 2>results/logs/indexSam.err &

mkdir -p results/index

function indexBam {
    samtools index \
        results/sorted/Aip02.R2.sorted.bam \
        results/index/Aip02.R2.out.index
}
indexBam