import numpy as np
from scipy.stats import beta
from typing import List, Dict, Tuple


class Gap5ConsensusBuilder:
    def __init__(self, base_prior: float = 0.001):
        self.base_prior = base_prior
        self.bases = ['A', 'C', 'G', 'T', '-']

    def phred_to_prob(self, phred_score: int) -> float:
        """Convert Phred quality score to error probability"""
        return 10 ** (-phred_score / 10.0)

    def calculate_base_likelihoods(self,
                                   aligned_bases: List[str],
                                   quality_scores: List[int]) -> Dict[str, float]:
        """Calculate likelihood for each possible base"""
        likelihoods = {base: self.base_prior for base in self.bases}

        for base, quality in zip(aligned_bases, quality_scores):
            error_prob = self.phred_to_prob(quality)

            # Update likelihoods using Bayesian probability
            for consensus_base in self.bases:
                if consensus_base == base:
                    likelihoods[consensus_base] *= (1 - error_prob)
                else:
                    likelihoods[consensus_base] *= (error_prob / 3)

        return likelihoods

    def call_consensus(self,
                       pileup_column: List[Tuple[str, int]],
                       min_posterior: float = 0.75) -> Tuple[str, float]:
        """
        Call consensus base for a single position
        pileup_column: List of (base, quality_score) tuples
        """
        if not pileup_column:
            return ('-', 0.0)

        bases, qualities = zip(*pileup_column)

        # Calculate likelihoods for each possible base
        likelihoods = self.calculate_base_likelihoods(bases, qualities)

        # Convert to posterior probabilities
        total_likelihood = sum(likelihoods.values())
        posteriors = {
            base: likelihood / total_likelihood
            for base, likelihood in likelihoods.items()
        }

        # Find consensus base with highest posterior probability
        consensus_base = max(posteriors.items(), key = lambda x: x[1])

        if consensus_base[1] >= min_posterior:
            return consensus_base
        else:
            return ('N', 0.0)  # Uncertain call

    def build_consensus(self,
                        aligned_reads: List[List[Tuple[str, int]]]) -> str:
        """
        Build consensus sequence from multiple aligned reads
        aligned_reads: List of pileup columns, each containing (base, quality) tuples
        """
        consensus_sequence = []
        confidence_scores = []

        for pileup_column in zip(*aligned_reads):
            consensus_base, confidence = self.call_consensus(pileup_column)
            consensus_sequence.append(consensus_base)
            confidence_scores.append(confidence)

        return ''.join(consensus_sequence)


# Example usage
def example():
    # Create sample aligned reads with quality scores
    read1 = [('A', 30), ('C', 25), ('G', 35)]
    read2 = [('A', 28), ('C', 27), ('G', 32)]
    read3 = [('A', 31), ('T', 25), ('G', 34)]
    read4 = [('A', 31), ('T', 27), ('G', 34)]

    aligned_reads = [read1, read2, read3, read4]

    # Create consensus builder and generate consensus
    consensus_builder = Gap5ConsensusBuilder()
    consensus_sequence = consensus_builder.build_consensus(aligned_reads)

    return consensus_sequence


if __name__ == "__main__":
    consensus = example()
    print(f"Consensus sequence: {consensus}")
