#!/usr/bin/env bash
# indexGenome.sh
bwa index -a bwtsw ${1}/GRCh38_reference.fa \
    1>logs/indexGenome.log 2>logs/indexGenome.err &
