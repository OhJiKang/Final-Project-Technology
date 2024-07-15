from itertools import combinations
from util.find_subgraph_with_number_items.find_subgraph_with_number_items import find_subgraph_with_number_items
from util.execute_transaction.execute_transaction import transform_transaction
import pandas as pd

def calculate_support(subgraph, transactions):
    return sum(1 for transaction in transactions if subgraph.issubset(transaction))





def generate_association_rules(top_k_results, transactions, min_confidence=0.5):
    # top_k_results is a list of tuples (subgraph, support)
    rules = []
    
    for subgraph, support in top_k_results:
        if len(subgraph) < 2:
            continue  # We need at least two items to generate a rule
        
        for i in range(1, len(subgraph)):
            for antecedent in combinations(subgraph, i):
                antecedent = frozenset(antecedent)
                consequent = frozenset(item for item in subgraph if item not in antecedent)
                antecedent_support = calculate_support(antecedent, transactions)
                confidence = support / antecedent_support
                
                if confidence >= min_confidence:
                    consequent_support = calculate_support(consequent, transactions)
                    lift = confidence / (consequent_support / len(transactions))
                    rules.append({
                        'antecedent': list(antecedent),
                        'consequent': list(consequent),
                        'support': support,
                        'confidence': confidence,
                        'lift': lift
                    })
    return rules

def finding_association_rules(transactions,num_of_item=2,min_support=0.3):
    print("Find Subgraph")
    subgraphs=find_subgraph_with_number_items(transactions,num_of_item,min_support)
    print("Find Subgraph Done")
    rules=generate_association_rules(subgraphs,transactions,0.5)
    return rules

def find_best_recommendation_item(item,file_path,num_of_item=2,min_support=0.3):
    best_rule = None
    best_score = -1
    transactions=transform_transaction(file_path)
    item_normalized = item.strip().lower()
    rules=finding_association_rules(transactions,num_of_item,min_support)
    for rule in rules:
         # Normalize each item in antecedent for comparison (remove leading/trailing whitespace)
        antecedent_normalized = [antecedent.strip().lower() for antecedent in rule['antecedent']]
        if item_normalized in antecedent_normalized:
            score = rule['confidence']
            if score > best_score:
                best_score = score
                best_rule = rule
    return best_rule