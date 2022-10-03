Feature: Move a missile

    Background: Login a user and initialized app
        Given Im logged as "user1"
        And the app is initialized

    Scenario: Move a missile to a new position
        Given I have a missile in the board game
        And two ships far away from the range of the missile
        When I move the missile to a new position
        Then the missile is moved to the new position
        And the missile is not exploded
        

