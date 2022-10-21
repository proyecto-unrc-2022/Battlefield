Feature: Ship Movement

Background: Login a user and initialize the app
    Given I am logged in as "user1"
    And the app is initialized
    And the game is started

Scenario: Move without collision
    Given I have a ship 'Destroyer' in '5','5' with course 'N' and hp '100'
    When The ship moves '3' positions
    Then I should see the ship at the new position '2','5' 