import sys
import requests
import sqlite3

def anki_connect_invoke(action, version, params={}):
    url = 'http://127.0.0.1:8765'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'action': action,
        'version': version,
        'params': params
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            if 'error' in response_data and response_data['error'] is not None:
                raise Exception(response_data['error'])
            if 'result' in response_data:
                return response_data['result']
            else:
                raise Exception('failed to get result from AnkiConnect')
        else:
            raise Exception('failed to connect to AnkiConnect')
    except Exception as e:
        raise Exception(f"Error: {e}")
    
def parse_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()
    words = text.split() #TODO: requires two reads, one read and one split
    return words

def JMdict_query(kanji):
    conn = sqlite3.connect("JMdict/jmdict.db")
    cursor = conn.cursor()
    cursor.execute("SELECT kanji, reading, meaning FROM entries WHERE kanji LIKE (?)", (kanji,)) #TODO: figure out why 嫁入り doesnt work
    results = cursor.fetchone()
    conn.close()
    return results
    
def main():
    if len(sys.argv) != 3:
        sys.exit("Incorrect number of arguments\n"
                 "usage: (source file path) (deck name)")
    file_path = sys.argv[1]
    deck_name = sys.argv[2]

    try:
        #TODO: if deck already exists, ask user to either if they want to overwrite
        nothing = "nothing"
        deck_names = anki_connect_invoke('deckNames', 6)
        if deck_name in deck_names:
            print('Deck already exists. Would you like to overwrite the deck? Y/N') #TODO: add option to add to existing deck
            while True:
                user_input = input()
                if user_input == "Y":
                    anki_connect_invoke('deleteDecks', 6, {'decks': [deck_name],
                                                           'cardsToo': True})
                    break
                elif user_input == "N":
                    sys.exit("program terminated")
                else:
                    print('Please enter (Y) or (N)')

        anki_connect_invoke('changeDeck', 6, {'cards': [], 'deck': deck_name})
        words = parse_file(file_path)
        notes = []
        for word in words:
            (kanji, reading, meaning) = JMdict_query(word)
            notes.append({
                'deckName': deck_name,
                'modelName': 'Basic',
                'fields': {
                    'Front': kanji,
                    'Back': f"Meaning: {meaning}, Reading: {reading}"
                },
            })
            print('current word:', kanji, reading, meaning)
        anki_connect_invoke('addNotes', 6, {'notes': notes})
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()