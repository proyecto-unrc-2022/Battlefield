Feature: Actions before move

    Background: Login a user - initialize the app
        Given I am logged in as "user"
        And the app initialized

    Scenario: Game doesn't exist
        Given Is my turn
        When I try to move in a game that doesn't exist
        Then I should see an error message 'Game not found' about the 'game'




