# BioPython_seqio.py
# Author: Nick Wlodychak
# Date: 23-09-24

"""
This script takes in a fasta file and writes out a second one
with the SeqRecords reverse complement.
"""

from Bio import SeqIO
import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description="Convert a Fasta file to its reverse complement.")
    parser.add_argument("-i", "--infile",
                        help="Input FASTA file.",
                        metavar="infile",
                        required=True,
                        default=".")
    parser.add_argument("-o", "--outfile",
                        help="Output FASTA file.",
                        metavar="outfile",
                        required=True,
                        default=".")
    args = parser.parse_args()
    return args


def reverse_complement_fasta(input_file, output_file):
    sequences = list(SeqIO.parse(input_file, "fasta"))
    reverse_complements = [seq.reverse_complement
                           (id=seq.id, description=seq.description)
                           for seq in sequences]
    SeqIO.write(reverse_complements, output_file, "fasta")


if __name__ == "__main__":
    args = get_args()
    reverse_complement_fasta(args.infile, args.outfile)
