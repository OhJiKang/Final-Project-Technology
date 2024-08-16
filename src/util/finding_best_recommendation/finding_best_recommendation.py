from itertools import combinations
from util.find_subgraph_with_number_items.find_subgraph_with_number_items import find_all_subgraph
from util.execute_transaction.execute_transaction import transform_transaction
from util.AER_Mining.AER_Mining import AER_Transaction_Rules,AER_Transaction_Rules_Without_Condition

import pandas as pd





def finding_association_rules(transactions,items,min_conf=0.3):
    subgraphs=find_all_subgraph(transactions,0.01)
    rules=AER_Transaction_Rules(subgraphs,items,minconf=min_conf)
    return subgraphs,rules

def find_best_recommendation_item(items,file_path,min_conf=0.3):
    best_rule = None
    best_score = -1
    items_normalized = [item.strip().lower() for item in items]
    transactions=transform_transaction(file_path)
    subgraphs,rules=finding_association_rules(transactions,items,min_conf)
    for rule in rules:
        # Normalize each item in antecedent for comparison (remove leading/trailing whitespace)
        antecedent_normalized = [antecedent.strip().lower() for antecedent in rule['antecedent']]
        if items_normalized == antecedent_normalized:
            score = rule['confidence']+rule['lift']
            if score > best_score:
                best_score = score
                best_rule = rule
        if best_rule==None:
            if all(item in antecedent_normalized for item in items_normalized):
                score = rule['confidence']+rule['lift']
                if score > best_score:
                    best_score = score
                    best_rule = rule
    if best_rule==None:
        rules=AER_Transaction_Rules_Without_Condition(subgraphs,items)
        for rule in rules:
            # Normalize each item in antecedent for comparison (remove leading/trailing whitespace)
            antecedent_normalized = [antecedent.strip().lower() for antecedent in rule['antecedent']]
            if items_normalized == antecedent_normalized:
                score = rule['confidence']+rule['lift']
                if score > best_score:
                    best_score = score
                    best_rule = rule
            if best_rule==None:
                if all(item in antecedent_normalized for item in items_normalized):
                    score = rule['confidence']+rule['lift']
                    if score > best_score:
                        best_score = score
                        best_rule = rule
    return best_rule

def find_best_recommendation_item_with_database(items,file,min_conf=0.3):
    best_rule = None
    best_score = -1
    items_normalized = [item.strip().lower() for item in items]
    transactions=file
    subgraphs,rules=finding_association_rules(transactions,items,min_conf)
    print("Finding_Rules")
    for rule in rules:
        # Normalize each item in antecedent for comparison (remove leading/trailing whitespace)
        antecedent_normalized = [antecedent.strip().lower() for antecedent in rule['antecedent']]
        if items_normalized == antecedent_normalized:
            score = rule['confidence']+rule['lift']
            if score > best_score:
                best_score = score
                best_rule = rule
        if best_rule==None:
            if all(item in antecedent_normalized for item in items_normalized):
                score = rule['confidence']+rule['lift']
                if score > best_score:
                    best_score = score
                    best_rule = rule
    # if best_rule==None:
    #     rules=AER_Transaction_Rules_Without_Condition(subgraphs)
    #     for rule in rules:
    #         # Normalize each item in antecedent for comparison (remove leading/trailing whitespace)
    #         antecedent_normalized = [antecedent.strip().lower() for antecedent in rule['antecedent']]
    #         if items_normalized == antecedent_normalized:
    #             score = rule['confidence']+rule['lift']
    #             if score > best_score:
    #                 best_score = score
    #                 best_rule = rule
    #         if best_rule==None:
    #             if all(item in antecedent_normalized for item in items_normalized):
    #                 score = rule['confidence']+rule['lift']
    #                 if score > best_score:
    #                     best_score = score
    #                     best_rule = rule
    return best_rule
