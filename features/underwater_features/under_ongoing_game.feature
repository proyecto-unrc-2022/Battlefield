Feature: Ongoing Under Game
    Background: We have an ongoing game
        Given there exists two users and they are logged in:
            |username   |password   |email              |
            |player1    |player1    |player1@example.com|
            |player2    |player2    |player2@example.com| 
        Given the user 'player1' is in a game of dimension '6'x'6' with visitor
        And the user 'player1' chose 'Saukko' submarine
        And the user 'player2' chose 'Nautilus' submarine

        #     Scenario: Rotate and move submarine
        #         Given the user 'player1' chooses the position '{x:d}','{y:d}' and direction '{d:d}'
        #         When the user 'player1' rotates the submarine with direction '3'
        #         And the user 'player1' moves the submarine '2' positions
        #         Then the board is in the following state:
        #             | 0 | 1 | 2 | 3 | 4 | 5 |
        #             | H |   |   |   |   |   |
        #             |   | T |   |   |   |   |
        #             |   |   |   |   |   |   |
        #             |   |   |   |   |   |   |
        #             |   |   |   |   |   |   |
        #             |   |   |   |   |   |   |
