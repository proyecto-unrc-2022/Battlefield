from flask import url_for


def test_attack_is_done(flask_app):
    # response = flask_app.get('/api/v1/air_force/attack')
    response = flask_app.get(url_for("air_force.attack"))

    assert response.status_code == 200
    assert 'booom' in response.text
