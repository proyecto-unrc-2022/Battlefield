Feature: Initialize a game

    Background: Two players are logged in
    Given there exist some users and they are logged in:
        |username   |password   |email              |
        |player1    |player1    |player1@example.com|
        |player2    |player2    |player2@example.com|

    
    Scenario: Create a new game
        When the user 'player1' asks for a new game
        Then a new game with host 'player1' is registered
        And a game with an empty board is returned
        
    Scenario: Player of a game tries to create another
        Given the user 'player1' is in a game
        When the user 'player1' asks for a new game
        Then the system informs failure