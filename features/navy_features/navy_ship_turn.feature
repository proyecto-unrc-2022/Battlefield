Feature: Turn a ship

    Background: Login a user and initialized app with a game
        Given a user '1' logged in
        And a user '2' logged in
        And the user '1' created a NavyGame '1'
        And the user '2' joined the NavyGame '1'

    Scenario: A ship turns and doesn't collide with anything
        Given the user '1' created a 'Destroyer' in '5', '5' with course 'N' and '60' hp in the NavyGame '1'
        And the user '2' created a 'Destroyer' in '5', '15' with course 'S' and '60' hp in the NavyGame '1'
        When the user '1' turns his ship to 'E' and moves it '0' cells for round '1' in NavyGame '1'
        And the user '2' turns his ship to 'W' and moves it '0' cells for round '1' in NavyGame '1'
        And the NavyGame '1' updates for user '1'
        And the NavyGame '1' updates for user '2'
        Then the user '1' should see his ship with the course 'E' at '5', '5' with '60' hp in the NavyGame '1'
        Then the user '2' should see his ship with the course 'W' at '5', '15' with '60' hp in the NavyGame '1'
