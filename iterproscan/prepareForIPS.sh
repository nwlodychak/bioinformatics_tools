#!/bin/bash
# prepareForIPS.sh

# Check for correct number of input arguments
if [ $# -ne 3 ]; then
  echo "Usage: bash prepareForIPS.sh <num_lines> <input_fasta_file> <output_file>"
  exit 1
fi

# Use head to get the top num_lines of the input file
head -n $1 $2 | \
  # Remove * symbols with sed
  sed 's/\*//g' > $3