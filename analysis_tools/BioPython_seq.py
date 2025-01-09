# BioPython_seq.py
# Author: Nick Wlodychak
# Date: 23-09-24
"""
This script creates a generic seq record object and is
compatible with older versions of BioPython that use Bio.Alphabet
"""

# import modules
try:
    from Bio.Alphabet import generic_dna
except ImportError:
    generic_dna = None
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO

if generic_dna:
    # newer biopython refuses second argument
    seq_data = Seq("aaaatgggggggggggccccgtt", generic_dna)
else:
    seq_data = Seq("ATGCGTGCAT")

# establish record
record = SeqRecord(
    seq_data,
    id="#12345",
    description="example 1",
    annotations={"molecule_type": "DNA"}
)

# write the SeqRecord object to a file in GenBank format
SeqIO.write(record, "BioPython_seq.gb", "genbank")
