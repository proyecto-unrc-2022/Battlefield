Feature: Submarine

    Scenario: Create a new game
        Given A user is logged in
        When the user asks for a new underwater game
        Then A new game is registered
        And an empty board with one player is returned

    Scenario: Get the submarine options
        Given the system is running
        When I receive a request to show the submarine options
        Then the options are returned

    Scenario: Join a game
        Given the user 'player' is logged in
        And there is a game with available slots
        When the user 'player' joins that game
        Then the game is modified
