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


    Scenario: Everyone moves
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
        Then the system informs success
        When the user 'player2' rotates the submarine with direction '7' and attacks
        Then the system informs success
        And the board is in the following state:
            | 0 | 1 | 2 | 3 | 4 | 5 |
            |   |   |   |   |   |   |
            |   |   |   |   |   |   |
            |   |   |   |   | * |   |
            |   | T |   |   |   | H |
            |   | H |   |   |   |   |
            |   |   |   |   |   |   |


    Scenario: three rounds
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
        Then the system informs success
        When the user 'player2' rotates the submarine with direction '7' and attacks
        Then the system informs success
            # | 0 | 1 | 2 | 3 | 4 | 5 |
            # |   |   |   |   |   |   |
            # |   |   |   |   |   |   |
            # |   |   |   |   | * |   |
            # |   | T |   |   |   | H |
            # |   | H |   |   |   |   |
            # |   |   |   |   |   |   |
        When the user 'player2' rotates the submarine with direction '4' and moves '2' positions
        Then the system informs success
        When the user 'player1' rotates the submarine with direction '2' and attacks
        Then the system informs success
            # | 0 | 1 | 2 | 3 | 4 | 5 |
            # |   |   |   |   |   |   |
            # |   |   |   |   |   |   |
            # |   |   |   |   |   |   |  #notar que el torpedo anterior avanzo y se chocó la pared
            # |   |   |   |   |   | T |
            # | T | H | * |   |   | T |
            # |   |   |   |   |   | H |
        When the user 'player1' rotates the submarine with direction '0' and moves '2' positions
        Then the system informs success
        When the user 'player2' rotates the submarine with direction '6' and moves '0' positions
        Then the system informs success
        And the board is in the following state:
            | 0 | 1 | 2 | 3 | 4 | 5 |
            |   |   |   |   |   |   |
            |   |   |   |   |   |   |
            |   | H |   |   |   |   |
            |   | T |   |   |   |   |
            |   |   |   |   |   |   |
            |   |   |   |   |   | H |


    Scenario: Not his turn
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
        Then the system informs success
        When the user 'player2' rotates the submarine with direction '7' and attacks
        Then the system informs success
        When the user 'player1' rotates the submarine with direction '4' and moves '2' positions
        Then the system informs failure with code '409' 


    Scenario: Rotate 180 degrees
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
        When the user 'player1' rotates the submarine with direction '7' and moves '1' positions
        Then the system informs failure with code '409'
