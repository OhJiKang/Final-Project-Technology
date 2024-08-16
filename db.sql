CREATE TABLE Account (
    AccountID INT PRIMARY KEY IDENTITY(1,1),
    Username NVARCHAR(255) NOT NULL
);
Create Table Product(
    ProductID INT PRIMARY KEY IDENTITY(1,1),
    ProductName NVARCHAR(255) NOT NULL
);
Create Table Transactions(
	TransactionID int identity(1,1) PRIMARY KEY,
	AccountID int FOREIGN KEY REFERENCES Account(AccountID)
);
Create Table TransactionBridge(
	TransactionID int FOREIGN KEY REFERENCES Transactions(TransactionID),
	ProductID int FOREIGN KEY REFERENCES PRODUCT(ProductID)
);
