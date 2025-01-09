

INPUT_FQ=
OUTPUT_FA=
BLAST_RESULTS=

seqtk seq -a $INPUT_FQ > ${OUTPUT_FA}.fa
seqtk seq -A ${OUTPUT_FA}.fa | head -n 10000 > ${OUTPUT_FA}.trunc.fa
blastn -db nt -query ${OUTPUT_FA}.trunc.fa -outfmt "6 qseqid sseqid pident length mismatch evalue bitscore staxids sscinames" -max_target_seqs 5 -out blast_results.txt -remote
cut -f9 blast_results.txt | sort | uniq -c | sort -nr


cut -f2 blast_results.txt | cut -d'|' -f4 | efetch -db nucleotide -format gb

blastn -db nt -query ${OUTPUT_FA}.trunc.fa -outfmt "6 qseqid sseqid sacc stitle pident length mismatch evalue bitscore staxids sscinames" -max_target_seqs 5 -out blast_results_detailed.txt -remote
