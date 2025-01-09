#!/usr/bin/env nextflow

// Pipeline parameters
params.reads = "$baseDir/data/reads/*_{1,2}.fastq.gz"
params.reference = "$baseDir/data/reference/genome.fa"
params.outdir = "results"

// Create channel for paired-end reads
read_pairs_ch = channel.fromFilePairs(params.reads)

process trim {
    publishDir "${params.outdir}/index"

    input:
    path reference

    output:
    path 'genome_index'

    script:
    """
    bash index.sh ${reference} genome_index
    """
}

process index {
    publishDir "${params.outdir}/index"

    input:
    path reference

    output:
    path 'genome_index'

    script:
    """
    bash index.sh ${reference} genome_index
    """
}

process align {
    publishDir "${params.outdir}/aligned"

    input:
    path index
    tuple val(sample_id), path(reads)

    output:
    path "${sample_id}.sam"

    script:
    """
    bash sam.sh ${index} ${reads[0]} ${reads[1]} ${sample_id}.sam
    """
}

process sort {
    publishDir "${params.outdir}/sorted"

    input:
    path sam_file

    output:
    path "${sam_file.baseName}.bam"

    script:
    """
    bash sort.sh ${sam_file} ${sam_file.baseName}.bam
    """
}

workflow {
    trim(params.reads)
    index(params.reference)
    sort(ALIGN.out)
    align(INDEX.out, read_pairs_ch)
}
