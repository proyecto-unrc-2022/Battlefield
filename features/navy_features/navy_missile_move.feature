Feature: Move a missile

    Background: Login a user and initialized app with a game
        Given a user '1' logged in
        And a user '2' exists
        And the app is initialized
        And the game started

    Scenario: Move to a valid position
        Given The user '1' has a ship 'Destroyer' in '2','2' with course 'N' and hp '100'
        And The user '2' has a ship 'Destroyer' in '2','11' with course 'N' and hp '100'
        And There is a missile at '5','5' with speed '2', course 'E' and damage '50'
        When The missile moves
        Then I should see the missile at the new position '5','7'

    Scenario: Move to the right border
        Given The user '1' has a ship 'Destroyer' in '2','2' with course 'N' and hp '100'
        And The user '2' has a ship 'Destroyer' in '2','11' with course 'N' and hp '100'
        And There is a missile at '5','20' with speed '2', course 'E' and damage '50'
        When The missile moves
        Then Missile should be destroyed

    Scenario: Move to the left border
        Given The user '1' has a ship 'Destroyer' in '2','2' with course 'N' and hp '100'
        And The user '2' has a ship 'Destroyer' in '2','11' with course 'N' and hp '100'
        And There is a missile at '5','1' with speed '2', course 'W' and damage '50'
        When The missile moves
        Then Missile should be destroyed

    Scenario: Move to the top border
        Given The user '1' has a ship 'Destroyer' in '2','2' with course 'N' and hp '100'
        And The user '2' has a ship 'Destroyer' in '2','11' with course 'N' and hp '100'
        And There is a missile at '1','5' with speed '2', course 'N' and damage '50'
        When The missile moves
        Then Missile should be destroyed

    Scenario: Move to the bottom border
        Given The user '1' has a ship 'Destroyer' in '2','2' with course 'N' and hp '100'
        And The user '2' has a ship 'Destroyer' in '2','11' with course 'N' and hp '100'
        And There is a missile at '20','5' with speed '2', course 'E' and damage '50'
        When The missile moves
        Then Missile should be destroyed

    Scenario: Move to a position with a ship and destroy it
        Given The user '1' has a ship 'Battleship' in '8','15' with course 'N' and hp '10'
        And The user '2' has a ship 'Destroyer' in '2','11' with course 'N' and hp '100'
        And There is a missile at '8','13' with speed '3', course 'E' and damage '50'
        When The missile moves
        Then Missile should be destroyed
        And The ship at '8','15' should be destroyed

    Scenario: Move to a position with a ship and hit it
        Given The user '1' has a ship 'Battleship' in '8','15' with course 'N' and hp '51'
        And The user '2' has a ship 'Destroyer' in '2','11' with course 'N' and hp '100'
        And There is a missile at '8','13' with speed '3', course 'E' and damage '50'
        When The missile moves
        Then Missile should be destroyed
        And The ship at '8','15' should have '1' hp

