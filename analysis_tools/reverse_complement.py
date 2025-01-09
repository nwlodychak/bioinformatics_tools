import csv

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
input_csv = '/Users/nwlodychak/Downloads/index.csv'  # Replace with your input CSV file path
output_csv = '/Users/nwlodychak/Downloads/output_index.csv'  # Replace with your output CSV file path
process_csv(input_csv, output_csv)
