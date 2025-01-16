import csv
import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description="Convert a list of sequences to their reverse complement.")
    parser.add_argument("-i", "--infile",
                        help="Input file containing sequences to reverse complement.",
                        metavar="infile",
                        required=True,
                        default=".")
    parser.add_argument("-o", "--outfile",
                        help="Output location to write to.",
                        metavar="outfile",
                        required=True,
                        default=".")
    args = parser.parse_args()
    return args


def reverse_complement(seq):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement[nuc] for nuc in reversed(seq))

def process_csv(input_file, output_file):
    with open(input_file, 'r') as csv_read_file:
        csv_reader = csv.reader(csv_read_file)
        with open(output_file, 'w', newline='') as csv_write_file:
            csv_writer = csv.writer(csv_write_file)
            header = next(csv_reader)
            csv_writer.writerow(header + ['Reverse_Complement'])

            for row in csv_reader:
                original_seq = row[0].upper()
                rev_comp_seq = reverse_complement(original_seq)
                csv_writer.writerow([original_seq, rev_comp_seq])

# Use the function with the input and output file paths

args = get_args()
process_csv(args.infile, args.outfile)
