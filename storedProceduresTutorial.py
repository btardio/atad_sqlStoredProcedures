#!/usr/bin/env python
# coding: utf-8

# In[1]:


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

