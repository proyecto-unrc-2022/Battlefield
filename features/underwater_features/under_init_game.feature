Feature: Initialize a game

    Background: Some players are logged in
    Given there exist some users and they are logged in:
        |username   |password   |email              |
        |player1    |player1    |player1@example.com|
        |player2    |player2    |player2@example.com|
        |player3    |player3    |player3@example.com|
    
    Scenario: Create a new game
        When the user 'player1' asks for a new game
        Then the system informs success
        # Then a new game with host 'player1' is registered
        # And a game with an empty board is returned
        
    Scenario: Player of a game tries to create another
        Given the user 'player1' is in a game of id '1'
        When the user 'player1' asks for a new game
        Then the system informs failure with code '409'

    Scenario: Join a game
        Given the user 'player1' is in a game of id '1'
        When the user 'player2' asks to join the game of id '1'
        Then the system informs success
        # And a game with 'player1' is returned
        # And a game with 'player2' is returned

    Scenario: Join a game of my own
        Given the user 'player1' is in a game of id '1'
        When the user 'player1' asks to join the game of id '1'
        Then the system informs failure with code '409'

    Scenario: Join a game without slots
        Given the user 'player1' is in a game of id '1'
        When the user 'player2' asks to join the game of id '1'
        And the user 'player3' asks to join the game of id '1'
        Then the system informs failure with code '409'
