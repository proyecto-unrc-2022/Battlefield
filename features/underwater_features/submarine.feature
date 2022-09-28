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
