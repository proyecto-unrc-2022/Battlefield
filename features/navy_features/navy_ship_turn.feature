Feature: Turn a ship

    Background: Login a user and initialized app with a game
        Given a user '1' logged in
        And a user '2' logged in
        And the user '1' created a NavyGame '1'
        And the user '2' joined the NavyGame '1'

    Scenario: A ship turns and doesn't collide with anything
        Given the user '1' created a 'Destroyer' in '5', '5' with course 'N' for the NavyGame '1'
        And the user '2' created a 'Destroyer' in '5', '15' with course 'S' for the NavyGame '1'
        When the user '1' turns his ship to 'E' and moves it '0' cells for NavyGame '1'
        And the user '2' turns his ship to 'W' and moves it '0' cells for NavyGame '1'
        And the NavyGame '1' updates
        Then the user '1' should see his ship with the course 'E' at '5', '5' with '60' hp for the NavyGame '1'
        Then the user '2' should see his ship with the course 'W' at '5', '15' with '60' hp for the NavyGame '1'

    Scenario: A ship turns and collides with a missile and stills alive
        Given the user '1' created a 'Destroyer' in '5', '5' with course 'N' for the NavyGame '1'
        And the user '2' created a 'Destroyer' in '5', '15' with course 'S' for the NavyGame '1'
        When the user '1' turns his ship to 'E' and moves it '2' cells for NavyGame '1'
        And the user '2' turns his ship to 'W' and attacks for NavyGame '1'
        And the NavyGame '1' updates
        And the user '2' turns his ship to 'W' and moves it '0' cells for NavyGame '1'
        And the user '1' turns his ship to 'W' and moves it '0' cells for NavyGame '1'
        And the NavyGame '1' updates
        Then the user '1' should see his ship with the course 'E' at '5', '7' with '40' hp for the NavyGame '1'

    Scenario: A ship turns and collides with a missile and it dies
        Given the user '1' created a 'Destroyer' in '5', '5' with course 'N' for the NavyGame '1'
        And the user '2' created a 'Battleship' in '5', '15' with course 'S' for the NavyGame '1'
        When the user '1' turns his ship to 'E' and moves it '3' cells for NavyGame '1'
        And the user '2' turns his ship to 'W' and attacks for NavyGame '1'
        And the NavyGame '1' updates
        And the user '2' turns his ship to 'W' moves it '0' cells for NavyGame '1'
        And the user '1' turns his ship to 'W' and moves it '0' cells for NavyGame '1'
        And the NavyGame '1' updates
        Then the user '1' should see his ship with the course 'E' at '5', '7' with '0' hp for the NavyGame '1'
        And the user '2' should be the winner

    Scenario: A ship turns and collides with another ship
        Given the user '1' created a 'Cruiser' in '5', '10' with course 'N' for the NavyGame '1'
        And the user '2' created a 'Destroyer' in '5', '11' with course 'N' for the NavyGame '1'
        When the user '1' turns his ship to 'E' and moves it '3' cells for NavyGame '1'
        And the user '2' turns his ship to 'N' moves it '0' cells for NavyGame '1'
        And the NavyGame '1' updates
        Then the user '2' should see his ship with the course 'N' at '5', '11' with '0' hp for the NavyGame '1'
        And the user '1' should be the winner

