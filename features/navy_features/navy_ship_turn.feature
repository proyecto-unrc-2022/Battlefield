Feature: Turn a ship

    Background: Login a user and initialized app with a game
        Given I am logged in as "user1"
        And another user exists as "user2"
        And the game is started

    Scenario: A ship turns and doesn't collide with anything
        Given The user '1' has a ship 'Destroyer' in '5','5' with course 'N' and hp '100'
        When The ship with id '1' turns to 'W'
        Then I should see the ship '1' with the new course 'W'

    Scenario: A ship turns and collides with a missile and stills alive
        Given The user '1' has a ship 'Destroyer' in '5','5' with course 'N' and hp '100'
        And There is a missile at '5','6' with speed '3', course 'W' and damage '50'
        When The ship with id '1' turns to 'W'
        Then I should see the ship '1' with the new course 'W'
        And The ship with id '1' should have '50' hp

    Scenario: A ship turns and collides with a missile and it dies
        Given The user '1' has a ship 'Destroyer' in '5','5' with course 'N' and hp '40'
        And There is a missile at '5','6' with speed '3', course 'W' and damage '50'
        When The ship with id '1' turns to 'W'
        Then The ship with id '1' should be destroyed

    Scenario: A ship turns and collides with another ship and wins
        Given The user '1' has a ship 'Destroyer' in '5','5' with course 'N' and hp '100'
        Given The user '2' has a ship 'Cruiser' in '5','6' with course 'N' and hp '60'
        When The ship with id '1' turns to 'W'
        Then The ship with id '2' should be destroyed

    Scenario: A ship turns and collides with another ship and lose
        Given The user '1' has a ship 'Destroyer' in '5','5' with course 'N' and hp '60'
        Given The user '2' has a ship 'Cruiser' in '5','6' with course 'N' and hp '100'
        When The ship with id '1' turns to 'W'
        Then The ship with id '1' should be destroyed
