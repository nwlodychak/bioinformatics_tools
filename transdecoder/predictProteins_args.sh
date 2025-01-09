#!/usr/bin/env bash
# predictProteins.sh
# Usage: bash scripts/predictProteins.sh 1>results/logs/predictProteins.log 2>results/logs/predictProteins.err

#<TRANSCRIPTOME> might be 'data/trinity_de_novo/Trinity.fasta'
#<TRANSDECODER_DIR> might be 'results/trinity_de_novo.transdecoder_dir'
#<DOMTBLOUT> might be 'results/pfam.domtblout'
#<OUTFMT> might be 'results/blastPep.outfmt6'

TransDecoder.Predict \
    -t $1 \
    -O $2 \
    --retain_pfam_hits $3 \
    --retain_blastp_hits $4