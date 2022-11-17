Feature: Create a navy Ship for a Navy Game.
  
  Background: Login a user and initialize the app
    Given a user '1' logged in
    And a user '2' exists

  Scenario: Create a valid ship as user 1
    Given the user '1' creates a NavyGame '1'
    And the user '2' joins the NavyGame '1'
    When the user '1' creates a 'Destroyer' in '2', '3' with course 'N'
    Then the ship should be created successfully

  Scenario: Create a valid ship as user 2
    Given the user '2' creates a NavyGame '1'
    And the user '1' joins the NavyGame '1'
    When the user '1' creates a 'Destroyer' in '5', '17' with course 'N'
    Then the ship should be created successfully

  Scenario: Create a ship with invalid name
    Given the user '1' creates a NavyGame '1'
    And the user '2' joins the NavyGame '1'
    When the user '1' creates a 'Submarine' in '2', '3' with course 'N'
    Then an error should appear

  Scenario: Create a ship with invalid name or course
    Given the user '1' creates a NavyGame '1'
    And the user '2' joins the NavyGame '1'
    When the user '1' creates a 'Destroyer' in '2', '3' with course 'K'
    Then an error should appear 

  Scenario: Create a ship with invalid X coord
    Given the user '1' creates a NavyGame '1'
    And the user '2' joins the NavyGame '1'
    When the user '1' creates a 'Destroyer' in '11', '3' with course 'N'
    Then an error should appear

  Scenario: Create a ship with invalid Y coord as user 1
    Given the user '1' creates a NavyGame '1'
    And the user '2' joins the NavyGame '1'
    When the user '1' creates a 'Destroyer' in '5', '16' with course 'N'
    Then an error should appear

  Scenario: Create a ship with invalid Y coord as user 2
    Given the user '2' creates a NavyGame '1'
    And the user '1' joins the NavyGame '1'
    When the user '1' creates a 'Destroyer' in '5', '3' with course 'N'
    Then an error should appear