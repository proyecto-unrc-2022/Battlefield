Feature: Create a navy Ship for a Navy Game.
  
  Background: Login a user and initialize the app
    Given I am logged in as "user1"
    And another user exists as "user2"


  Scenario: Create a valid ship as user 1
    Given I've created a Navy Game
    And another user joins the game I've created
    When I try to create a "Destroyer" ship in ('2', '3') position, and 'N' direction
    Then the ship should be created successfully

  Scenario: Create a valid ship as user 2
    Given another user creates a Navy Game
    And I join the game created by another user
    When I try to create a "Destroyer" ship in ('5', '17') coords, and 'N' direction
    Then the ship should be created successfully

  Scenario: Create a ship with invalid name or course
    Given I've created a Navy Game
    And another user joins the game I've created
    When I try to create ship with wrong name or course
    Then I should get an error

  Scenario: Create a ship with invalid x coord
    Given I've created a Navy Game
    And another user joins the game I've created
    When I try to create ship with ('11', '9') coords
    Then I should get an error

  Scenario: Create a ship with invalid y coord as user 1
    Given I've created a Navy Game
    And another user joins the game I've created
    When I try to create ship with ('2', '16') coords
    Then I should get an error

  Scenario: Create a ship with invalid y coord as user 2
    Given another user creates a Navy Game
    And I join the game created by another user
    When I try to create ship with ('2', '6') coords
    Then I should get an error