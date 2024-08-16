from model.connectionDatabase import connectDatabase 


def getProducts():
    try:
        cursor,connection=connectDatabase()        
        cursor.execute("SELECT * FROM PRODUCT;")

        products = cursor.fetchall()

        cursor.close()
        connection.close()
        return products
    except Exception as e:
        print("Connection to SQL Server failed. Error: ", e)
        return []