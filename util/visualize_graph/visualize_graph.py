import itertools
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules,fpgrowth
from util.find_top_k_subgraph.find_top_k_subgraph import find_top_k_subgraphs,find_top_k_subgraphs_author
from util.find_subgraph_with_number_items.find_subgraph_with_number_items import find_subgraph_with_number_items
from util.execute_transaction.execute_transaction import transform_transaction

import networkx as nx
from collections import Counter
from collections import defaultdict,deque
import heapq
import random



# Function to find frequent subgraphs using DFS



def visualize_graph(file_path,K):
     # Process transactions
            transactions = pd.read_csv(file_path)['Product'].dropna().tolist()
            transactions=[item.split(', ') for item in transactions]
            te = TransactionEncoder()
            te_ary = te.fit_transform(transactions)
            df = pd.DataFrame(te_ary, columns=te.columns_)
            # Step 2: Apply Apriori Algorithm to find frequent itemsets
            frequent_itemsets = apriori(df, min_support=0.1, use_colnames=True)
            # Step 3: Generate Association Rules
            rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
            # Step 4: Filter for itemsets with at least 2 items and sort by support
            frequent_patterns = frequent_itemsets[frequent_itemsets['itemsets'].apply(lambda x: len(x) == 4)]
            frequent_patterns = frequent_patterns.sort_values(by='support', ascending=False)
            # Step 5: Filter Top K Pattern
            top_k_patterns = frequent_patterns.head(K)
            # Step 6: Return data to visualize 
            nodes = [{'id': item} for itemset in top_k_patterns['itemsets'] for item in itemset]
            nodes = {node['id']: node for node in nodes}.values()
            edges = []
            colors = itertools.cycle(['red', 'green', 'blue', 'orange', 'purple', 'brown', 'pink', 'gray'])
            for index, (itemset, color) in enumerate(zip(top_k_patterns['itemsets'], colors)):
                items = list(itemset)
                for i in range(len(items)):
                    for j in range(i + 1, len(items)):
                        edges.append({'source': items[i], 'target': items[j], 'color': color})
            graph_data = {'nodes': list(nodes), 'links': edges}
            return graph_data
def visualize_graph_2(file_path,K):
        transactions = transform_transaction(file_path)
        # Process transactions
        min_support = 10

        top_k_subgraphs = find_top_k_subgraphs_author(transactions,K,min_support)
        # Flatten the list of lists and remove duplicates
        # unique_items = set(item.strip() for sublist in top_k_subgraphs for item in sublist)
        # Step 6: Return data to visualize
        nodes = [{'id': item} for subgraph, support in top_k_subgraphs for item in subgraph]
        nodes = {node['id']: node for node in nodes}.values()
        edges = []
        color_space = [
        'red', 'green', 'blue', 'orange', 'purple', 
        'brown', 'pink', 'gray', 'cyan', 'magenta', 
        'yellow', 'lime', 'teal', 'lavender', 'brown', 
        'beige', 'maroon', 'mint', 'olive', 'coral', 
        'navy', 'black', 'white', 'silver', 'gold'
        ]
        colors = itertools.cycle(color_space)

        for index, (subgraph, color) in enumerate(zip(top_k_subgraphs, colors)):
            items = subgraph[0]  # extract the subgraph
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    edges.append({'source': items[i], 'target': items[j], 'color': color})
    
        graph_data = {'nodes': list(nodes), 'links': edges}

        return graph_data

def visualize_graph_3(file_path,num_of_item):
        transactions = transform_transaction(file_path)
        # Process transactions
        frequent_subgraphs = find_subgraph_with_number_items(transactions,num_of_item)
        # Flatten the list of lists and remove duplicates
        # unique_items = set(item.strip() for sublist in top_k_subgraphs for item in sublist)
        # Step 6: Return data to visualize
        nodes = [{'id': item} for subgraph, support in frequent_subgraphs for item in subgraph]
        nodes = {node['id']: node for node in nodes}.values()

        edges = []
        color_space = [
        'red', 'green', 'blue', 'orange', 'purple', 
        'brown', 'pink', 'gray', 'cyan', 'magenta', 
        'yellow', 'lime', 'teal', 'lavender', 'brown', 
        'beige', 'maroon', 'mint', 'olive', 'coral', 
        'navy', 'black', 'white', 'silver', 'gold'
        ]
        colors = itertools.cycle(color_space)

        for index, (subgraph, color) in enumerate(zip(frequent_subgraphs, colors)):
            items = subgraph[0]  # extract the subgraph
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    edges.append({'source': items[i], 'target': items[j], 'color': color})
    
        graph_data = {'nodes': list(nodes), 'links': edges}

        return graph_data

