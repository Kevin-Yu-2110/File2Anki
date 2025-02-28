def parse_txt_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()
    words = text.split() #TODO: requires two reads, one read and one split
    return words