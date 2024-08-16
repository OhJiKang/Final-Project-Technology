from model.products import getProducts
from model.transactions import getTransactions
from model.transactionBridge import getAllItemBridge,getTransactionsBridge,getAllItemBridgeWithTransactionID

def getUniqueItemsFromDatabase():
    TransactionsBridge=getAllItemBridge()
    ItemUnique=list({item[0].strip().lower() for item in TransactionsBridge})
    return ItemUnique
def executeTransaction():
    transactions=getTransactions()
    transactionsBridge=getAllItemBridgeWithTransactionID()
    productListAll=[]
    for TransactionID, AccountID in transactions:
        productListTransaction=[]
        for TransactionID_BridgeTable, Product_BridgeTable in transactionsBridge:
            if(TransactionID==TransactionID_BridgeTable):
                productListTransaction.append(Product_BridgeTable.strip().lower())
        productListAll.append(productListTransaction)
    productList = [frozenset(items) for items in productListAll]
    return productList