Feature: Actions before move

    Background: Login a user - initialize the app
        Given I am logged in as "user"
        And the app is initialized

    Scenario: Game doesn't exist
        Given Is my turn
        When I try to move in a game that doesn't exist
        Then I should see an error message 'Game doesn't exist'

    Scenario: Invalid action
        Given Is my turn
        And I have a 'Destroyer' and can move '3' spaces with its
        When I try to move in a game with an invalid action like shoot and move
        Then I should see an error message 'Invalid move'


    Scenario: Not is my Game
        Given Is my turn
        When I try to move in a game that is not mine
        Then I should see an error message 'You try to access a game that is not yours'

    Scenario: User doesn't exist
        Given Is my turn
        When I try to move in a game with a user that doesn't exist
        Then I should see an error message 'User doesn't exist'

    Scenario: Incorrect direction
        Given Is my turn
        And I have a ship in (1,1)
        When I try to move in a game with an incorrect direction like 'Z'
        Then I should see an error message about the wrong 'direction'

    Scenario: Incorrect distance to move
        Given Is my turn
        And I have a 'Destroyer' and can move '3' spaces with its
        When I try to move in a game with an incorrect distance like '-1'
        Then I should see an error message about the wrong 'distance'

    Scenario: Incorrect ship selected
        Given Is my turn
        And I have a 'Battleship' and can move '4' spaces with its
        When I try to move in a game with an incorrect ship selected like 'Mostroyer'
        Then I should see an error message about the wrong 'ship selected'

    Scenario: Incorrect attack status
        Given Is my turn
        And I Have a 'Destroyer' and can move '3' spaces with its
        When I try to move in a game with an incorrect attack status like '2'
        Then I should see an error message about the wrong 'attack'




