# BioPython_genbank.py
# Author: Nick Wlodychak
# Date: 23-09-24

"""
Fetch a GenBank record based on the type of ID and its value.
"""

from Bio import Entrez, SeqIO


def fetch_genbank_record(id_type, id_value):
    if id_type == "gi":
        handle = Entrez.efetch(db="nucleotide",
                               id=id_value,
                               rettype="gb",
                               retmode="text")
    elif id_type == "accession":
        handle = Entrez.efetch(db="nucleotide",
                               id=id_value,
                               rettype="gb",
                               retmode="text")
    else:
        raise ValueError(f"Unsupported ID type: {id_type}")

    return SeqIO.read(handle, "genbank")


def main():
    Entrez.email = input("Please enter your Entrez email address: ")
    seq1 = fetch_genbank_record("gi", "515056")
    seq2 = fetch_genbank_record("accession", "J01673.1")

    sequences = [seq1, seq2]

    for seq in sequences:
        print("\nSEQUENCE: ", seq.seq)
        print("\nFeatures for sequence:", seq.id)
        for feature in seq.features:
            print("Type:", feature.type)
            print("Location:", feature.location)
            print("Strand:", feature.strand)
            print("------------------------")


if __name__ == "__main__":
    main()
