from modules.parse_file import *

def test_basic1_txt_file():
    assert(parse_file('tests/test_files/basic1.txt')) == {'感じ', '家', '食べる', 'ます'} #TODO: figure out the morphene situation

def test_basic_epub():
    assert(parse_file('sample_input/epub/sample_japanese.epub')) == {
        '森', '一', '昔々', '小さな', '物語', '見付ける', 'て', '光る', '、',
        '言う', '木の実', '日', '集める', '石', '不思議', 'と', '或る', 'た',
        '魚', '毎日', 'だ', '住む', 'で', '…', '少年', 'が', 'を', '居る', '彼',
        '捕まえる', '第', 'に', '川', 'は', '章', '。', 'タロウ', '村', 'ます'
    } #this is lowkey a fake test cos i just copied the output and set it as expected, im just assuming the output is correct