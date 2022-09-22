Feature: Location of the plane at the beginning of the game

    @air_force
    Scenario: Location of the plane on a empty map
        Given a map with no planes in it
        When i place a plane 
        Then i should get a '200' response
        And the plane is in a correctly position
