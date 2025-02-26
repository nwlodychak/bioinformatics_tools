from typing import List, Dict, Tuple


class Gap5Consensus:
    """
    Class for building a likelihood estimate from phred score and cosensus basecall
    """
    def __init__(self, base_prior: float = 0.001):
        self.base_prior = base_prior
        self.bases = ['A', 'C', 'G', 'T', '-']

    def phred_to_prob(self, phred_score: int) -> float:
        """
        Convert phred score to probability of error
        :param phred_score: single base phred score
        :return: probability of erroneous base call (float)
        """
        return 10 ** (-phred_score / 10.0)

    def calculate_base_likelihoods(self,
                                   aligned_bases: List[str],
                                   quality_scores: List[int]) -> Dict[str, float]:
        """
        Calculate a likelihood estimate for each base call
        :param aligned_bases: stacked consensus bases
        :param quality_scores: stacked consensus scores
        :return: likelihood estimate for each base call
        """
        likelihoods = {base: self.base_prior for base in self.bases}

        for base, quality in zip(aligned_bases, quality_scores):
            error_prob = self.phred_to_prob(quality)

            # update bayesian likelihood estimate
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
        :param pileup_column: List of (base, quality_score) tuples
        :param min_posterior: Minimum posterior probability
        :return: Consensus base and quality score estimate
        """
        if not pileup_column:
            return ('-', 0.0)

        bases, qualities = zip(*pileup_column)

        # calculate likelihoods for each possible base
        likelihoods = self.calculate_base_likelihoods(bases, qualities)

        # convert to posterior probabilities
        total_likelihood = sum(likelihoods.values())
        posteriors = {
            base: likelihood / total_likelihood
            for base, likelihood in likelihoods.items()
        }

        # MAP estimate
        consensus_base = max(posteriors.items(), key = lambda x: x[1])

        if consensus_base[1] < min_posterior:
            return ('N', 0.0)  # Uncertain call

        return consensus_base

    def build_consensus(self,
                        aligned_reads: List[List[Tuple[str, int]]]) -> str:
        """
        Build consensus sequence from multiple aligned reads
        :param aligned_reads: List of pileup columns, each containing (base, quality) tuples
        :return: Consensus sequence
        """
        consensus_sequence = []
        confidence_scores = []

        for pileup_column in zip(*aligned_reads):
            consensus_base, confidence = self.call_consensus(pileup_column)
            consensus_sequence.append(consensus_base)
            confidence_scores.append(confidence)

        return ''.join(consensus_sequence)


# Example usage
if __name__ == "__main__":
    # dummy matrix
    read1 = [('A', 30), ('C', 25), ('T', 32), ('G', 35)]
    read2 = [('A', 28), ('C', 27), ('T', 28), ('G', 32)]
    read3 = [('A', 31), ('T', 25), ('T', 22), ('G', 34)]
    read4 = [('A', 31), ('T', 27), ('G', 30), ('G', 34)]

    aligned_reads = [read1, read2, read3, read4]

    # main logic
    consensus_builder = Gap5Consensus()
    consensus_sequence = consensus_builder.build_consensus(aligned_reads)
    print(f"Consensus sequence: {consensus_sequence}")
