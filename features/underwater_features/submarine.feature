Feature: Submarine

    Scenario: Create a new game
    Given A user is logged in
    When the user asks for a new underwater game
    Then A new game is registered
    And an empty board with one player is returned