Feature: Ship Movement

Background: Login a user and initialize the app
    Given I am logged in as "user1"
    And another user exists as "user2"
    And the app is initialized
    And the game is started

Scenario: Move without collision
    Given The user '1' has a ship 'Destroyer' in '5','5' with course 'N' and hp '60'
    When The ship id '1' moves '3' positions
    Then I should see the ship at the position '2','5' 

Scenario: Ship collides with a ship and is destroyed
    Given The user '1' has a ship 'Destroyer' in '5','5' with course 'N' and hp '60'
    And The user '2' has a ship 'Cruiser' in '4','5' with course 'W' and hp '100'
    When The ship id '1' moves '3' positions
    Then The ship with id '1' should be destroyed
    And The ship with id '2' should have '40' hp

Scenario: Ship collides with a ship and decrease its hp
    Given The user '1' has a ship 'Cruiser' in '5','5' with course 'N' and hp '100'
    And The user '2' has a ship 'Destroyer' in '4','5' with course 'W' and hp '60'
    When The ship id '1' moves '3' positions
    Then The ship with id '1' should have '40' hp
    And I should see the ship at the position '2','5'
    And The ship with id '2' should be destroyed

Scenario: Ship collides with a missile and decreases its hp
    Given The user '1' has a ship 'Destroyer' in '5','5' with course 'N' and hp '60'
    And There is a missile at '4','5' with speed '2', course 'E' and damage '50'
    When The ship id '1' moves '3' positions
    Then The ship with id '1' should have '10' hp

Scenario: Ship collides with a missile and is destroyed
    Given The user '1' has a ship 'Destroyer' in '5','5' with course 'N' and hp '60'
    And There is a missile at '4','5' with speed '2', course 'E' and damage '80'
    When The ship id '1' moves '3' positions
    Then The ship with id '1' should be destroyed
