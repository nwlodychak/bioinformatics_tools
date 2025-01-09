#!/usr/bin/env bash
# runIPS.sh
# usage: bash scripts/runIPS.sh <input> <output> 1>results/logs/runIPS.log 2>results/logs/runIPS.err

# Check if input and output file arguments were provided
if [ $# -ne 2 ]; then
  echo "Usage: bash runIPS.sh <input> <output>"
  exit 1
fi

# Set variables
cpus=2

# Run InterProScan
interproscan.sh -i $1 -f tsv -o $2 --goterms --pathways -dp -cpu $cpus \ 
1>results/logs/runIPS.log 2>results/logs/runIPS.err