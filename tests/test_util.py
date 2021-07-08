from src.util import metaphone


def test_metaphone():
    assert metaphone('Nick') == 'NK'
