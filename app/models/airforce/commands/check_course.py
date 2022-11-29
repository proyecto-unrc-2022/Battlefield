class CheckCourse:
    course: None
    game: None
    player: None

    def __init__(self, course, player, game):
        self.course = course
        self.game = game
        self.player = player

    def execute(self):
        self.game.battlefield.check_course(self.course, self.player)
