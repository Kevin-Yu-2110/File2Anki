import sqlite3

def test_query():
    conn = sqlite3.connect("JMdict/jmdict.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries WHERE kanji = '食べる'")
    res = cursor.fetchall()
    print(res)
    assert res[0][1] == '食べる'