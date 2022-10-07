from app import db
from app.daos.user_dao import add_user
from app.underwater import boards
from app.underwater.daos.under_game_dao import UnderGameDAO as dao

db.drop_all()
db.create_all()

add_user('a','a','a')
add_user('b','b','b')

game = dao.create(1, visitor_id=2)
game_dao = dao(game)

sub1 = game_dao.add_submarine(1, 0)
sub2 = game_dao.add_submarine(2, 3)

game_dao.place(sub1, 3, 3, 3)
game_dao.place(sub2, 2, 7, 15, 7)

def render_board(m):
    h = len(m)
    w = len(m[0])

    print('-' * (w*4+1))
    for row in m:
        print('|', end='')
        for cell in row:
            if cell:
                print(' 0 |', end='')
            else:
                print('   |', end='')
        print('')
    print('-' * (w*4+1))

render_board(boards[1].matrix)