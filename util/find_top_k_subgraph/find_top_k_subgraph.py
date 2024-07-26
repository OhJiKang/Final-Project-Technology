from util.IsCaminomal.finding_CaminomalGraph import is_canonical
from util.RightMostPathExtenstion.RightMostPathExtension import rightMostPathExtension
def find_top_k_subgraphs(transactions, k, min_support):
    Qk = []  # List to store top-k subgraphs
    Qc = []  # List for extending subgraphs
    # Function to calculate support of a subgraph
    def calculate_support(subgraph):
        return sum(1 for transaction in transactions if subgraph.issubset(transaction))
    
    # Initialize Qc with single items and their supports
    items = set()
    for transaction in transactions:
        subgraphList=[]
        for node in transaction:
            subgraphList.append(node)
        if len(transaction) > 1:
            subgraph = frozenset(subgraphList[:2])  # Chọn hai mục đầu tiên
            for _,transanctionitem in Qk:
                if subgraph.issubset(transanctionitem):
                    flagNotToDo=True
            if flagNotToDo ==True:
                continue
            support = calculate_support(subgraph)
            
            if support >= min_support:
                Qc.append((support, subgraph))
                Qk.sort(key=lambda x: x[0])  # Sort Qk by support in ascending order
                Qk.append((support, subgraph))
                if len(Qk) >= k:
                    min_support = Qk[0][0]  # Update minsup to the smallest support in Qk
                    if len(Qk) > k:
                        Qk.pop(0)  # Remove the subgraph with the least support if Qk exceeds size kss        
        # Explore larger subgraphs based on the highest support in Qc
    while Qc:
        Qc.sort(reverse=True, key=lambda x: x[0])  # Sort Qc by support in descending order
        current_support, current_subgraph = Qc.pop(0)  # Get subgraph with highest support
        if current_support > min_support:    
            current_subgraph_set = set(current_subgraph)
            for item in items:
                if item not in current_subgraph_set:
                    new_subgraph = frozenset(current_subgraph | {item})
                    support = calculate_support(new_subgraph)
                    if support >= min_support:
                        Qc.append((support, new_subgraph))
                        Qk.append((support, new_subgraph))
                        if len(Qk) >= k:
                            min_support = Qk[0][0]  # Update minsup to the smallest support in Qk
                            if len(Qk) > k:
                                Qk.sort(key=lambda x: x[0])  # Sort Qk by support in ascending order
                                Qk.pop(0)  # Remove the subgraph with the least support if Qk exceeds size k
        
    # Return top-k subgraphs with their support
    top_k_results = [(list(subgraph), support) for support, subgraph in Qk]
    return top_k_results
def find_top_k_subgraphs_author(transactions, k, min_support):
    Qk = []  # List to store top-k subgraphs
    Qc = []  # List for extending subgraphs
    # Function to calculate support of a subgraph
    def calculate_support(subgraph):
        return sum(1 for transaction in transactions if subgraph.issubset(transaction))
    
    for transaction in transactions:
        subgraphList=[]
        for node in transaction:
            subgraphList.append(node)
        if len(transaction) > 1:
            flagNotToDo=False
            subgraph = frozenset(subgraphList[:2])  # Chọn hai mục đầu tiên
            for _,transanctionitem in Qk:
                if subgraph.issubset(transanctionitem):
                    flagNotToDo=True
            if flagNotToDo ==True:
                continue
            support = calculate_support(subgraph)
            if support >= min_support:
                Qc.append((support, subgraph))
                Qk.sort(key=lambda x: x[0])  # Sort Qk by support in ascending order
                Qk.append((support, subgraph))
                if len(Qk) >= k:
                    min_support = Qk[0][0]  # Update minsup to the smallest support in Qk
                    if len(Qk) > k:
                        Qk.pop(0)  # Remove the subgraph with the least support if Qk exceeds size kss        
        # Explore larger subgraphs based on the highest support in Qc

    while Qc:
        Qc=sorted(Qc,reverse=True, key=lambda x: x[0])  # Sort Qc by support in descending order
        current_support, current_subgraph = Qc.pop(0)  # Get subgraph with highest support
        if current_support > min_support:
            current_subgraph = set(current_subgraph)
            all_extension= rightMostPathExtension(current_subgraph,transactions)
            for item in all_extension:
                edge = item.get("Extension")
                support = item.get("Support")
                new_subgraph = frozenset(current_subgraph | {edge})
                if support >= min_support and is_canonical(new_subgraph):
                    Qc.append((support, new_subgraph))
                    Qk.append((support, new_subgraph))
                    Qk=sorted(Qk,key=lambda x: x[0])
                    if len(Qk) >= k:
                        min_support = Qk[0][0]  # Update minsup to the smallest support in Qk
                        if len(Qk) > k:
                              # Sort Qk by support in ascending order
                            Qk.pop(0)  # Remove the subgraph with the least support if Qk exceeds size k
    # Return top-k subgraphs with their support
    top_k_results = [(list(subgraph), support) for support, subgraph in Qk]
    

    return top_k_results