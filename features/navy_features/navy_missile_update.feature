Feature: Move a missile

    Background: Logged users and start a game
        Given a user '1' logged in
        And a user '2' logged in
        And the user '1' created a NavyGame '1'
        And the user '2' joined the NavyGame '1'

    Scenario: Missile update to a valid position
        Given the user '1' created a 'Destroyer' in '2', '2' with course 'N' and '60' hp in the NavyGame '1'
        And the user '2' created a 'Destroyer' in '5', '11' with course 'N' and '60' hp in the NavyGame '1'
        And a missile exists from user '2' in '5', '5' with course 'E', speed '2', and damage '50' in the NavyGame '1'
        When the user '1' turns his ship to 'E' and moves it '0' cells for round '1' in NavyGame '1'
        And the user '2' turns his ship to 'W' and moves it '0' cells for round '1' in NavyGame '1'
        Then a missile with course 'E', speed '2', and damage '50' should be in '5', '7' in the NavyGame '1'

    Scenario: Missile update to the right border
        Given the user '1' created a 'Destroyer' in '2', '2' with course 'N' and '60' hp in the NavyGame '1'
        And the user '2' created a 'Destroyer' in '2', '11' with course 'N' and '60' hp in the NavyGame '1'
        And a missile exists from user '2' in '5', '20' with course 'E', speed '2', and damage '50' in the NavyGame '1'
        When the user '1' turns his ship to 'E' and moves it '0' cells for round '1' in NavyGame '1'
        And the user '2' turns his ship to 'W' and moves it '0' cells for round '1' in NavyGame '1'
        Then the missile '1' in NavyGame '1' should be destroyed

    Scenario: Missile update to the left border
        Given the user '1' created a 'Destroyer' in '2', '2' with course 'N' and '60' hp in the NavyGame '1'
        And the user '2' created a 'Destroyer' in '2', '11' with course 'N' and '60' hp in the NavyGame '1'
        And a missile exists from user '2' in '5', '1' with course 'W', speed '2', and damage '50' in the NavyGame '1'
        When the user '1' turns his ship to 'E' and moves it '0' cells for round '1' in NavyGame '1'
        And the user '2' turns his ship to 'W' and moves it '0' cells for round '1' in NavyGame '1'
        Then the missile '1' in NavyGame '1' should be destroyed

    Scenario: Missile update to the top border
        Given the user '1' created a 'Destroyer' in '2', '2' with course 'N' and '60' hp in the NavyGame '1'
        And the user '2' created a 'Destroyer' in '2', '11' with course 'N' and '60' hp in the NavyGame '1'
        And a missile exists from user '2' in '1', '5' with course 'N', speed '2', and damage '50' in the NavyGame '1'
        When the user '1' turns his ship to 'E' and moves it '0' cells for round '1' in NavyGame '1'
        And the user '2' turns his ship to 'W' and moves it '0' cells for round '1' in NavyGame '1'
        Then the missile '1' in NavyGame '1' should be destroyed

    Scenario: Missile update to the bottom border
        Given the user '1' created a 'Destroyer' in '2', '2' with course 'N' and '60' hp in the NavyGame '1'
        And the user '2' created a 'Destroyer' in '2', '11' with course 'N' and '60' hp in the NavyGame '1'
        And a missile exists from user '2' in '20', '5' with course 'E', speed '2', and damage '50' in the NavyGame '1'
        When the user '1' turns his ship to 'E' and moves it '0' cells for round '1' in NavyGame '1'
        And the user '2' turns his ship to 'W' and moves it '0' cells for round '1' in NavyGame '1'
        Then the missile '1' in NavyGame '1' should be destroyed

    Scenario: Missile update and destroys a ship
        Given the user '1' created a 'Destroyer' in '5', '5' with course 'N' and '60' hp in the NavyGame '1'
        And the user '2' created a 'Destroyer' in '5', '15' with course 'N' and '60' hp in the NavyGame '1'
        And a missile exists from user '2' in '6', '7' with course 'W', speed '3', and damage '60' in the NavyGame '1'
        When the user '1' turns his ship to 'E' and moves it '0' cells for round '1' in NavyGame '1'
        And the user '2' turns his ship to 'W' and moves it '0' cells for round '1' in NavyGame '1'
        And the NavyGame '1' updates for user '1'
        And the NavyGame '1' updates for user '2'
        Then the user '1' should see his ship with the course 'N' at '5', '5' with '0' hp in the NavyGame '1'
        And the missile '1' in NavyGame '1' should be destroyed
        And the user '2' should be the winner in the NavyGame '1'

    Scenario: Missile update and hits a ship
        Given the user '1' created a 'Destroyer' in '5', '5' with course 'N' and '60' hp in the NavyGame '1'
        And the user '2' created a 'Destroyer' in '5', '15' with course 'N' and '60' hp in the NavyGame '1'
        And a missile exists from user '2' in '6', '7' with course 'W', speed '3', and damage '30' in the NavyGame '1'
        When the user '1' turns his ship to 'E' and moves it '0' cells for round '1' in NavyGame '1'
        And the user '2' turns his ship to 'W' and moves it '0' cells for round '1' in NavyGame '1'
        And the NavyGame '1' updates for user '1'
        And the NavyGame '1' updates for user '2'
        Then the user '1' should see his ship with the course 'E' at '5', '5' with '30' hp in the NavyGame '1'
