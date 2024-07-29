from model.connectionDatabase import connectDatabase 


def getTransactionsBridge():
    try:
        cursor,connection=connectDatabase()        
        cursor.execute("SELECT * FROM TransactionBridge")

        transactions = cursor.fetchall()

        cursor.close()
        connection.close()
        return transactions
    except Exception as e:
        print("Connection to SQL Server failed. Error: ", e)
        return []
def getAllItemBridge():
    try:
        cursor,connection=connectDatabase()        
        cursor.execute("SELECT ProductName FROM TransactionBridge INNER JOIN Product ON TransactionBridge.ProductID = Product.ProductID")

        transactions = cursor.fetchall()

        cursor.close()
        connection.close()
        return transactions
    except Exception as e:
        print("Connection to SQL Server failed. Error: ", e)
        return []
def getAllItemBridgeWithTransactionID():
    try:
        cursor,connection=connectDatabase()        
        cursor.execute("SELECT TransactionID,ProductName FROM TransactionBridge INNER JOIN Product ON TransactionBridge.ProductID = Product.ProductID")

        transactions = cursor.fetchall()

        cursor.close()
        connection.close()
        return transactions
    except Exception as e:
        print("Connection to SQL Server failed. Error: ", e)
        return []