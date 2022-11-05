Feature: Actions before move

    Background: Login a user and initialize the app
        Given I am logged in as "user1"
        And another user exists as "user2"
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

    Scenario: User doesn't exist
        Given Is my turn
        And The user '1' has a 'Battleship' in '2','5' with course 'N'
        When I try to move in a game with a user that doesn't exist
        Then I should see an error message 'User not found'

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


