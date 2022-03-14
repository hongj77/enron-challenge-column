# Modified version of https://www.geeksforgeeks.org/auto-complete-feature-using-trie/

import db 
import sys

class TrieNode():
    def __init__(self):
        self.children = {} # char -> node
        self.last = False

class Trie():
    def __init__(self):
        self.root = TrieNode()
 
    def formTrie(self, keys):
        for key in keys:
            self.insert(key)  # inserting one key to the trie.
 
    def insert(self, key):
        node = self.root
 
        for a in key:
            if not node.children.get(a):
                node.children[a] = TrieNode()
 
            node = node.children[a]
 
        node.last = True
 
    def suggestionsRec(self, node, word, res):
        if node.last:
            res.append(word)
        for a, n in node.children.items():
            self.suggestionsRec(n, word + a, res)
 
    def returnSuggestions(self, key):
        node = self.root
        res = []
        for a in key:
            if not node.children.get(a):
                return res
            node = node.children[a]
        if not node.children:
            return res
        self.suggestionsRec(node, key, res)
        return res
 
def initialize_trie(conn):
    rows = conn.execute("SELECT wordId FROM word").fetchall()   
    keys = []
    for word in rows:
        keys.append(word[0])
    t = Trie()
    t.formTrie(keys)
    return t

def find_docs(conn, words):
    res = []
    sql="select docId from wordToDoc where wordId in ({seq})".format(seq=','.join(['?']*len(words)))
    rows = conn.execute(sql, words).fetchall()   
    for row in rows:
        res.append(row[0])
    return res
 
if __name__=="__main__":
    if len(sys.argv) < 2:
        print("Give the search term for the first argument.")
        sys.exit()
    try:
        conn = db.set_up_db()
    except Exception as e:
        print("Error initializing DB")
        print(e)
    t = initialize_trie(conn)
    res = t.returnSuggestions(sys.argv[1])
    print("----------------------matched words-----------------------------")
    print(res)
    
    print("----------------------documents-----------------------------")

    docs = find_docs(conn, res)
    print(docs)

 