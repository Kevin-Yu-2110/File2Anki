import pytest
from modules.parse_file import *

def test_basic1_txt_file():
    assert(parse_txt_file('tests/test_files/basic1.txt')) == ['感じ', '家']




