import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import MeCab #TODO: mecab currently uses unidic-lite, which is smaller but less detailed than unidic, can add modular option in config.ini

#currently returns a set, i.e. unordered. This is fine for the current use case, but may want to change to a list if we want to implement frequency ordering

def parse_file(path):
    if path.endswith('.txt'):
        return parse_txt_file(path)
    elif path.endswith('.epub'):
        return parse_epub(path)
    else:
        raise ValueError("File type not supported")
    
def parse_line(line, tagger: MeCab.Tagger) -> list:  #pass in tagger to avoid tagger initialisation overhead
    lemmas = set()
    words = tagger.parse(line).split('\n')
    for word in words:
        if word == 'EOS':
            break
        word = word.split('\t')
        lemma = word[3]
        lemmas.add(lemma)
    return lemmas

def parse_txt_file(path): #TODO: could probably be optimised
    words = set()
    tagger = MeCab.Tagger()
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            words = words.union(parse_line(line, tagger)) #TODO: currently unions the sets for every line - 
                                                          #could be terrible idk alternative is to pass in a set and add each word
    return words

#TODO: only parses main body - title, author and other metatext is ignored
def parse_epub(path):
    book = epub.read_epub(path)
    words = set()
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT: #seems like metadata (title and table of contents) is last item in list
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            tagger = MeCab.Tagger()
            for line in soup.get_text().split():
                words = words.union(parse_line(line, tagger))
    print(words)
    return words      