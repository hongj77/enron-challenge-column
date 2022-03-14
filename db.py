import sqlite3

def set_up_db():
    conn = sqlite3.connect('enron.db')
    print ("Opened database successfully")
    conn.execute("CREATE TABLE IF NOT EXISTS word (\
	    wordId TEXT PRIMARY KEY )")
    conn.execute("CREATE TABLE IF NOT EXISTS document (\
	    docId TEXT PRIMARY KEY \
        )")
    conn.commit()
    # TODO: add foreign key constraint.
    conn.execute("CREATE TABLE IF NOT EXISTS wordToDoc(\
        relationId TEXT PRIMARY KEY, \
	    wordId TEXT, \
	    docId TEXT \
        )")
    return conn

def save_doc_id(conn, doc_id):
    conn.execute("INSERT OR IGNORE INTO document VALUES (?)", (doc_id,))
    conn.commit()

def save_word(conn, word):
    conn.execute("INSERT OR IGNORE INTO word VALUES (?)", (word,))
    conn.commit()

def save_word_doc_relation(conn, relation_id, word, doc_id):
    conn.execute("INSERT OR IGNORE INTO wordToDoc VALUES (?, ?, ?)", (relation_id, word, doc_id))
    conn.commit()
