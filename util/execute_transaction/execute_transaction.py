import pandas as pd

def transform_transaction(file_path):
    df = pd.read_csv(file_path, usecols=['Product'])
    transactions = df['Product'].apply(lambda products: frozenset(product.strip().lower() for product in products.split(','))).tolist()
    return transactions
def get_all_unique_item_from_transaction(file_path):
    df = pd.read_csv(file_path, usecols=['Product'])
    transactions = df['Product'].apply(lambda products: frozenset(product.strip() for product in products.split(','))).tolist()
    unique_items = set(item for transaction in transactions for item in transaction)

    return unique_items
