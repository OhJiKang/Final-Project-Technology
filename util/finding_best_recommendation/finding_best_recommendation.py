from itertools import combinations
from util.find_subgraph_with_number_items.find_subgraph_with_number_items import find_all_subgraph
from util.execute_transaction.execute_transaction import transform_transaction
from util.AER_Mining.AER_Mining import AER_Transaction_Rules,AER_Transaction_Rules_Without_Condition

import pandas as pd


def calculate_support(subgraph, transactions):
    return sum(1 for transaction in transactions if subgraph.issubset(transaction))




def generate_association_rules(top_k_results, transactions, min_confidence=0.5):
    # top_k_results is a list of tuples (subgraph, support)
    rules = []
    normalized_transactions = [
        {item.strip().lower() for item in transaction}
        for transaction in transactions
    ]
    for subgraph, support in top_k_results:
        if len(subgraph) < 2:
            continue  # We need at least two items to generate a rule
        
        for i in range(1, len(subgraph)):
            for antecedent in combinations(subgraph, i):
                antecedent = frozenset(antecedent)
                consequent = frozenset(item for item in subgraph if item not in antecedent)
                antecedent_support = calculate_support(antecedent, normalized_transactions)
                confidence = support / antecedent_support
                if confidence >= min_confidence:
                    consequent_support = calculate_support(consequent, normalized_transactions)
                    lift = confidence / (consequent_support / len(normalized_transactions))
                    rules.append({
                        'antecedent': list(antecedent),
                        'consequent': list(consequent),
                        'support': support,
                        'confidence': confidence,
                        'lift': lift
                    })
    return rules

def finding_association_rules(transactions,num_of_item=2,min_support=0.3):
    subgraphs=find_all_subgraph(transactions,0.3)
    rules=AER_Transaction_Rules(subgraphs,minconf=0.1)
    return subgraphs,rules

def find_best_recommendation_item(items,file_path,num_of_item=2,min_support=0.3):
    best_rule = None
    best_score = -1
    items_normalized = [item.strip().lower() for item in items]
    transactions=transform_transaction(file_path)
    subgraphs,rules=finding_association_rules(transactions,num_of_item,min_support)
    for rule in rules:
        # Normalize each item in antecedent for comparison (remove leading/trailing whitespace)
        antecedent_normalized = [antecedent.strip().lower() for antecedent in rule['antecedent']]
        if items_normalized == antecedent_normalized:
            score = rule['confidence']
            if score > best_score:
                best_score = score
                best_rule = rule
        if best_rule==None:
            if all(item in antecedent_normalized for item in items_normalized):
                score = rule['confidence']
                if score > best_score:
                    best_score = score
                    best_rule = rule
    if best_rule==None:
        rules=AER_Transaction_Rules_Without_Condition(subgraphs)
        for rule in rules:
            # Normalize each item in antecedent for comparison (remove leading/trailing whitespace)
            antecedent_normalized = [antecedent.strip().lower() for antecedent in rule['antecedent']]
            if items_normalized == antecedent_normalized:
                score = rule['confidence']
                if score > best_score:
                    best_score = score
                    best_rule = rule
            if best_rule==None:
                if all(item in antecedent_normalized for item in items_normalized):
                    score = rule['confidence']
                    if score > best_score:
                        best_score = score
                        best_rule = rule
    return best_rule
