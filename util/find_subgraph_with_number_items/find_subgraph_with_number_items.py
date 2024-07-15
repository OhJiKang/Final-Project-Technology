from collections import defaultdict,deque
import heapq

# def find_subgraph_with_number_items(transactions,num_of_item=2,min_support=0.3,finding_only_rules=False):
#     k=len(transactions)
#     Qk = []  # Queue to store top-k subgraphs
#     frequent_subgraphs = defaultdict(int)  # Dictionary to count subgraph occurrences
#     Qc = []  # Priority queue for extending subgraphs
    
#     # Function to calculate support of a subgraph
#     def calculate_support(subgraph):
#         return sum(1 for transaction in transactions if subgraph.issubset(transaction))
    
#     # Initialize Qc with single items and their supports
#     items = set()
#     for transaction in transactions:
#         items.update(transaction)
        
#     for item in items:
#         subgraph = frozenset([item])
#         support = calculate_support(subgraph)
#         if support >= min_support:
#             heapq.heappush(Qc, (-support, subgraph))  # Store support as negative to use heapq as max-heap

#     # Explore larger subgraphs based on the highest support in Qc
#     while Qc and len(Qk) < k:
#         current_support, current_subgraph = heapq.heappop(Qc)
#         current_support = -current_support  # Restore original support value
#         if current_support < min_support:
#             continue
        
#         # Add to Qk if frequent
#         frequent_subgraphs[current_subgraph] = current_support
#         Qk.append((current_subgraph, current_support))
        
#         # Extend current_subgraph with each item and calculate support
#         current_subgraph_set = set(current_subgraph)
#         for item in items:
#             if item not in current_subgraph_set:
#                 new_subgraph = frozenset(current_subgraph | {item})
#                 support = calculate_support(new_subgraph)
#                 if support >= min_support:
#                     heapq.heappush(Qc, (-support, new_subgraph))  # Store support as negative to use heapq as max-heap

#         # Update min_support based on the least frequent subgraph in Qk
#         if len(Qk) == k:
#             min_support = Qk[-1][1]

#     # Return top-k subgraphs with their support
#     top_k_results = [(list(subgraph), support) for subgraph, support in Qk if len(subgraph)==num_of_item]
#     return top_k_results
def find_subgraph_with_number_items(transactions, num_of_item=2, min_support=0.3, finding_only_rules=False):
    frequent_subgraphs = defaultdict(int)  # Dictionary to count subgraph occurrences
    Qc = []  # Priority queue for extending subgraphs
    hsups = {}  # Dictionary to store highest support for each extension
    
    # Function to calculate support of a subgraph
    def calculate_support(subgraph):
        return sum(1 for transaction in transactions if subgraph.issubset(transaction))
    
    # Initial scan of the database to calculate support of single edge graphs
    items = set()
    for transaction in transactions:
        items.update(transaction)
        
    for item in items:
        subgraph = frozenset([item])
        support = calculate_support(subgraph)
        if support >= min_support:
            heapq.heappush(Qc, (-support, subgraph))  # Store support as negative to use heapq as max-heap
            hsups[subgraph] = support  # Store the highest support

    # Explore larger subgraphs based on the highest support in Qc
    while Qc:
        current_support, current_subgraph = heapq.heappop(Qc)
        current_support = -current_support  # Restore original support value
        if current_support < min_support:
            continue
        
        # Add to frequent_subgraphs if frequent
        frequent_subgraphs[current_subgraph] = current_support
        
        # Extend current_subgraph with each item and calculate support
        current_subgraph_set = set(current_subgraph)
        for item in items:
            if item not in current_subgraph_set:
                new_subgraph = frozenset(current_subgraph | {item})
                
                # Skip strategy
                remaining_graphs = len(transactions) - len(frequent_subgraphs)
                if hsups.get(new_subgraph, 0) + remaining_graphs < min_support:
                    continue
                
                support = calculate_support(new_subgraph)
                if support >= min_support:
                    heapq.heappush(Qc, (-support, new_subgraph))  # Store support as negative to use heapq as max-heap
                    hsups[new_subgraph] = support  # Update the highest support

    # Return all subgraphs with their support
    all_frequent_subgraphs = [(list(subgraph), support) for subgraph, support in frequent_subgraphs.items() if len(subgraph) == num_of_item]
    return all_frequent_subgraphs


# def find_subgraph_with_number_items(transactions,num_of_item=2,min_support=0.3,finding_only_rules=False):
#     k = len(transactions)
#     Qk = []  # Queue to store top-k subgraphs
#     frequent_subgraphs = defaultdict(int)  # Dictionary to count subgraph occurrences
#     Qc = []  # Priority queue for extending subgraphs
    
#     # Function to calculate support of a subgraph
#     def calculate_support(subgraph):
#         return sum(1 for transaction in transactions if subgraph.issubset(transaction))

#     # Initial scan for single-edge graphs
#     items = set()
#     initial_supports = {}
#     for transaction in transactions:
#         items.update(transaction)
    
#     for item in items:
#         subgraph = frozenset([item])
#         support = calculate_support(subgraph)
#         initial_supports[subgraph] = support
#         if support >= min_support:
#             heapq.heappush(Qc, (-support, subgraph))  # Store support as negative to use heapq as max-heap

#     # Adjust min_support based on single-edge graphs
#     min_support = max(min_support, min(initial_supports.values()))

#     # Explore larger subgraphs based on the highest support in Qc
#     while Qc and len(Qk) < k:
#         current_support, current_subgraph = heapq.heappop(Qc)
#         current_support = -current_support  # Restore original support value
#         if current_support < min_support:
#             continue
        
#         # Add to Qk if frequent
#         frequent_subgraphs[current_subgraph] = current_support
#         Qk.append((current_subgraph, current_support))
        
#         # Extend current_subgraph with each item and calculate support
#         current_subgraph_set = set(current_subgraph)
#         extensions = []
#         for item in items:
#             if item not in current_subgraph_set:
#                 new_subgraph = frozenset(current_subgraph | {item})
#                 support = calculate_support(new_subgraph)
#                 if support >= min_support:
#                     extensions.append((support, new_subgraph))
        
#         # Apply the skip strategy
#         if extensions:
#             hsup = max(support for support, subgraph in extensions)
#             rn = len(transactions) - len(frequent_subgraphs)
#             if hsup + rn < min_support:
#                 continue
        
#             for support, new_subgraph in extensions:
#                 heapq.heappush(Qc, (-support, new_subgraph))  # Store support as negative to use heapq as max-heap

#         # Update min_support based on the least frequent subgraph in Qk
#         if len(Qk) == k:
#             min_support = Qk[-1][1]

#     # Return top-k subgraphs with their support
#     top_k_results = [(list(subgraph), support) for subgraph, support in Qk if len(subgraph) == num_of_item]
#     return top_k_results