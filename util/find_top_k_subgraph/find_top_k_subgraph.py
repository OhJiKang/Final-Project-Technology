def find_top_k_subgraphs(transactions, k, min_support=0.3):
    Qk = []  # List to store top-k subgraphs
    frequent_subgraphs = {}  # Dictionary to count subgraph occurrences
    Qc = []  # List for extending subgraphs
    
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
            Qc.append((support, subgraph))

    # Explore larger subgraphs based on the highest support in Qc
    while Qc and len(Qk) < k:
        Qc.sort(reverse=True, key=lambda x: x[0])  # Sort Qc by support in descending order
        current_support, current_subgraph = Qc.pop(0)  # Get subgraph with highest support
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
                    Qc.append((support, new_subgraph))

        # Update min_support based on the least frequent subgraph in Qk
        if len(Qk) >= k:
            min_support = Qk[0][1]  # Update minsup to the smallest support in Qk
            if len(Qk) > k:
                Qk.sort(key=lambda x: x[0])  # Sort Qk by support in ascending order
                Qk.pop(0)  # Remove the subgraph with the least support if Qk exceeds size k
    # Return top-k subgraphs with their support
    top_k_results = [(list(subgraph), support) for subgraph, support in Qk]
    return top_k_results
