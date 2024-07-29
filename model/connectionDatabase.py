import pyodbc # Thư viện kết nối SQL Server
def connectDatabase():
    connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=tcp:graphmining.database.windows.net,1433;'
    'DATABASE=GraphMining; Uid=GraphMining; PWD=admin123!;')
    connection = pyodbc.connect(connection_string)
    cursor=connection.cursor()
    return cursor,connection