Feature: Move a missile

    Background: Login a user and initialized app with a game
        Given Im logged as 'user'
        And the app is initialized
        And the game is started

    Scenario: Move to a valid position
        Given I have a ship 'Destroyer' in '2','2' with course 'N' and hp '100'
        And Exist a missile at '5','5' with speed '2', course 'E' and damage '50'
        When The missile move
        Then I should see the missile at the new position '5','7'

    Scenario: Move to the right border
        Given I have a ship 'Destroyer' in '2','2' with course 'N' and hp '100'
        And Exist a missile at '5','20' with speed '2', course 'E' and damage '50'
        When The missile move
        Then Missile should be destroyed

    Scenario: Move to the left border
        Given I have a ship 'Destroyer' in '2','2' with course 'N' and hp '100'
        And Exist a missile at '5','1' with speed '2', course 'W' and damage '50'
        When The missile move
        Then Missile should be destroyed

    Scenario: Move to the top border
        Given I have a ship 'Destroyer' in '2','2' with course 'N' and hp '100'
        And Exist a missile at '1','5' with speed '2', course 'N' and damage '50'
        When The missile move
        Then Missile should be destroyed

    Scenario: Move to the bottom border
        Given I have a ship 'Destroyer' in '2','2' with course 'N' and hp '100'
        And Exist a missile at '20','5' with speed '2', course 'E' and damage '50'
        When The missile move
        Then Missile should be destroyed

    Scenario: Move to a position with a ship and destroy it
        Given I have a ship 'Battleship' in '8','15' with course 'N' and hp '10'
        And Exist a missile at '8','13' with speed '3', course 'E' and damage '50'
        When The missile move
        Then Missile should be destroyed
        And The ship at '8','15' should be destroyed

    Scenario: Move to a position with a ship and hit it
        Given I have a ship 'Battleship' in '8','15' with course 'N' and hp '51'
        And Exist a missile at '8','13' with speed '3', course 'E' and damage '50'
        When The missile move
        Then Missile should be destroyed
        And The ship at '8','15' should have '1' hp

