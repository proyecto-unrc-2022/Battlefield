Feature: Play and start game

  #Background: Logged in User

  Scenario: Starting game
    Given the initialized application
    And I have some ships available
    When I request to play a game
    Then I should get the available ships
