Feature: Create a navy Ship for a Navy Game.
  
    Background: Login a user and initialize the app
        Given a user '1' logged in
        And a user '2' logged in

    Scenario: Create a valid ship as user 1
        Given the user '1' created a NavyGame '1'
        And the user '2' joined the NavyGame '1'
        When the user '1' creates a 'Destroyer' in '2', '3' with course 'N' for the NavyGame '1'
        Then the ship of user '1' should be created successfully

    Scenario: Create a valid ship as user 2
        Given the user '2' created a NavyGame '1'
        And the user '1' joined the NavyGame '1'
        When the user '1' creates a 'Destroyer' in '5', '17' with course 'N' for the NavyGame '1'
        Then the ship of user '1' should be created successfully

    Scenario: Create a ship with invalid name
        Given the user '1' created a NavyGame '1'
        And the user '2' joined the NavyGame '1'
        When the user '1' creates a 'Submarine' in '2', '3' with course 'N' for the NavyGame '1'
        Then the ship of user '1' shouldn't be created
        And the user '1' should see an error message 'Must be one of: Destroyer, Cruiser, Battleship, Corvette.'

    Scenario: Create a ship with invalid course
        Given the user '1' created a NavyGame '1'
        And the user '2' joined the NavyGame '1'
        When the user '1' creates a 'Destroyer' in '2', '3' with course 'K' for the NavyGame '1'
        Then the ship of user '1' shouldn't be created
        And the user '1' should see an error message 'Must be one of: N, S, E, W, SE, SW, NE, NW.'

    Scenario: Create a ship with invalid X coord
        Given the user '1' created a NavyGame '1'
        And the user '2' joined the NavyGame '1'
        When the user '1' creates a 'Destroyer' in '11', '3' with course 'N' for the NavyGame '1'
        Then the ship of user '1' shouldn't be created
        And the user '1' should see an error message 'Ship can't be builded out of range'

    Scenario: Create a ship with invalid Y coord as user 1
        Given the user '1' created a NavyGame '1'
        And the user '2' joined the NavyGame '1'
        When the user '1' creates a 'Destroyer' in '5', '16' with course 'N' for the NavyGame '1'
        Then the ship of user '1' shouldn't be created
        And the user '1' should see an error message 'Ship can't be builded out of range'

    Scenario: Create a ship with invalid Y coord as user 2
        Given the user '2' created a NavyGame '1'
        And the user '1' joined the NavyGame '1'
        When the user '1' creates a 'Destroyer' in '5', '3' with course 'N' for the NavyGame '1'
        Then the ship of user '1' shouldn't be created
        And the user '1' should see an error message 'Ship can't be builded out of range'