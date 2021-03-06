import os
from urllib.parse import urlparse
import json

from flask import Flask
from flask import render_template
from flask import request

import psycopg2

app         = Flask(__name__)
port        = int(os.getenv('PORT', 80))
db_port     = int(os.getenv('DB_PORT', 5432))
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_name     = os.getenv('DB_NAME')
db_host     = os.getenv('DB_HOST')

conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    user=db_username,
    password=db_password,
    database=db_name)

@app.route('/')
# top-level page display, creates table if it doesn't exist
def serve_page():
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS words (
		id serial primary key,
		word varchar(256) NOT NULL,
		definition varchar(256) NOT NULL) """)
    return render_template('index.html')


@app.route('/words', methods=['PUT'])
# triggers on hitting the 'Add' button; inserts word/definition into table
def handle_words():
    cur = conn.cursor()
    
    cur.execute("""INSERT INTO words (word, definition)
        VALUES (%s, %s)""", (request.form['word'], request.form['definition']))
    conn.commit()
    
    return ('', 204)


@app.route('/words', methods=['GET'])
# queries and formats results for display on page
def display_select():
    cur = conn.cursor()
    
    # SQL query for all the rows in the table, stores rows in an object
    cur.execute("""SELECT word, definition FROM words""")
    cursor_obj = cur.fetchall()
    
    # grabs column names from the table
    labels = [column[0] for column in cur.description]
    
    # makes a list from the dict of the zip of column names and the results object
    results_list = []
    for row in cursor_obj:
        results_list.append(dict(zip(labels, row)))
    
    # makes json from the list for display on the page
    return json.dumps(results_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)