from model.connectionDatabase import connectDatabase 

# Khai báo connection string

def getTransactions():
    try:
        cursor,connection=connectDatabase()        
        
        cursor.execute("SELECT * FROM TRANSACTIONS;")

        transactions = cursor.fetchall()

        cursor.close()
        connection.close()
        return transactions
    except Exception as e:
        print("Connection to SQL Server failed. Error: ", e)
        return []