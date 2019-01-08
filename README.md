# Tutorial: Prevent SQL Injection using stored procedures.

In this tutorial we will explain what an SQL Injection attack is and introduce a good development method for preventing creation of code that exposes us to these attacks using stored procedures.

## Requirements

### MySQL

Stored procedures are not available in SQLite, so for this tutorial we will be using MySQL Community. You can download the community version from: <https://dev.mysql.com/downloads/mysql/>

### Anaconda

The Anaconda development environment does include SQL Alchemy. You can download Anaconda at: <https://www.anaconda.com/download/>

### mysqlclient

mysqlclient is required as an interface to connect to the mysql database server from your Anaconda environment. To install, use the Anaconda environment command prompt and type:

```
pip install mysqlclient
```

## SQL Injection

According to Wikipedia:

SQL injection is a code injection technique, used to attack data-driven applications, in which nefarious SQL statements are inserted into an entry field for execution (e.g. to dump the database contents to the attacker).

In the simplest terms, an SQL injection happens whenever a programmer neglects to consider users who provide input that is not expected. Using this input technique an attacker can gain access to a database.

An example of an SQL injection attack is shown:

<https://www.youtube.com/watch?v=sXW7OKda9JM>


## Stored Procedure

According to Wikipedia:

A stored procedure (also termed proc, storp, sproc, StoPro, StoredProc, StoreProc, sp, or SP) is a subroutine available to applications that access a relational database management system (RDBMS). Such procedures are stored in the database data dictionary. 

In simpler terms, a stored procedure is a CRUD (create read update delete) operation that uses the SQL language (or another language such as Perl or PHP). The stored procedure may or may not return a result set. The stored procedure may or may not include arguments. Stored procedures can be used to provide an added abstraction layer to an application, making mistakes during the development process that could lead to SQL injection vulnerabilities less likely. 


## Creating a tutorial table and database:

First create a simple table for demonstration purposes. The table has id, first and last name and favorite whole number columns.


```sql
CREATE DATABASE tutorial;
GRANT ALL ON tutorial.* TO '<ENTER YOUR USERNAME HERE>'@'localhost';
CREATE TABLE tutorial.users (id int, 
                             firstname varchar(255), 
                             lastname varchar(255),
                             favoritewhole int);
``` 

Insert some random rows into the table.

```sql
INSERT INTO tutorial.users VALUES(0, 'John', 'Smith', 10);
INSERT INTO tutorial.users VALUES(1, 'Joe', 'Smith', 20);
INSERT INTO tutorial.users VALUES(2, 'John', 'Deer', 30);
INSERT INTO tutorial.users VALUES(3, 'Joe', 'Deer', 40);
```


## Creating a stored procedure:

```sql
# drop the procedure if it exists
DROP procedure IF EXISTS `tutorial`.`procedure_fetch_favorite`;

# set the delimiter
DELIMITER $$
# create the procedure
CREATE PROCEDURE `tutorial`.`procedure_fetch_favorite`(infirst VARCHAR(255), inlast VARCHAR(255))

BEGIN
  SELECT favoritewhole 
    FROM tutorial.users
    WHERE firstname=infirst AND lastname=inlast;
END$$

DELIMITER ;
```


#### DELIMITER explanation

The delimiter command changes the standard ; delimiter for our stored procedure. We use this so that we can write a procedure that uses the standard ; delimiter without it being interpreted as the end of our procedure. We end our procedure with $$ instead of ; and then we set the delimiter back to the standard delimiter.

#### CREATE PROCEDURE explanation

The create procedure creates the procedure with two arguments, infirst and inlast. It is also possible to have OUT variables. In the example above it would be arguably better to place the favoritewhole into an OUT variable.

### Show the created procedure.

To see the procedure that was created:

```sql
SHOW CREATE PROCEDURE `tutorial`.`procedure_fetch_favorite`;
```

### Call the created procedure.

To call the created procedure using SQL:

```sql
CALL `tutorial`.`procedure_fetch_favorite`('John', 'Smith');
```


## Calling the procedure using Python SQL Alchemy 

```python

from sqlalchemy import create_engine

# Create a database engine, which includes a connection pool
engine = create_engine('mysql://<INSERT YOUR USERNAME>:<INSERT YOUR PASSWORD>@localhost/tutorial')

# Start a raw connection, SQL Alchemy does not provide a higher level connection mechanism.
connection = engine.raw_connection()
try:
    # Retrieve a connection cursor. Read more: 
    # https://en.wikipedia.org/wiki/Cursor_(databases)
    cursor = connection.cursor()
    # Make the actual procedure call, sending it 'Joe' and 'Smith' as arguments
    cursor.callproc("tutorial.procedure_fetch_favorite", ['Joe', 'Smith'])
    # Fetch the results
    results = list(cursor.fetchall())
    cursor.close() # close the cursor
    # commit, make final any database changes, this is not necessary in our example 
    # as we are not making changes to the database but if UPDATE were used this is 
    # an important step
    connection.commit() 
finally:
    connection.close() # close the connection

# print the results
print(results)

# Dispose of the connection pool used by this engine.
engine.dispose()
    
```

## Further Information

A very comprehensive description of stored procedures is available: <https://www.w3resource.com/mysql/mysql-procedure.php>



