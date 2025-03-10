import sqlite3
import xml.etree.ElementTree as ET

xml_file = "JMdict/JMdict_e.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

conn = sqlite3.connect("JMdict/jmdict.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kanji TEXT,
    reading TEXT,
    meaning TEXT
)
""")


for entry in root.findall("entry"):
    kanji_list = [k.text for k in entry.findall("k_ele/keb")]
    reading_list = [r.text for r in entry.findall("r_ele/reb")]
    meaning_list = [s.text for s in entry.findall("sense/gloss")]

    reading_text = ", ".join(reading_list)
    meaning_text = "; ".join(meaning_list)

    for kanji in kanji_list: #TODO: could add field for alternate kanji
        cursor.execute("INSERT INTO entries (kanji, reading, meaning) VALUES (?, ?, ?)",
                   (kanji, reading_text, meaning_text))
conn.commit()
conn.close()
print("Database setup complete")