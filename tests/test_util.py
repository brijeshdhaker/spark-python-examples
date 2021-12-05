from src.utils.util import metaphone


def test_metaphone():
    assert metaphone('Nick') == 'NK'
