Feature: Creation and movement of a machine_gun

    @air_force_machine_gun
    Scenario: Create a machine_gun
    Given an user and a plane in a valid position
    When create a machine gun
    Then '200' response