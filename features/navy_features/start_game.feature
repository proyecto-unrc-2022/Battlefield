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
  
  Scenario: Game doesn't exist
    Given I have ships to choose
    When I try to start a game which doesn't exist
    Then I should get an error message about the game

  Scenario: Incorrect game
    Given I have ships to choose
    When I try to start a game with an incorrect data type in game_id field
    Then I should get an error message about the game

  Scenario: Incorrect User
    Given I have a game created
    And I have ships to choose
    When I try to start a game with an incorrect data type in id_user field
    Then I should get an error message about the user

  Scenario: User doesn't exist
    Given I have a game created
    And I have ships to choose
    When I try to start a game with an user who doesn't exist
    Then I should get an error message about the user

  Scenario: Incorrect Direction
    Given I have a game created
    And I have ships to choose
    When I try to start a game with an incorrect direction
    Then I should get an error message about the direction

  Scenario: Incorrect Ship Type
    Given I have a game created
    And I have ships to choose
    When I try to start a game with an incorrect ship type
    Then I should get an error message about the ship type

  Scenario: Position Out of range in X
    Given I have a game created
    And I have ships to choose
    When I try to start a game with a position out of range in x
    Then I should get an error message about the position in x 

  Scenario: Position Out of range in Y
    Given I have a game created
    And I have ships to choose
    When I try to start a game with a position out of range in y
    Then I should get an error message about the position in y