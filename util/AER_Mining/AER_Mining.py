import itertools
def calculate_support(pattern, frequencies):
    # Calculate the support of a pattern based on frequencies
    support = 0
    for items, freq in frequencies.items():
        if all(item in items for item in pattern):
            support += freq
    return support

def calculate_confidence(antecedent, consequent, frequencies):
    rule_support = calculate_support(antecedent + consequent, frequencies)
    antecedent_support = calculate_support(antecedent, frequencies)
    return rule_support / antecedent_support if antecedent_support else 0

def calculate_lift(antecedent, consequent, frequencies):
    rule_support = calculate_support(antecedent + consequent, frequencies)
    antecedent_support = calculate_support(antecedent, frequencies)
    consequent_support = calculate_support(consequent, frequencies)
    total_support = sum(frequencies.values())
    expected_confidence = (antecedent_support / total_support) * (consequent_support / total_support)
    return rule_support / (expected_confidence * total_support) if expected_confidence else 0


def AER_Transaction_Rules(transactions,minsup=0.03,minlift=0.04,minconf=0.02):
    # Extract items and their frequencies
    frequencies = {tuple(sublist): freq for sublist, freq in transactions}
    # Get unique items
    attribute_list = sorted(set(itertools.chain(*[list(item) for item in frequencies.keys()])))

    # Initialize core patterns
    map_candidates = [{tuple([attr]): frequencies} for attr in attribute_list]
    # Step 2: Pattern Growth
    list_patterns = []
    k = 1
    while map_candidates:
        new_map_candidates = []
        for candidate in map_candidates:
            for pattern, instances in candidate.items():
                for attr in attribute_list:
                    if attr > pattern[-1]:
                        new_pattern = pattern + (attr,)
                        new_support = calculate_support(new_pattern, frequencies)
                        support = new_support / sum(frequencies.values())
                        if support >= minsup:
                            confidence = calculate_confidence(pattern, (attr,), frequencies)
                            lift = calculate_lift(pattern, (attr,), frequencies)
                            if lift >= minlift:
                                new_map_candidates.append({new_pattern: frequencies})
                                if confidence >= minconf:
                                    list_patterns.append({
                                        'antecedent': list(pattern),
                                        'consequent': [attr],
                                        'support': support,
                                        'confidence': confidence,
                                        'lift': lift
                                    })
        map_candidates = new_map_candidates
        k += 1
    return list_patterns
def AER_Transaction_Rules_Without_Condition(transactions):
    # Extract items and their frequencies
    frequencies = {tuple(sublist): freq for sublist, freq in transactions}
    # Get unique items
    attribute_list = sorted(set(itertools.chain(*[list(item) for item in frequencies.keys()])))

    # Initialize core patterns
    map_candidates = [{tuple([attr]): frequencies} for attr in attribute_list]

    # Step 2: Pattern Growth
    list_patterns = []
    k = 1

    while map_candidates:
        new_map_candidates = []
        for candidate in map_candidates:
            for pattern, instances in candidate.items():
                for attr in attribute_list:
                    if attr > pattern[-1]:
                        new_pattern = pattern + (attr,)
                        new_support = calculate_support(new_pattern, frequencies)
                        support = new_support / sum(frequencies.values())
                        if support > 0:
                            confidence = calculate_confidence(pattern, (attr,), frequencies)
                            lift = calculate_lift(pattern, (attr,), frequencies)
                            if lift > 0:
                                new_map_candidates.append({new_pattern: frequencies})
                                if confidence > 0:
                                    list_patterns.append({
                                        'antecedent': list(pattern),
                                        'consequent': [attr],
                                        'support': support,
                                        'confidence': confidence,
                                        'lift': lift
                                    })
        map_candidates = new_map_candidates
        k += 1
    return list_patterns
