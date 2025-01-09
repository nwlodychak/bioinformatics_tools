#!/usr/bin/env bash
# pfamScan.sh
# Usage: bash scripts/pfamScan.sh 1>results/logs/pfamScan.log 2>results/logs/pfamScan.err

#<DOMTBLOUT> might be 'results/pfam.domtblout'
#<PFAMA_PATH> might be '/work/courses/BINF6308/inputFiles/SampleDataFiles/Pfam-A.hmm'
#<LONGEST_ORFS> might be 'results/trinity_de_novo.transdecoder_dir/longest_orfs.pep'

hmmscan --cpu 4 --domtblout $1 \
    $2 \
    $3