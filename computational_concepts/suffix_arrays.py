from typing import Tuple

S = "BLACKSPHINXOFQUARTZ"
P = "QUARTZ"
n = len(S)

# Function to construct the suffix array
def build_suffix_array(S):
    suffixes = [(S[i:], i) for i in range(len(S))]
    suffixes.sort()  # Sort based on the suffix strings
    print(suffixes)
    return [suffix[1] for suffix in suffixes]

# Function to get the suffix at a given index in the suffix array
A = build_suffix_array(S)
print(A)

def suffixAt(index):
    return S[A[index]:]

def search(P: str) -> Tuple[int, int]:
    """
    Return indices (s, r) such that the interval A[s:r] (including the end
    index) represents all suffixes of S that start with the pattern P.
    """
    # Find starting position of interval
    l = 0  # in Python, arrays are indexed starting at 0
    r = n
    while l < r:
        mid = (l + r) // 2  # division rounding down to nearest integer
        # suffixAt(A[i]) is the ith smallest suffix
        if P > suffixAt(mid):
            l = mid + 1
        else:
            r = mid
    s = l

    # Find ending position of interval
    r = n
    while l < r:
        mid = (l + r) // 2
        if suffixAt(mid).startswith(P):
            l = mid + 1
        else:
            r = mid
    return (s, r)

# Test the search function
result = search(P)
print(f"The pattern '{P}' is found in the interval: {result}")


def build_suffix_array(genome):
    suffixes = [(genome[i:], i) for i in range(len(genome))]
    suffixes.sort()
    return [s[1] for s in suffixes]  # Return only the indices

def search_mmp(read, genome, suffix_array):
    left, right = 0, len(suffix_array) - 1
    while left <= right:
        mid = (left + right) // 2
        suffix_start = suffix_array[mid]
        # Changed comparison to check if suffix starts with read
        if genome[suffix_start:].startswith(read):
            return suffix_start
        elif read < genome[suffix_start:]:
            right = mid - 1
        else:
            left = mid + 1
    return -1


def star_align_read(read, genome, suffix_array):
    # Step 1: Seed Searching
    seeds = []
    remaining_read = read
    while remaining_read:
        mmp_start = search_mmp(remaining_read, genome, suffix_array)
        if mmp_start == -1:
            break
        mmp_length = 0
        while mmp_length < len(remaining_read) and mmp_length < len(genome) - mmp_start:
            if remaining_read[mmp_length] != genome[mmp_start + mmp_length]:
                break
            mmp_length += 1
        seeds.append((mmp_start, mmp_length))
        remaining_read = remaining_read[mmp_length:]

    # Step 2: Clustering, Stitching, and Scoring
    return seeds  # For simplicity, we'll just return the seeds


genome = "ACTGACTGGGGAGTAGAGAGAG"
read = "GGGG"
read_length = len(read)
A = build_suffix_array(genome)
aligned = star_align_read(read, genome, A)
print(aligned)

