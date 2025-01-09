#!/usr/bin/env bash
#indexAll.sh
# Usage: bash scripts/indexAll.sh 1>results/logs/indexAll.log 2>results/logs/indexAll.err &

mkdir -p results/index results/reports
resultsSorted="results/sorted/"
resultsIndex="results/index/"
resultsReports="results/reports/"

function indexBam {
    for bam in $resultsSorted*.sorted.bam
    do
        echo "$bam in progress..."
        base=$(basename $bam .sorted.bam)
        samtools index \
            $resultsSorted$base.sorted.bam \
            $resultsIndex$base.out.index
        samtools flagstat \
            -O tsv \
            $resultsSorted$base.sorted.bam > \
            $resultsReports$base.flagstat.tsv
        samtools idxstats \
            $resultsSorted$base.sorted.bam > \
            $resultsReports$base.idxstat.tsv
        printf "$base completed. Results at: \
            \n\t$resultsIndex$base.out.index \
            \n\t$resultsReports$base.flagstat.tsv \
            \n\t$resultsReports$base.idxstat.tsv"
    done
}
indexBam