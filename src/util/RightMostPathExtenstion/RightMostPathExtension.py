def calculate_support(subgraph,transactions):
    return sum(1 for transaction in transactions if subgraph.issubset(transaction))
def rightMostPathExtension(subgraph,transactions):
    EdgeExtension=[]
    subgraphList=[]
    transactionList=[]
    for node in subgraph:
        subgraphList.append(node)
    for transaction in transactions:
        transactionList=[]
        for item in transaction:
            transactionList.append(item)
        try:
            start_index = transactionList.index(subgraphList[0])
            # Check if the subsequent elements match the entire subgraph
            if transactionList[start_index:start_index + len(subgraphList)] == subgraphList:
                next_item = transactionList[start_index + len(subgraphList)] if start_index + len(subgraphList) < len(transactionList) else None
                foundNext=False
                
                if(next_item!=None):
                    foundNext = any(item and item.get('Extension') == next_item for item in EdgeExtension)
                else:
                    foundNext=True
                if not foundNext and next_item!=None:
                    newSubgraph=frozenset(subgraph|{next_item})
                    newSupport=calculate_support(newSubgraph,transactions)
                    EdgeExtension.append({"Extension":next_item,"Support":newSupport})
        except ValueError:
            continue  
    return EdgeExtension