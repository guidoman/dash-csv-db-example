# dash-csv-db-example
In this example, you store data in a DB as CSV text. Each CSV is identified by its date (unique ID).

Inside a Dash app, you select a date from the dropdown and the plot is updated with data read from the DB. CSV is parsed (and manipulated if needed) using Pandas.

Interaction with the DB is implemented with SqlAlchemy. 
