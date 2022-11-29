Feature: Create, get, update and delete a Navy Game from API

    Background: Login users
        Given a user '1' logged in

    Scenario: Create a NavyGame
        When the user '1' creates a NavyGame '1'
        Then the user '1' should see that the NavyGame was created

    Scenario: Get all NavyGames
        Given a user '2' logged in
        And the user '1' created a NavyGame '1'
        And the user '2' created a NavyGame '2'
        When the user '1' tries to get all NavyGames in the app 
        Then the user '1' should get all NavyGames in the app

    Scenario: Get a NavyGame by id
        Given the user '1' created a NavyGame '1'
        When the user '1' tries to get the NavyGame '1'
        Then the user '1' should get the NavyGame '1'

    Scenario: A user joins a created NavyGame
        Given a user '2' logged in
        And the user '2' created a NavyGame '1'
        When the user '1' tries to join the NavyGame '1'
        Then the user '1' should see that the NavyGame was updated

    Scenario: Delete a NavyGame
        Given the user '1' created a NavyGame '1'
        When the user '1' deletes the NavyGame '1'
        Then the user '1' should see that the NavyGame was deleted
