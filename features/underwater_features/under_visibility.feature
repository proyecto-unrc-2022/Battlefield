Feature: Visibility

    Background: Game with two players
        Given there exist some users and they are logged in:
            |username   |password   |email              |
            |player1    |player1    |player1@example.com|
            |player2    |player2    |player2@example.com|
        And there is a game of dimension '10'x'20' with 'player1' and 'player2'
        And the submarine options are the following:
            | name          | id |
            | Saukko        | 0  |
            | Nautilus      | 1  |
            | USS Sturgeon  | 2  |
        
    
    Scenario: Visibility just after placing subs
        Given the submarines are in the following state:
            | submarine | username | health | x_position | y_position | direction |
            |   Saukko  | player1  |   10   |     3      |      7     |     3     |
            |  Nautilus | player2  |   20   |     7      |     12     |     0     |
        And the board is in the following state
            |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 |
            |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |  T |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |  H |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |  H |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |  T |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |  T |    |    |    |    |    |    |    |
        Then the visibility of 'player1' is the following
            |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 |
            |    |    |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |    |    |    |    |
            |    |    |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |    |    |    |    |
            |    |    |  _ |  _ |  _ |  _ | FT3|  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |    |    |    |    |
            |    |    |  _ |  _ |  _ |  _ |  _ | FH3|  _ |  _ |  _ |  _ |  _ |    |    |    |    |    |    |    |
            |    |    |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |    |    |    |    |
            |    |    |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |    |    |    |    |
            |    |    |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |    |    |    |    |
            |    |    |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ | EH0|    |    |    |    |    |    |    |
            |    |    |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ | ET0|    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        And the visibility of 'player2' is the following
            |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 |
            |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |
            |    |    |    |    |    |    |    |    |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |
            |    |    |    |    |    |    |    |    |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |
            |    |    |    |    |    |    |    |    |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |
            |    |    |    |    |    |    |    |    |  _ |  _ |  _ |  _ | FH0|  _ |  _ |  _ |  _ |    |    |    |
            |    |    |    |    |    |    |    |    |  _ |  _ |  _ |  _ | FT0|  _ |  _ |  _ |  _ |    |    |    |
            |    |    |    |    |    |    |    |    |  _ |  _ |  _ |  _ | FT0|  _ |  _ |  _ |  _ |    |    |    |

            
    Scenario: Send radar pulse
        Given the submarines are in the following state:
            | submarine | username | health | x_position | y_position | direction |
            |   Saukko  | player1  |   10   |     3      |      5     |     3     |
            |  Nautilus | player2  |   20   |     7      |     12     |     0     |
        And the board is in the following state
            |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 |
            |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |  T |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    |  H |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |  H |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |  T |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |  T |    |    |    |    |    |    |    |
        Then the visibility of 'player1' is the following
            |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 |
            |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |    |    |    |    |    |    |
            |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |    |    |    |    |    |    |
            |  _ |  _ |  _ |  _ | FT3|  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |    |    |    |    |    |    |
            |  _ |  _ |  _ |  _ |  _ | FH3|  _ |  _ |  _ |  _ |  _ |    |    |    |    |    |    |    |    |    |
            |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |    |    |    |    |    |    |
            |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |    |    |    |    |    |    |
            |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |    |    |    |    |    |    |
            |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |    |    |    |    |    |    |
            |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        When the player 'player1' sends a radar pulse
        And the user 'player2' rotates the submarine with direction '0' and attacks
        Then the visibility of 'player1' is the following
            |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 |
            |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ | rN | rN | rN |    |    |    |    |    |    |
            |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ | rN | rN | rN |    |    |    |    |    |    |
            |  _ |  _ |  _ |  _ | FT3|  _ |  _ |  _ |  _ |  _ |  _ | rN | rN | rN |    |    |    |    |    |    |
            |  _ |  _ |  _ |  _ |  _ | FH3|  _ |  _ |  _ |  _ |  _ | rN | rN | rN |    |    |    |    |    |    |
            |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ | rN | rN | rN |    |    |    |    |    |    |
            |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ | rN | rN | rN |    |    |    |    |    |    |
            |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ | rN | rN | rN |    |    |    |    |    |    |
            |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ | rN | rP | rN |    |    |    |    |    |    |
            |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ | rN | rP | rN |    |    |    |    |    |    |
            | rN | rN | rN | rN | rN | rN | rN | rN | rN | rN | rN | rN | rP | rN |    |    |    |    |    |    |
        And the visibility of 'player2' is the following
            |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 |
            |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    | rP |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
            |    |    |    |    |    | rP |    |    |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |
            |    |    |    |    |    |    |    |    |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |
            |    |    |    |    |    |    |    |    |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |  _ |    |    |    |
            |    |    |    |    |    |    |    |    |  _ |  _ |  _ |  _ | F*0|  _ |  _ |  _ |  _ |    |    |    |
            |    |    |    |    |    |    |    |    |  _ |  _ |  _ |  _ | FH0|  _ |  _ |  _ |  _ |    |    |    |
            |    |    |    |    |    |    |    |    |  _ |  _ |  _ |  _ | FT0|  _ |  _ |  _ |  _ |    |    |    |
            |    |    |    |    |    |    |    |    |  _ |  _ |  _ |  _ | FT0|  _ |  _ |  _ |  _ |    |    |    |
