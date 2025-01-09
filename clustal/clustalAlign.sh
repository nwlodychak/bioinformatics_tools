#!/bin/bash
# clustalAlign.sh
# Usage: "Usage: clustalAlign.sh -i <input_file> [-o <output_file>] [-t threads]"
# This script takes in a amino acid file and passes it to clustal omega
# where it is processed into an aligment file.

set -e

# Usage function
usage() {
    echo "Usage: $(basename $0) -i <input_file> [-o <output_file>] [-t threads]"
    echo "Aligns sequences using Clustal Omega"
    exit 1
}

# Cleanup function
cleanup() {
    rm -f "${BASENAME}_clustalo.log"
    exit 1
}
trap cleanup EXIT

# Parse command line options
while getopts "i:o:t:h" opt; do
    case $opt in
        i) INFILE="$OPTARG";;
        o) OUTFILE="$OPTARG";;
        t) THREADS="$OPTARG";;
        h) usage;;
        ?) usage;;
    esac
done

# Validate input
if [ ! -f "$INFILE" ]; then
    echo "Error: Input file $INFILE does not exist."
    exit 1
fi

if [ ! -s "$INFILE" ]; then
    echo "Error: Input file is empty"
    exit 1
fi

if [[ ! $INFILE =~ \.fasta$ ]] && [[ ! $INFILE =~ \.fa$ ]]; then
    echo "Error: Input file must have .fasta or .fa extension"
    exit 1
fi

# Set default output file if not specified
if [ -z "$OUTFILE" ]; then
    BASENAME=$(echo ${INFILE} | awk -F_aa.fasta '{print $1}')
    OUTFILE="${BASENAME}_alignment.fasta"
fi

# Check for clustalo
if ! command -v clustalo >/dev/null 2>&1; then
    echo "Error: Clustal Omega (clustalo) is not installed or not in PATH"
    exit 1
fi

# Backup existing output
if [ -f "$OUTFILE" ]; then
    backup="${OUTFILE}.$(date +%Y%m%d_%H%M%S).bak"
    mv "$OUTFILE" "$backup"
    echo "Existing output file backed up to $backup"
fi

# Run alignment
echo "Starting alignment..."
start_time=$(date +%s)

clustalo -i "$INFILE" \
         -o "$OUTFILE" \
         --force \
         --threads="${THREADS:-1}" \
         --verbose \
         2> "${BASENAME}_clustalo.log"

end_time=$(date +%s)
runtime=$((end_time - start_time))

# Check results
if [ $? -eq 0 ] && [ -s "$OUTFILE" ]; then
    echo "Alignment complete. Results saved to $OUTFILE"
    echo "Runtime: $runtime seconds"
else
    echo "Error running Clustal Omega. Check ${BASENAME}_clustalo.log for details"
    exit 1
fi
