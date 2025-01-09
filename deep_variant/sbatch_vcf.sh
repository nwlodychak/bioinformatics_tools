#!/usr/bin/env bash
# sbatch_vcf.sh


###
# Slurm commands to request resources
###
#SBATCH --partition=express # choose from debug, express, or short
#SBATCH --job-name=buildIndex # change this name to be informative for what you are running (eg. name of key script)
#SBATCH --time=01:00:00 # max time to run in hh:mm:ss, must be at or below max for partition
#SBATCH -N 1 # nodes requested
#SBATCH -n 1 # task per node requested
#SBATCH --output="batch-%x-%j.output" # where to direct standard output
#SBATCH --mail-type=ALL
#SBATCH --mail-user=wlodychak.s 
# output file will be batch-<job-name>-<job-ID>.output and include stdout and stderr
# to capture stderr to a separate file add the --error= command to a new sbatch line


###
# Usage
###
#bash scirpts/sbatch_vcf.sh

###
# Core script
###

script_name=$(basename "$0")
1>logs/sbatch.log

function log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $script_name - $1" >&1
}

log "Loading our BINF6308 Anaconda environment."
module load anaconda3/2021.11
source activate BINF-12-2021

log "Loading samtools."
module load samtools/1.10
mkdir -p genome data results logs
GENOME_FOLDER=genome
READS_FOLDER=data
RESULTS_FOLDER=results

log "Genome Directory= $GENOME_FOLDER"
log "Data Directory= $READS_FOLDER"
log "Results Directory= $RESULTS_FOLDER"

log "Starting pipe"

log "Retrieving genome"
bash scripts/getGenome.sh
cp GRCh38_reference.fa.gz $GENOME_FOLDER
log "Genome found at $GENOME_FOLDER"

log "Indexing genome"
bash scripts/indexGenome.sh $GENOME_FOLDER
log "Genome index found at $GENOME_FOLDER"

log "Get reads"
bash scripts/getReads.sh
cp *.fastq $READS_FOLDER
log "Reads found at $READS_FOLDER"

echo "Trim reads"
bash scripts/trimReads.sh $READS_FOLDER
log "Trimmed reads found at $READS_FOLDER"

log "Align reads"
bash scripts/alignReads.sh $GENOME_FOLDER $READS_FOLDER
log "Aligned reads found at $READS_FOLDER"

log "Sort reads"
bash scripts/sort.sh $READS_FOLDER
log "Reads sorted found at $READS_FOLDER"

log "Index reads"
bash scripts/indexReads.sh $READS_FOLDER
log "indexed reads sorted found at $READS_FOLDER"
