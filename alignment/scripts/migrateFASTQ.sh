#!/usr/bin/env bash
# migrateFASTQ.sh

mkdir -p data/
cd data/
mkdir rawreads/
echo "Stores raw FASTQ reads for analysis. Not git tracked." > rawreads/README.md
cd rawreads/
cp /work/courses/BINF6308/AiptasiaMiSeq/fastq/*.fastq .

arr=(*.fastq)
count=${#arr[@]}

printf "$count file(s) transfered sucessfully. /n/n$arr"