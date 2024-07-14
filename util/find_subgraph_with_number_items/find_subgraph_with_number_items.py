from collections import defaultdict,deque
import heapq

def find_subgraph_with_number_items(transactions,num_of_item=2,min_support=0.3,finding_only_rules=False):
    k=len(transactions)
    Qk = []  # Queue to store top-k subgraphs
    frequent_subgraphs = defaultdict(int)  # Dictionary to count subgraph occurrences
    Qc = []  # Priority queue for extending subgraphs
    
    # Function to calculate support of a subgraph
    def calculate_support(subgraph):
        return sum(1 for transaction in transactions if subgraph.issubset(transaction))
    
    # Initialize Qc with single items and their supports
    items = set()
    for transaction in transactions:
        items.update(transaction)
        
    for item in items:
        subgraph = frozenset([item])
        support = calculate_support(subgraph)
        if support >= min_support:
            heapq.heappush(Qc, (-support, subgraph))  # Store support as negative to use heapq as max-heap

    # Explore larger subgraphs based on the highest support in Qc
    while Qc and len(Qk) < k:
        current_support, current_subgraph = heapq.heappop(Qc)
        current_support = -current_support  # Restore original support value
        if current_support < min_support:
            continue
        
        # Add to Qk if frequent
        frequent_subgraphs[current_subgraph] = current_support
        Qk.append((current_subgraph, current_support))
        
        # Extend current_subgraph with each item and calculate support
        current_subgraph_set = set(current_subgraph)
        for item in items:
            if item not in current_subgraph_set:
                new_subgraph = frozenset(current_subgraph | {item})
                support = calculate_support(new_subgraph)
                if support >= min_support:
                    heapq.heappush(Qc, (-support, new_subgraph))  # Store support as negative to use heapq as max-heap

        # Update min_support based on the least frequent subgraph in Qk
        if len(Qk) == k:
            min_support = Qk[-1][1]

    # Return top-k subgraphs with their support
    top_k_results = [(list(subgraph), support) for subgraph, support in Qk if len(subgraph)==num_of_item]
    return top_k_results