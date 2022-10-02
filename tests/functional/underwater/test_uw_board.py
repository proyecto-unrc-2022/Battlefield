from app.models.underwater.under_models import UnderBoard


def test_place_submarine(flask_app):
    b = UnderBoard(-1, 5, 10)
    b.place("Su", 3, 3, 5, 4)
    expected = [
        [None, None, None, None, None, None, "Su", None, None, None],
        [None, None, None, None, None, "Su", None, None, None, None],
        [None, None, None, None, "Su", None, None, None, None, None],
        [None, None, None, "Su", None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
    ]
    assert b.matrix == expected
