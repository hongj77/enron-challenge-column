import os
import sqlite3
import pdb
import sys, getopt

def format_message_id(line):
    line = line.replace("Message-ID:", "")
    line = line.replace("<", "")
    line = line.replace(">", "")
    line = line.strip()
    return line

def format_word(word):
    word = word.strip()
    word = word.replace(".", "")
    word = word.replace(",", "")
    word = word.replace(")", "")
    word = word.replace("(", "")
    word = word.replace("!", "")
    word = word.replace(";", "")
    return word

def is_invalid_word(word):
    if word == '\n':
        return True
    if word == '':
        return True
    if not word:
        return True
    # pdb.set_trace()
    return False

def save_doc_id(conn, doc_id):
    conn.execute("INSERT OR IGNORE INTO document VALUES (?)", (doc_id,))
    conn.commit()

def save_word(conn, word):
    conn.execute("INSERT OR IGNORE INTO word VALUES (?)", (word,))
    conn.commit()

def save_word_doc_relation(conn, relation_id, word, doc_id):
    conn.execute("INSERT OR IGNORE INTO wordToDoc VALUES (?, ?, ?)", (relation_id, word, doc_id))
    conn.commit()

def process_body_line(conn, line, doc_id):
    for word in line.split(" "):
        word = format_word(word)
        if is_invalid_word(word):
            continue
        relation_id = word+"_"+doc_id
        save_word_doc_relation(conn, relation_id, word, doc_id)
        save_word(conn, word)
    
def parse_file(conn, path):
    """
    Opens file in path and creates reverse index for every word
    path - path to a single email file
    """
    # Skip to body of email. For each word, associate word -> doc_id.
    email_body = False
    with open(path, encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('Message-ID'):
                doc_id = format_message_id(line)
                save_doc_id(conn, doc_id)
            if line.startswith('X-FileName'):
                email_body = True
                continue
            if not email_body:
                continue
            process_body_line(conn, line, doc_id)

def parse_files(conn, path):
    for root, subdirs, files in os.walk(path):
        for file in os.listdir(root):
            filePath = os.path.join(root, file)
            if os.path.isdir(filePath):
                pass
            else:
                if not filePath.endswith('.'):
                    continue
                print("starting file: ", filePath)
                parse_file(conn, filePath)
                print("finishing file: ", filePath)

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

if __name__=="__main__":
    if len(sys.argv) < 2:
        print("Give the data path for the first argument.")
        sys.exit()
    filepath = sys.argv[1]
    try:
        conn = set_up_db()
    except Exception as e:
        print("Error initializing DB")
        print(e)
        
    parse_files(conn, filepath)