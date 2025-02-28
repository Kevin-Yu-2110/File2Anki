import sqlite3

def JMdict_query(kanji):
    conn = sqlite3.connect("JMdict/jmdict.db")
    cursor = conn.cursor()
    cursor.execute("SELECT kanji, reading, meaning FROM entries WHERE kanji LIKE (?)", (kanji,)) #TODO: figure out why 嫁入り doesnt work
    results = cursor.fetchone()
    conn.close()
    return results