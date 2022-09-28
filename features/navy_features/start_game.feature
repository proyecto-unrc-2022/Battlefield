Feature: Create and start game

  Background: Login a user and initialize the app
    Given I am logged in as "user1"
    And the app has been initialized


  Scenario: Create new Game
    Given I have some ships available
    When I request to create a game
    Then I should get the available ships and the game id


  Scenario: Start a Game
    Given I have a game created
    And I have ships to choose
    When I choose a 'Destroyer' ship in ('2', '3') position, and 'N' direction
    Then I should see the game board, with the ship located in ('2', '3') and directed to 'N'