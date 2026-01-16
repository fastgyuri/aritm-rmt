"""
Functions for fetching and generating prime data.
"""

import requests
import math
import numpy as np
from typing import List, Tuple
import time

def fetch_oeis_sequence(seq_id: int, max_terms: int = 200) -> List[int]:
    """
    Fetch sequence from OEIS.
    
    Args:
        seq_id: OEIS sequence ID (without 'A' prefix)
        max_terms: Maximum number of terms to fetch
        
    Returns:
        List of sequence terms
    """
    url = f"https://oeis.org/A{seq_id:06d}/b{seq_id:06d}.txt"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = []
        for line in response.text.strip().split('\n'):
            if line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) >= 2:
                try:
                    val = int(parts[1].strip())
                    data.append(val)
                    if len(data) >= max_terms:
                        break
                except ValueError:
                    continue
        return data
    except Exception as e:
        print(f"Error fetching A{seq_id}: {e}")
        # Return fallback data for common sequences
        return get_fallback_sequence(seq_id, max_terms)

def get_fallback_sequence(seq_id: int, max_terms: int) -> List[int]:
    """Fallback data for when OEIS is unavailable."""
    # Known sequences from the paper
    if seq_id == 5250:  # A005250: Record gaps
        return [1, 2, 4, 6, 8, 14, 18, 20, 22, 34, 36, 44, 52, 72, 86, 96, 112, 114, 118, 132]
    elif seq_id == 101:  # A000101: Starting primes
        return [2, 3, 7, 23, 89, 113, 523, 887, 1129, 1327, 9551, 15683, 19609, 31397, 155921]
    return []

def sieve_of_eratosthenes(limit: int) -> List[int]:
    """
    Generate all primes up to limit using Sieve of Eratosthenes.
    
    Args:
        limit: Maximum number to check
        
    Returns:
        List of primes <= limit
    """
    if limit < 2:
        return []
    
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[:2] = False
    sieve[4::2] = False
    
    for i in range(3, int(limit**0.5) + 1, 2):
        if sieve[i]:
            sieve[i*i::i] = False
    
    return list(np.where(sieve)[0])

def generate_primes_sieve(limit: int) -> List[int]:
    """Wrapper for sieve with timing."""
    print(f"Generating primes up to {limit:,}...")
    start = time.time()
    primes = sieve_of_eratosthenes(limit)
    elapsed = time.time() - start
    print(f"  Generated {len(primes):,} primes in {elapsed:.2f} seconds")
    return primes

def primes_in_progression(primes: List[int], a: int, q: int) -> List[int]:
    """
    Extract primes in arithmetic progression a mod q.
    
    Args:
        primes: List of all primes
        a: Residue
        q: Modulus
        
    Returns:
        Primes ≡ a (mod q)
    """
    return [p for p in primes if p % q == a]

def calculate_gaps(primes: List[int]) -> List[int]:
    """Calculate gaps between consecutive primes."""
    return [primes[i+1] - primes[i] for i in range(len(primes)-1)]

def normalize_gap(gap: int, p: float) -> float:
    """
    Calculate normalized gap: g / ln²(p).
    
    Args:
        gap: Prime gap
        p: Starting prime
        
    Returns:
        Normalized gap R = gap / ln²(p)
    """
    if p <= 1:
        return 0.0
    return gap / (math.log(p) ** 2)
