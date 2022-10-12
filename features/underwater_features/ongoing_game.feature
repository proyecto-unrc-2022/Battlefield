Feature: Game in ongoing game state

    Background: Game with players
        Given there exist some users and they are logged in:
            |username   |password   |email              |
            |player1    |player1    |player1@example.com|
            |player2    |player2    |player2@example.com|
        And there is a game of dimension '6'x'6' with 'player1' and 'player2'
        And the submarine options are the following:
            | name          | id |
            | Saukko        | 0  |
            | Nautilus      | 1  |
            | USS Sturgeon  | 2  |


    Scenario: Rotate and move submarine
        Given the submarines are in the following state:
            | submarine | username | health | x_position | y_position | direction |
            |   Saukko  | player1  |   10   |     1      |      1     |     3     |
            |  Nautilus | player2  |   20   |     3      |      5     |     0     |
        And the board is in the following state:
            | 0 | 1 | 2 | 3 | 4 | 5 |
            | T |   |   |   |   |   |
            |   | H |   |   |   |   |
            |   |   |   |   |   |   |
            |   |   |   |   |   | H |
            |   |   |   |   |   | T |
            |   |   |   |   |   | T |
        When the user 'player1' rotates the submarine with direction '4' and moves '3' positions
        Then the board is in the following state:
            | 0 | 1 | 2 | 3 | 4 | 5 |
            |   |   |   |   |   |   |
            |   |   |   |   |   |   |
            |   |   |   |   |   |   |
            |   | T |   |   |   | H |
            |   | H |   |   |   | T |
            |   |   |   |   |   | T |
