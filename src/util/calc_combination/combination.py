from itertools import combinations

def calcCombination(transaction):
    # Parse the transaction to get items
    # Generate all combinations containing 1 item to n items
    all_combinations = []
    for r in range(1, len(transaction) + 1):
        all_combinations.extend(combinations(transaction, r))
    return all_combinations

