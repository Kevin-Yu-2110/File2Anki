import subprocess
from modules.anki_invoke import anki_connect_invoke

def test_simple(): #TODO; setup automatic delete deck after test
    anki_connect_invoke('deleteDecks', {'decks': ['testdeck'], 'cardsToo': True})
    exit = subprocess.run(['python3', 'File2Anki.py', 'tests/test_files/basic1.txt', 'testdeck'], capture_output=True)
    assert exit.returncode == 0
    res = anki_connect_invoke('deckNames')
    assert 'testdeck' in res
    res = anki_connect_invoke('findNotes', {'query': 'deck:testdeck'})
    notes = anki_connect_invoke('notesInfo', {'notes': res})
    notes.sort(key=lambda x: x['fields']['Front']['value'])
    assert notes[1]['fields']['Front']['value'] == '感じ'
    assert notes[1]['fields']['Back']['value'] == 'Meaning: feeling; sense; impression, Reading: かんじ'
    assert notes[0]['fields']['Front']['value'] == '家'
    assert notes[0]['fields']['Back']['value'] == 'Meaning: house; residence; dwelling; family; household; lineage; family name, Reading: いえ'
    assert notes[2]['fields']['Front']['value'] == '食べる'
    assert notes[2]['fields']['Back']['value'] == 'Meaning: to eat; to live on (e.g. a salary); to live off; to subsist on, Reading: たべる'
    anki_connect_invoke('deleteDecks', {'decks': ['testdeck'], 'cardsToo': True})

def test_epub_simple(): #pretty bad test, just tests number of notes, also fails if one of the notes already exists in another deck
    anki_connect_invoke('deleteDecks', {'decks': ['testdeck'], 'cardsToo': True})
    exit = subprocess.run(['python3', 'File2Anki.py', 'tests/test_files/sample_japanese.epub', 'testdeck'], capture_output=True)
    assert exit.returncode == 0
    res = anki_connect_invoke('deckNames')
    assert 'testdeck' in res
    res = anki_connect_invoke('findNotes', {'query': 'deck:testdeck'})
    notes = anki_connect_invoke('notesInfo', {'notes': res})
    assert len(notes) == 25
    anki_connect_invoke('deleteDecks', {'decks': ['testdeck'], 'cardsToo': True})