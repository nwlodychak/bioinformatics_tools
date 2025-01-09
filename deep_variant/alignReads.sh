#!/usr/bin/env bash
# alignReads.sh
bwa mem -t 8 -R "@RG\tID:SRR6808334\tSM:bar" -p ${1}/GRCh38_reference.fa ${2}/SRR6808334_1.fastq ${2}/SRR6808334_2.fastq \
    1>${2}/SRR6808334.sam 2>logs/alignReads.err &
