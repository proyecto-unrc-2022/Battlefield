from . import air_force

@air_force.route('/attack')
def attack():
    return { 'result': 'booom!!!' }
