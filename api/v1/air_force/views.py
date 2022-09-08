from . import air_force
from api import token_auth

@air_force.route('/attack')
@token_auth.login_required
def attack():
    return { 'result': 'booom!!!' }

@air_force.route('/flight')
def fligth():
    return { 'a' : 'a' }

