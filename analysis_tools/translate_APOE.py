from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import argparse
import re
import os

def get_args():
    """Return parsed command-line arguments."""
    parser = argparse.ArgumentParser(description="Amino Acid Translator.")
    parser.add_argument('-i', '--infile',
                        metavar='INFILE',
                        help='Path to input fasta file containing gDNA nucleotide sequence',
                        type=str,
                        required=True
                        )
    parser.add_argument('-s', '--stop',
                        help='True if translating only orfs. Defaults to True.',
                        action='store_false',
                        default=False,
                        required=False
                        )
    return parser.parse_args()

def is_dna(seq):
    """Tests for DNA Nucleotides"""
    return all(nucleotide in 'ATCGN' for nucleotide in seq)

def translate_sequences(infile, stop, outfile):
    """Converts DNA Sequence to aa sequence."""
    translated_records = []

    try:
        # Base code for translation
        for record in SeqIO.parse(infile, "fasta"):
            assert is_dna(record.seq), f"Invalid nucleotide detected in sequence. Check Record: {record.id}"
            trimmed = record.seq[:len(record.seq) - (len(record.seq) % 3)]
            translated_seq = trimmed.translate(to_stop=stop)
            translated_record = SeqRecord(translated_seq, id=record.id, description=record.description)
            translated_records.append(translated_record)
        
        # Ensure there were sequences to translate
        assert len(translated_records) > 0, "No valid sequences found in input file."
        # Write to file
        SeqIO.write(translated_records, outfile, "fasta")

    # Assertion errors for error handling
    except AssertionError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    args = get_args()
    
    # Check if the input file exists
    if not os.path.exists(args.infile):
        print(f"Error: Input file '{args.infile}' does not exist.")
        exit(1)
    
    # Output file name generation
    basename = re.match(r"(.+)\.fasta$", args.infile).group(1)
    print(f"Basename is: {basename}")
    outfile = f"{basename}_aa.fasta"
    
    # Check for write permissions in the output directory
    if not os.access(os.path.dirname(os.path.abspath(outfile)), os.W_OK):
        print(f"Error: No permission to write to the directory of {outfile}.")
        exit(1)
    
    translate_sequences(args.infile, args.stop, outfile)
    print(f"Success! Output at: {outfile}")
