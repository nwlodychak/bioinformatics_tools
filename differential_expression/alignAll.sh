#!/usr/bin/env bash
# alignAll.sh

outDir='quant/'

function align {
    local sample=$1
    salmon quant -l IU \
        -1 /work/courses/BINF6309/AiptasiaMiSeq/fastq/${SAMPLE}.R1.fastq \
        -2 /work/courses/BINF6309/AiptasiaMiSeq/fastq/${SAMPLE}.R2.fastq \
        -i AipIndex \
        --validateMappings \
        -o ${outDir}${SAMPLE}
}


# Use grep and cut to obtain sample list from the AiptasiaMiseq folder
while IFS= read -r SAMPLE; do
    echo Processing ${SAMPLE}.R1.fastq and ${SAMPLE}.R2.fastq
    align ${SAMPLE}
done < <(ls /work/courses/BINF6309/AiptasiaMiSeq/fastq/ | grep Aip | cut -d. -f1 | sort | uniq)
