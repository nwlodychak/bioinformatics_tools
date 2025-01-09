#!/usr/bin/env bash
# alignAll.sh
# Usage: bash scripts/alignAll.sh 1>results/logs/alignAll.log 2>results/logs/alignAll.err &

# Initialize variable to contain the suffix for the left reads
leftSuffix=".paired.R1.fastq"
rightSuffix=".paired.R2.fastq"
pairedOutPath="data/trimmed/paired/"

mkdir -p results/sam

function alignReads {
    for fastq in $pairedOutPath*$leftSuffix
    do
        base=$(basename $fastq $leftSuffix)
        echo "$base in progress."
        gsnap \
        -A sam \
        -D data \
        -d AiptasiaGmapDb \
        -N 1 \
        $pairedOutPath$base$leftSuffix \
        $pairedOutPath$base$rightSuffix \
        1>results/sam/$base.sam
        printf "$base completed successfully. Output at: \
            /n/t results/sam/$base.sam"
    done
}
alignReads