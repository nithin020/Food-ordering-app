create database Edyoda;

create table SalesPeople(
Snum int(10) Primary Key,
Snum int(10),
Sname varchar(20) unique Key,
City varchar(20),
Comm int(10)
);

INSERT INTO `edyoda`.`SalesPeople` (`Snum`, `Sname`, `City`, `Comm`) VALUES ('1001', 'Peel.' ,'London', 12);
INSERT INTO `edyoda`.`SalesPeople` (`Snum`, `Sname`, `City`, `Comm`) VALUES ('1002', 'Serres', 'Sanjose', 13);
INSERT INTO `edyoda`.`SalesPeople` (`Snum`, `Sname`, `City`, `Comm`) VALUES ('1004', 'Motika' ,'London', 11);
INSERT INTO `edyoda`.`SalesPeople` (`Snum`, `Sname`, `City`, `Comm`) VALUES ('1007', 'Rifkin' ,'Barcelona', 15);
INSERT INTO `edyoda`.`SalesPeople` (`Snum`, `Sname`, `City`, `Comm`) VALUES ('1003', 'Axelrod' ,'NewYork', 10); 

SELECT * FROM SalesPeople;

CREATE TABLE customers (
    Cnum INT PRIMARY KEY,
    Cname VARCHAR(255),
    City VARCHAR(255) NOT NULL,
    Snum INT,
    FOREIGN KEY (Snum) REFERENCES SalesPeople (Snum)
  );
  
  SELECT * FROM customers;
  CREATE TABLE
  Orders (
    Onum INT PRIMARY KEY,
    Amt DECIMAL,
    Odate DATE,
    Cnum INT,
    Snum INT,
    FOREIGN KEY (Cnum) REFERENCES Customers (Cnum),
    FOREIGN KEY (Snum) REFERENCES SalesPeople (Snum)
  );
  
select * from Orders;

#QUESTION 1
SELECT COUNT(*)
FROM SalesPeople
WHERE Sname LIKE 'A%';

#QUESTION 2
SELECT Snum
FROM orders
GROUP BY Snum
HAVING SUM(Amt) > 2000;

#QUESTION 3
SELECT COUNT(*) AS NumberOfSalespeople
FROM SalesPeople
WHERE City = 'Newyork';

#QUESTION 4
SELECT COUNT(*) AS num_salespeople
FROM SalesPeople
WHERE City IN ('Newyork', 'London');

#QUESTION 5
SELECT Snum,
COUNT(*) AS NumOrders,Odate
FROM Orders
GROUP BY Snum, Odate;









