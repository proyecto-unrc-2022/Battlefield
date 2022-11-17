Feature: Actions before move

    Background: Login a user and initialize the app
        Given a user '1' logged in
        And a user '2' exists
        And the app is initialized

    Scenario: Game doesn't exist
        Given Is my turn
        And The user '1' has a 'Destroyer' in '1','1' with course 'N'
        When I try to move in a game that doesn't exist
        Then I should see an error message 'Game not found'

    Scenario: Invalid action
        Given Is my turn
        And The user '1' has a 'Battleship' in '2','3' with course 'N'
        When I try to move in a game with an invalid action like shoot and move
        Then I should see an error message 'Invalid move'

    Scenario: Incorrect direction
        Given Is my turn
        And The user '1' has a 'Corvette' in '6','3' with course 'N'
        When I try to move in a game with an incorrect direction like 'Z'
        Then I should see an error message 'Must be one of: N, S, E, W, SE, SW, NE, NW.'

    Scenario: Incorrect distance to move
        Given Is my turn
        And The user '1' has a 'Corvette' in '1','3' with course 'S'
        When I try to move in a game with an incorrect distance like '-1'
        Then I should see an error message 'The movement is a negative distance'

    Scenario: Incorrect range of distance to move
        Given Is my turn
        And The user '1' has a 'Destroyer' in '1','3' with course 'E'
        When I try to move in a game with an incorrect move range like '5'
        Then I should see an error message 'Can't move more than 3 spaces'

    Scenario: Ship doesn't exist
        Given Is my turn
        And The user '1' has a 'Cruiser' in '6','7' with course 'S'
        When I try to move a ship that doesn't exist in the game
        Then I should see an error message 'Ship not found'

    Scenario: Incorrect ship selected
        Given Is my turn
        And The user '1' has a 'Battleship' in '2','5' with course 'N'
        And The user '2' has a 'Cruiser' in '4','3' with course 'N'
        When I try to move user 2's ship
        Then I should see an error message 'Invalid ship in game'

    Scenario: The game is over
        Given The game is already finished
        And The user '1' has a 'Destroyer' in '2','7' with course 'N'
        When I try to make an action in the ended game
        Then I should see an error message 'Game finished'

    Scenario: Player make two consecutive actions
        Given Is my turn
        And The user '1' has a 'Battleship' in '2','5' with course 'N'
        When I move the ship 3 positions to 'N'
        And  I try to move the ship again
        Then I should see an error message 'No its your turn yet'

