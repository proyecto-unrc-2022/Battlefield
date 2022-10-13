Feature: Actions before move

    Background: Login a user - initialize the app
        Given I am logged in as "user"
        And the app initialized

    Scenario: Game doesn't exist
        Given Is my turn
        When I try to move in a game that doesn't exist
        Then I should see an error message 'Game not found' about the game
    
    Scenario: Invalid action
        Given Is my turn
        And I have a 'Destroyer' and can move '3' spaces with its
        When I try to move in a game with an invalid action like shoot and move
        Then I should see an error message 'Invalid move'





