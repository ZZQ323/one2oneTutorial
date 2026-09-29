#!/usr/bin/env python3
"""
Viterbi Parser for Two-State HMM
Author: Zhuang_zhanquan
Student ID: 602

This program implements the Viterbi algorithm to segment DNA sequences
into regions of different composition using a Hidden Markov Model.
"""

import sys
import math


# ============================================================================
# PART 1: Reading Input Files
# ============================================================================

def read_hmm_file(hmm_path):
    """
    Read HMM parameters from file.
    Format:
        Line 1: num_states num_symbols alphabet (e.g., "2 4 ACGT")
        Line 2: initial probabilities for each state
        Lines 3+: transition probabilities + emission probabilities for each state

    Returns:
        states, alphabet, initial_probs, transition_probs, emission_probs
    """
    with open(hmm_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('//')]

    # Parse first line: number of states, symbols, and alphabet
    first_line = lines[0].split()
    num_states = int(first_line[0])
    num_symbols = int(first_line[1])
    alphabet = list(first_line[2])  # e.g., ['A', 'C', 'G', 'T']

    # State names: state A, state B, ...
    states = [f"state {chr(65+i)}" for i in range(num_states)]

    # Parse initial probabilities
    initial_probs_list = [float(x) for x in lines[1].split()]
    initial_probs = {states[i]: initial_probs_list[i] for i in range(num_states)}

    # Parse transition and emission probabilities for each state
    transition_probs = {}
    emission_probs = {}

    for i in range(num_states):
        line_parts = lines[2 + i].split()
        trans_probs = [float(x) for x in line_parts[:num_states]]
        emit_probs = [float(x) for x in line_parts[num_states:num_states + num_symbols]]

        for j in range(num_states):
            transition_probs[(states[i], states[j])] = trans_probs[j]

        for j, symbol in enumerate(alphabet):
            emission_probs[(states[i], symbol)] = emit_probs[j]

    return states, alphabet, initial_probs, transition_probs, emission_probs


def read_fasta_file(fasta_path):
    """
    Read DNA sequence from FASTA file.
    Handles multi-line sequences. Converts to uppercase.
    """
    sequence = []
    with open(fasta_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                continue
            sequence.append(line.upper())

    return ''.join(sequence)


# ============================================================================
# PART 2: Viterbi Algorithm Implementation
# ============================================================================

def viterbi_algorithm(sequence, states, alphabet, initial_probs, transition_probs, emission_probs):
    """
    Viterbi algorithm using log probabilities to avoid underflow.
    """
    n = len(sequence)
    num_states = len(states)

    # --- Table Generation ---
    viterbi = [[float('-inf')] * num_states for _ in range(n)]
    backptr = [[0] * num_states for _ in range(n)]

    # --- Table Initialization (position 0) ---
    first_symbol = sequence[0]
    for j, state in enumerate(states):
        init_prob = initial_probs[state]
        emit_prob = emission_probs[(state, first_symbol)]
        if init_prob > 0 and emit_prob > 0:
            viterbi[0][j] = math.log(init_prob) + math.log(emit_prob)
        else:
            viterbi[0][j] = float('-inf')

    # --- Table Filling (positions 1..n-1) ---
    # Precompute log values for speed
    log_trans = {}
    for (s_from, s_to), p in transition_probs.items():
        log_trans[(s_from, s_to)] = math.log(p) if p > 0 else float('-inf')

    log_emit = {}
    for (s, sym), p in emission_probs.items():
        log_emit[(s, sym)] = math.log(p) if p > 0 else float('-inf')

    log_init = {}
    for s, p in initial_probs.items():
        log_init[s] = math.log(p) if p > 0 else float('-inf')

    for i in range(1, n):
        symbol = sequence[i]
        for j, cur_state in enumerate(states):
            max_prob = float('-inf')
            best_prev = 0
            le = log_emit[(cur_state, symbol)]
            for k, prev_state in enumerate(states):
                prob = viterbi[i-1][k] + log_trans[(prev_state, cur_state)] + le
                if prob > max_prob:
                    max_prob = prob
                    best_prev = k
            viterbi[i][j] = max_prob
            backptr[i][j] = best_prev

    # --- Traceback ---
    best_path = [0] * n
    best_path[n-1] = max(range(num_states), key=lambda j: viterbi[n-1][j])

    for i in range(n-2, -1, -1):
        best_path[i] = backptr[i+1][best_path[i+1]]

    return [states[idx] for idx in best_path]


# ============================================================================
# PART 3: Output Formatting
# ============================================================================

def format_output(path_states):
    """
    Group consecutive same-state positions into segments.
    Positions are 1-indexed in output.
    """
    if not path_states:
        return [], 0

    segments = []
    current_state = path_states[0]
    current_start = 0

    for i in range(1, len(path_states)):
        if path_states[i] != current_state:
            segments.append((current_start + 1, i, current_state))
            current_state = path_states[i]
            current_start = i

    segments.append((current_start + 1, len(path_states), current_state))

    state_b_count = sum(1 for _, _, state in segments if state == "state B")
    return segments, state_b_count


def main():
    if len(sys.argv) != 3:
        print("Usage: python viterbi_parser.py <input HMM file> <input fasta file>")
        sys.exit(1)

    hmm_file = sys.argv[1]
    fasta_file = sys.argv[2]

    # Read input files
    states, alphabet, initial_probs, transition_probs, emission_probs = read_hmm_file(hmm_file)
    sequence = read_fasta_file(fasta_file)

    # Run Viterbi algorithm
    path_states = viterbi_algorithm(sequence, states, alphabet, initial_probs, transition_probs, emission_probs)

    # Format and print output
    segments, state_b_count = format_output(path_states)
    for start, end, state in segments:
        print(f"{start} {end} {state}")

    print(f"\nNumber of segments in state B: {state_b_count}")


if __name__ == "__main__":
    main()
