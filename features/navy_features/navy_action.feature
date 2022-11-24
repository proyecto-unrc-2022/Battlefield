Feature: Creation of an action.

    Background: Logged users, game and ships created
        Given a user '1' logged in
        And a user '2' logged in
        And the user '1' created a NavyGame '1'
        And the user '2' joined the NavyGame '1'
        And the user '1' created a 'Destroyer' in '5', '5' with course 'N' and '60' hp in the NavyGame '1'
        And the user '2' created a 'Destroyer' in '5', '15' with course 'S' and '60' hp in the NavyGame '1'

    Scenario: Action creation for a non existing game
        When the user '1' turns his ship to 'E' and moves it '0' cells for round '1' in NavyGame '2'
        Then the user '1' should see an error message 'Game not found'

    Scenario: Move and attack in the same action.
        When the user '1' turns his ship to 'SE', moves it '2' cells and attacks for round '1' in NavyGame '1'
        Then the user '1' should see an error message 'Invalid action'

    Scenario: Move with an incorrect direction
        When the user '1' turns his ship to 'PEPE' and moves it '0' cells for round '1' in NavyGame '1'
        Then the user '1' should see an error message 'Must be one of: N, S, E, W, SE, SW, NE, NW.'

    Scenario: Move with a negative distance
        When the user '1' turns his ship to 'E' and moves it '-1' cells for round '1' in NavyGame '1'
        Then the user '1' should see an error message 'The move is a negative distance'

    Scenario: Move with incorrect range of distance
        When the user '1' turns his ship to 'E' and moves it '4' cells for round '1' in NavyGame '1'
        Then the user '1' should see an error message 'Can't move more than 3 spaces'

    Scenario: Move a ship that doesn't exist
        Given the user '1' created a NavyGame '2'
        Given the user '2' joined the NavyGame '2'
        When the user '1' turns his ship to 'E' and moves it '4' cells for round '1' in NavyGame '2'
        Then the user '1' should see an error message 'Game not started yet'

    Scenario: Move the other users ship
        When the user '1' turns users '2' ship to 'E' and moves it '4' cells for round '1' in NavyGame '1'
        Then the user '1' should see an error message 'Invalid ship in game'

    Scenario: Move in a finished game
        Given the user '1' created a NavyGame '2', but user '2' won it
        When the user '1' turns his ship to 'E' and moves it '4' cells for round '1' in NavyGame '2'
        Then the user '1' should see an error message 'Game finished'

    Scenario: Make two consecutive actions
        When the user '1' turns his ship to 'E' and moves it '3' cells for round '1' in NavyGame '1'
        When the user '1' turns his ship to 'W' and moves it '2' cells for round '1' in NavyGame '1'
        Then the user '1' should see an error message 'It's not your turn yet'

