Feature: Move a missile

    Background: Login a user and initialized app with a game
        Given Im logged as 'user1'
        And the app is initialized
        And the game one is started

    Scenario: Move to a valid position
        Given I have a ship 'Destroyer' at '2','2' and 'Cruiser' with '10' hp at '8','15' on the board game
        And I have a missile at '5','5' with '2' range, direction 'E' and damage '50'
        When I move the missile
        Then I should see the missile at the new position '5,'7'

    Scenario: Move to the right border
        Given I have a ship 'Destroyer' at '2','2' and 'Battleship' with '10' hp at '8','15' on the board game
        And I have a missile at '5','20' with '2' range, direction 'E' and damage '50'
        When I move the missile
        Then Missile should be destroyed

    Scenario: Move to the left border
        Given I have a ship 'Destroyer' at '2','2' and 'Battleship' with '10' hp at '8','15' on the board game
        And I have a missile at '5','1' with '2' range, direction 'W' and damage '50'
        When I move the missile
        Then Missile should be destroyed

    Scenario: Move to the top border
        Given I have a ship 'Destroyer' at '2','2' and 'Battleship' with '10' hp at '8','15' on the board game
        And I have a missile at '1','5' with '2' range, direction 'N' and damage '50'
        When I move the missile
        Then Missile should be destroyed

    Scenario: Move to the bottom border
        Given I have a ship 'Destroyer' at '2','2' and 'Battleship' with '10' hp at '8','15' on the board game
        And I have a missile at '20','5' with '2' range, direction 'S' and damage '50'
        When I move the missile
        Then Missile should be destroyed

    Scenario: Move to a position with a ship and destroy it
        Given I have a ship 'Destroyer' at '2','2' and 'Battleship' with '10' hp at '8','15' on the board game
        And I have a missile at '8','13' with '3' range, direction 'E' and damage '50'
        When I move the missile
        Then Missile should be destroyed
        And The ship at '8','15' should be destroyed

    Scenario: Move to a position with a ship and hit it
        Given I have a ship 'Destroyer' at '2','2' and 'Battleship' with '51' hp at '8','15' on the board game
        And I have a missile at '8','13' with '3' range, direction 'E' and damage '50'
        When I move the missile
        Then Missile should be destroyed
        And The ship at '8','15' should have '1' hp

    Scenario: Move to a position with a missile and destroy both
        Given I have a ship 'Destroyer' at '2','2' and 'Battleship' with '10' hp at '8','15' on the board game
        And I have a missile at '8','13' with '3' range, direction 'E' and damage '50'
        And I have a missile at '8','14' with '3' range, direction 'E' and damage '50'
        When I move the missile
        Then Missile should be destroyed
        And The enemy missile at '8','14' should be destroyed






