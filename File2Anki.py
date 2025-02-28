import sys
import requests
from modules import parse_file, query_dict
from modules.anki_invoke import anki_connect_invoke
import traceback
    
def main():
    if len(sys.argv) != 3:
        sys.exit("Incorrect number of arguments\n"
                 "usage: (source file path) (deck name)")
    file_path = sys.argv[1]
    deck_name = sys.argv[2]

    try:
        deck_names = anki_connect_invoke('deckNames', 6)
        if deck_name in deck_names:
            print('Deck already exists. Would you like to overwrite (delete corresponding notes) the deck? Y/N') #TODO: add option to add to existing deck
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

        anki_connect_invoke('createDeck', 6, {'deck': deck_name})
        words = parse_file.parse_txt_file(file_path)
        notes = []
        for word in words:
            (kanji, reading, meaning) = query_dict.JMdict_query(word)
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
        traceback.print_exc()

if __name__ == "__main__":
    main()