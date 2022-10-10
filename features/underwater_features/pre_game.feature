Feature: Game in pre game state

    Background: Game with players
        Given there exist some users and they are logged in:
            |username   |password   |email              |
            |player1    |player1    |player1@example.com|
            |player2    |player2    |player2@example.com|
        And there is a game of id '1' with 'player1' and 'player2'
        And the submarine options are the following:
            | name          | id |
            | Saukko        | 0  |
            | Nautilus      | 1  |
            | USS Sturgeon  | 2  |

    Scenario: Choose a submarine
        When the player asks for the submarine options
        And the player 'player1' chooses 'Saukko' as his submarine with position '4','5' and direction '3'
        Then the system informs success
