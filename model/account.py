from model.connectionDatabase import connectDatabase 

def getAccounts():
    try:
        cursor,connection=connectDatabase()        
        
        cursor.execute("SELECT * FROM Account;")

        accounts = cursor.fetchall()

        cursor.close()
        connection.close()
        return accounts
    except Exception as e:
        print("Connection to SQL Server failed. Error: ", e)
        return []