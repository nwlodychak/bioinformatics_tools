#!/usr/bin/bash
#SBATCH --partition=short               # choose from debug, express, or short
#SBATCH --job-name=ips
#SBATCH --time=04:00:00                 
#SBATCH -N 1                            # nodes requested
#SBATCH -n 4                            # task per node requested
#SBATCH --mem=10Gb
#SBATCH --exclusive
#SBATCH --output="batch-%x-%j.output"   # where to direct standard output; will be batch-jobname-jobID.output
#SBATCH --mail-type=ALL
#SBATCH --mail-user=wlodychak.s # Update to your user name!

# Usage: sbatch sbatch_IPS.sh 
# Assumes input data is in /home/$USER/AiptasiaRNASeq/data/proteinPrediction/results/predictedProteins 

echo "Starting our analysis $(date)" 
echo 

# define key constants
INPUT_DATA_PATH=/home/$USER/AiptasiaRNASeq/data/proteinPrediction/results
PREDICTED_PROTEIN_PATH=/predictedProteins
PROTEINS=Trinity.fasta.transdecoder.pep
ALL_PROTEINS=$INPUT_DATA_PATH$PREDICTED_PROTEIN_PATH/$PROTEINS
OUTPUT_DATA_PATH=/home/$USER/AiptasiaRNASeq/data/interProScan
LINES_TO_PROCESS=all  # all # set to "all" to calculate everything or change the numeric value

# record these key constants to our batch*.output file by echoing them:
echo "Key parameters"
echo "INPUT_DATA_PATH: $INPUT_DATA_PATH"
echo "PREDICTED_PROTEIN_PATH: $PREDICTED_PROTEIN_PATH"
echo "PROTEINS: $PROTEINS"
echo "ALL_PROTEINS: $ALL_PROTEINS"
echo "OUTPUT_DATA_PATH: $OUTPUT_DATA_PATH"
echo "LINES_TO_PROCESS: $LINES_TO_PROCESS"
echo
echo


echo "Loading our BINF6308 Anaconda environment."
module load anaconda3/2021.11
source activate BINF-12-2021

echo "Make directory for data files"
mkdir -p data/

echo "Moving predicted proteins to the working directory"
cp $ALL_PROTEINS data/

echo "Make directory for log files"
mkdir -p results/logs/

echo "Starting InterProScan pipeline $(date)"
echo "Running scan on $LINES_TO_PROCESS lines of $PROTEINS"

if [ $LINES_TO_PROCESS = "all" ]
then
  file_lines=$(wc -l data/$PROTEINS | cut -f 1 -d " ")
else
  file_lines=$LINES_TO_PROCESS
fi

echo "Preparing data for InterProScan - processing $file_lines lines"
bash scripts/prepareForIPS.sh $file_lines data/$PROTEINS data/cleaned_${SLURM_JOB_ID}_$PROTEINS \
  1>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID-prepareForIPS.log \
  2>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID-prepareForIPS.err

echo "Running InterProScan on the cleaned data: data/cleaned_$PROTEINS"
bash scripts/runIPS.sh data/cleaned_${SLURM_JOB_ID}_$PROTEINS results/${SLURM_JOB_ID}_proteins.tsv \
  1>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID-runIPS.log \
  2>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID-runIPS.err

echo "Summarizing output to the results/$PROTEINS/ folder"
mkdir -p results/${SLURM_JOB_ID}/ 
bash scripts/summarizeIPStsv.sh results/${SLURM_JOB_ID}_proteins.tsv results/${SLURM_JOB_ID}/ \
  1>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID-summarizeIPStsv.log \
  2>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID-summarizeIPStsv.err

echo "InterProScan pipeline complete $(date)"

echo "Moving key files back to /home"
cp -r results/ $OUTPUT_DATA_PATH

echo "Analysis complete $(date)"