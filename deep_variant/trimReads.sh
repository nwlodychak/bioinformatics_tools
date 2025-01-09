#!/usr/bin/env bash
# trimReads.sh
nice -n 19 java -jar /usr/local/programs/Trimmomatic-0.36/trimmomatic-0.36.jar PE \
    -threads 1 -phred33 \
    ${1}/SRR6808334_1.fastq \
    ${1}/SRR6808334_2.fastq \
    ${1}/SRR6808334_1.paired.fastq \
    ${1}/SRR6808334_1.unpaired.fastq \
    ${1}/SRR6808334_2.paired.fastq \
    ${1}/SRR6808334_2.unpaired.fastq \
    HEADCROP:0 \
    ILLUMINACLIP:/usr/local/programs/Trimmomatic-0.36/adapters/TruSeq3-PE.fa:2:30:10 \
    LEADING:20 TRAILING:20 SLIDINGWINDOW:4:30 MINLEN:36 \
    1>logs/trimReads.log 2>logs/trimReads.err &

