Feature: Play and start game

  Background: Login a user and initialize the app
    Given I am logged in as "user1"
    And the app has been initialized


  Scenario: Create new Game
    Given I have some ships available
    When I request to create a game
    Then I should get the available ships and the game id
