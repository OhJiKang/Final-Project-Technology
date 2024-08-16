import csv

csv_file_path = "Mini_Retail_Transaction_Dataset.csv"

product_id_map = {
    'Mustard': 1,
    'Bread': 2,
    'Olive Oil': 3,
    'Tissues': 4,
    'Ketchup': 5,
    'Ice Cream': 6,
    'Light Bulb': 7,
    'Spinach': 8,
    'Dish Soap': 9,
    'Milk': 10,
    'Shaving Cream': 11
}

with open(csv_file_path, mode="r", encoding="utf-8") as file:
    csv_reader = csv.DictReader(file)

    account_queries = []
    transaction_queries = []
    transaction_bridge_queries = []

    transaction_id_counter = 1

    for row in csv_reader:
        customer_name = row['Customer_Name']
        products = row['Product'].split(", ")

        account_query = f"INSERT INTO Account (Username) VALUES ('{customer_name}');"
        account_queries.append(account_query)
        
        account_id = csv_reader.line_num - 1

        transaction_query = f"INSERT INTO Transactions (AccountID) VALUES ({account_id});"
        transaction_queries.append(transaction_query)

        for product_name in products:
            if product_name:
                product_id = product_id_map.get(product_name)
                if product_id:
                    transaction_bridge_query = f"INSERT INTO TransactionBridge (TransactionID, ProductID) VALUES ({transaction_id_counter}, {product_id});"
                    transaction_bridge_queries.append(transaction_bridge_query)

        transaction_id_counter += 1

with open("account_queries.sql", mode="w", encoding="utf-8") as file:
    file.write("-- Insert into Account table\n")
    for query in account_queries:
        file.write(query + "\n")

with open("transaction_queries.sql", mode="w", encoding="utf-8") as file:
    file.write("-- Insert into Transactions table\n")
    for query in transaction_queries:
        file.write(query + "\n")

with open("transaction_bridge_queries.sql", mode="w", encoding="utf-8") as file:
    file.write("-- Insert into TransactionBridge table\n")
    for query in transaction_bridge_queries:
        file.write(query + "\n")