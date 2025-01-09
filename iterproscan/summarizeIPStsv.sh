#!/usr/bin/env bash
# summarizeIPStsv.sh
# Usage: bash summarizeIPStsv.sh <input IPS tsv> <output folder>

# Check if input and output file arguments were provided
if [ $# -ne 2 ]; then
  echo "Usage: bash summarizeIPStsv.sh <input tsv> <output folder>"
  exit 1
fi

mkdir -p $2  # make the output folder if it doesn't exist

# Summarize domains
cut -f12,13 $1| sort | uniq -c | sort -k1 -rn >$2/domains.txt

# Summarize GO Terms
cut -f14 $1 | \
perl -ne '@list=split/\|/, $_; foreach my $i (@list){ print "$i\n"; }' | \
sort | uniq -c | sort -k1 -rn >$2/go_ids.txt

# Summarize paths
cut -f15 $1 | \
perl -ne '@list=split/\|/, $_; foreach my $i (@list){ print "$i\n"; }' | \
sort | uniq -c | sort -k1 -rn >$2/path_ids.txt