import os
import pandas as pd
from Bio import SeqIO
import argparse

# Get inputs
parser = argparse.ArgumentParser(
        description="Fasta to Fastq")
parser.add_argument("--fasta_path",
        help="fasta file",
        default=".")
parser.add_argument("--phred_path",
        help="fasta file",
        default=".")
parser.add_argument("--fastq_path",
        help="fastq file path")
args = parser.parse_args()

fasta_path=args.fasta_path
fastq_path=args.fastq_path
phred_path=args.phred_path
print(phred_path)
print(fasta_path)
print(fastq_path)

if not os.path.exists(fasta_path): raise Exception("No file at %s." % fasta_path)
if not os.path.exists(phred_path): raise Exception("No file at %s." % phred_path)

def main(): 
    df = pd.read_csv(args.phred_path, names=['DATA'], header=None)
    phred_values_out = phred_conversion(df)
    fastq_out = fasta_to_fastq(fasta_path, fastq_path, phred_values_out)

# Phred Value Extraction
def phred_conversion(df):
    x = df.index[df['DATA'] == "BEGIN_DNA"].tolist()
    y = df.index[df['DATA'] == "END_DNA"].tolist()
    df2 = df.iloc[(x[0]+1):(y[0])]
    df3 = df2['DATA'].str.split(' ',expand=True)
    phred_list_int = list(map(int, df3.iloc[:,1].values.tolist()))
    phred_list_int = [ 40 if score > 40 else score for score in phred_list_int ]
    print(phred_list_int, len(phred_list_int))


    return phred_list_int



# Make FastQ
def fasta_to_fastq(fasta_path, fastq_path, phred_values_out):
    with open(fasta_path, "r") as fasta, open(fastq_path, "w") as fastq:
        for record in SeqIO.parse(fasta, "fasta"):
            record.letter_annotations["phred_quality"] = phred_values_out[0:len(record)]
            SeqIO.write(record, fastq, "fastq")
            print("FASTQ found at %s" % fastq_path)

if __name__ == "__main__":
    main()