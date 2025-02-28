import subprocess
from modules.anki_invoke import anki_connect_invoke

def test_simple():
    anki_connect_invoke('deleteDecks', 6, {'decks': ['testdeck'], 'cardsToo': True})
    exit = subprocess.run(['python3', 'File2Anki.py', 'tests/test_files/basic1.txt', 'testdeck'], capture_output=True)
    assert exit.returncode == 0
    res = anki_connect_invoke('deckNames', 6)
    assert 'testdeck' in res
    res = anki_connect_invoke('findNotes', 6, {'query': 'deck:testdeck'})
    notes = anki_connect_invoke('notesInfo', 6, {'notes': res})
    assert notes[0]['fields']['Front']['value'] == '感じ'
    assert notes[0]['fields']['Back']['value'] == 'Meaning: feeling; sense; impression, Reading: かんじ'
    assert notes[1]['fields']['Front']['value'] == '家'
    assert notes[1]['fields']['Back']['value'] == 'Meaning: house; residence; dwelling; family; household; lineage; family name, Reading: いえ'
    anki_connect_invoke('deleteDecks', 6, {'decks': ['testdeck'], 'cardsToo': True})
