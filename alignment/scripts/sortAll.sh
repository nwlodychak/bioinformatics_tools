#!/usr/bin/env bash
# sortAll.sh
# Usage: bash scripts/sortAll.sh 1>results/logs/sortAll.log 2>results/logs/sortAll.err &

mkdir -p results/sorted
resultsSorted="results/sorted/"
resultsSam="results/sam/"

function sortAll {
    for sam in $resultsSam*.sam
    do
        base=$(basename $sam .sam)
        echo "$base in progress..."
        samtools sort $resultsSam$base.sam \
            -o $resultsSorted$base.sorted.bam
        printf "$sam successfully sorted. Output at: \
        /n/t $resultsSorted$base.sorted.bam"
    done
}
sortAll