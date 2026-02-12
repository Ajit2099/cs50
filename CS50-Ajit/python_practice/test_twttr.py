from twttr import shorten

def test_uppercase():
    assert shorten("AJIT") == "JT"
    assert shorten("ARZOO") == "RZ"

def test_lowercase():
    assert shorten("ajit") == "jt"

def test_sentence():
    assert shorten("This is Ajit.")== "Ths s jt."