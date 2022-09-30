Feature: Submarine

    Scenario: Create a new game
        Given the user 'user' is logged in
        When the user asks for a new underwater game
        Then A new game is registered
        And an empty board with one player is returned

    Scenario: Join a game
        Given the user 'visitor' is logged in
        And there is a game with available slots
        When the user 'visitor' joins that game
        Then the game now has the new visitor

    Scenario: Get the submarine options
        Given the system is running
        When I receive a request to show the submarine options
        Then the options are returned

    Scenario: Choose a submarine
        Given the user 'player' is logged in
        And the user is in an ongoing game
        When the user chooses a submarine
        Then the game bounds the user to the choosen submarine
