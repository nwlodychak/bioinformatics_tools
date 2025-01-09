#!/usr/bin/env bash
# getReads.sh

# Retrieve the NGS reads from the NA12878 reference sample
fastq-dump --split-files SRR6808334 1>logs/getReads.log 2>logs/getReads.err
