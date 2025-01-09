#!/usr/bin/env bash
# alignPredicted_args.sh
# Usage: bash scripts/alignPredicted_args.sh 1>results/logs/alignPredicted_args.log 2>results/logs/alignPredicted_args.err

#<query> might be 'results/predictedProteins/Trinity.fasta.transdecoder.pep'
#<SWISSPROT_DB> might be '/work/courses/BINF6308/inputFiles/blastDB/swissprot' 

blastp -query $1  \
    -db $2 \
    -outfmt "6 qseqid sacc qlen slen length nident pident evalue stitle" \
    -evalue 1e-10 -num_threads 4 \
    -out 'results/alignedPredicted_args.txt'