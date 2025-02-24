import sqlite3
import xml.etree.ElementTree as ET

xml_file = "JMdict_e.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

conn = sqlite3.connect("jmdict.db")
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

    kanji_text = ", ".join(kanji_list) if kanji_list else None
    reading_text = ", ".join(reading_list) if reading_list else None
    meaning_text = "; ".join(meaning_list)

    cursor.execute("INSERT INTO entries (kanji, reading, meaning) VALUES (?, ?, ?)",
                   (kanji_text, reading_text, meaning_text))

conn.commit()
conn.close()
print("Database setup complete")