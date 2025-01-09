# sliding_window_fasta.py
# Author: Nick Wlodychak
# Date: 23-09-24

"""
This script takes in a fasta file and splits into kmers of length "k"
and calculates the GC content of each kmer
"""


import argparse
from Bio import SeqIO


def get_args():
    parser = argparse.ArgumentParser(
        description="Calculate GC content for each k-mer in sequences from the provided FASTA file.")
    parser.add_argument("-k", "--ksize",
                        type=int,
                        metavar="ksize",
                        required=True,
                        help="k-mer size")
    parser.add_argument("-i", "--infile",
                        type=str,
                        metavar="infile",
                        required=True,
                        help="Input FASTA file")

    args = parser.parse_args()
    return args


def sliding_window(k, sequence):
    k_mers = []
    for i in range(len(sequence) - k + 1):
        k_mers.append(sequence[i:i + k])
    return k_mers


def gc_content(sequence):
    gc_count = sequence.count('G') + sequence.count('C')
    return gc_count / len(sequence) if len(sequence) > 0 else 0


if __name__ == "__main__":
    args = get_args()
    for record in SeqIO.parse(args.infile, "fasta"):
        print(f">{record.id}")
        sequence = str(record.seq)
        k_mers = sliding_window(args.ksize, sequence)

        for k_mer in k_mers:
            print(f"{k_mer}\t{gc_content(k_mer):.2f}")
