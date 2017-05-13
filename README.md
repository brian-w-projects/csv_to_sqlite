<h1>CSV TO SQL</h1>
<h2>Brian W Projects</h2>

<pre>
This small program will parse through a .csv file and easily convert it to a SQLite file for further easy querying.

Usage:
csv_to_sqlite.py [-h] [-i] [-t TABLE_NAME] [-d DATABASE] filename

Convert CSV file to SQLITE table

positional arguments:
  filename       Set .csv file to read from.

optional arguments:
  -h, --help     show this help message and exit
  -i             Set flag to identify Column types otherwise program will
                 attempt to determine automatically.
  -t TABLE_NAME  Set table name. Default is data.
  -d DATABASE    Set existing database to add table to. Default creates new
                 database named data.db
</pre>