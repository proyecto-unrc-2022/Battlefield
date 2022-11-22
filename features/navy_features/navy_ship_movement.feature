Feature: Ship Movement

    Background: Logged users and start a game
        Given a user '1' logged in
        And a user '2' logged in
        And the user '1' created a NavyGame '1'
        And the user '2' joined the NavyGame '1'

    Scenario: Move without collision
        Given the user '1' created a 'Destroyer' in '5', '5' with course 'N' and '60' hp in the NavyGame '1'
        And the user '2' created a 'Destroyer' in '5', '15' with course 'S' and '60' hp in the NavyGame '1'
        When the user '1' turns his ship to 'SE' and moves it '2' cells for round '1' in NavyGame '1'
        And the user '2' turns his ship to 'NW' and moves it '3' cells for round '1' in NavyGame '1'
        And the NavyGame '1' updates for user '1'
        And the NavyGame '1' updates for user '2'
        Then the user '1' should see his ship with the course 'SE' at '7', '7' with '60' hp in the NavyGame '1'
        Then the user '2' should see his ship with the course 'NW' at '2', '12' with '60' hp in the NavyGame '1'

    Scenario: Ship collides with a ship and is destroyed
        Given the user '1' created a 'Cruiser' in '5', '9' with course 'E' and '100' hp in the NavyGame '1'
        And the user '2' created a 'Destroyer' in '5', '13' with course 'W' and '60' hp in the NavyGame '1'
        When the user '1' turns his ship to 'E' and moves it '3' cells for round '1' in NavyGame '1'
        And the user '2' turns his ship to 'W' and moves it '1' cells for round '1' in NavyGame '1'
        And the NavyGame '1' updates for user '1'
        And the NavyGame '1' updates for user '2'
        Then the user '2' should see his ship with the course 'W' at '5', '12' with '-40' hp in the NavyGame '1'
        And the user '1' should be the winner in the NavyGame '1'

    Scenario: Ship collides with a missile and decreases its hp
        Given the user '1' created a 'Destroyer' in '5', '5' with course 'N' and '60' hp in the NavyGame '1'
        And the user '2' created a 'Destroyer' in '5', '15' with course 'S' and '60' hp in the NavyGame '1'
        And a missile exists from user '2' in '3', '4' with course 'E', speed '1', and damage '30' in the NavyGame '1'
        When the user '1' turns his ship to 'N' and moves it '3' cells for round '1' in NavyGame '1'
        And the user '2' turns his ship to 'S' and moves it '0' cells for round '1' in NavyGame '1'
        And the NavyGame '1' updates for user '1'
        Then the user '1' should see his ship with the course 'N' at '2', '5' with '30' hp in the NavyGame '1'
        And the missile '1' in NavyGame '1' should be destroyed

    Scenario: Ship collides with a missile and is destroyed
        Given the user '1' created a 'Destroyer' in '5', '5' with course 'N' and '60' hp in the NavyGame '1'
        And the user '2' created a 'Destroyer' in '5', '15' with course 'S' and '60' hp in the NavyGame '1'
        And a missile exists from user '2' in '3', '4' with course 'E', speed '1', and damage '60' in the NavyGame '1'
        When the user '1' turns his ship to 'N' and moves it '3' cells for round '1' in NavyGame '1'
        And the user '2' turns his ship to 'S' and moves it '0' cells for round '1' in NavyGame '1'
        And the NavyGame '1' updates for user '1'
        And the NavyGame '1' updates for user '2'
        Then the user '1' should see his ship with the course 'N' at '3', '5' with '0' hp in the NavyGame '1'
        And the missile '1' in NavyGame '1' should be destroyed
        And the user '2' should be the winner in the NavyGame '1'

