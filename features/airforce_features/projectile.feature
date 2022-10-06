Feature: Creation, movement of a projectile

    @air_force_projectile
    Scenario: Create a projectile
    Given a plane in a valid position
    When create a projectile
    Then '200' response

    @air_force_projectile_move
    Scenario: Movement of the projectile
    Given a projectile in some place of the map 
    When a new shift starts
    Then the projectile moved the speed corresponding
