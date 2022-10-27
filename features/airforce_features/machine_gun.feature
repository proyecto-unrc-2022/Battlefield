Feature: Creation of a machine_gun

	    @air_force_machine_gun
	    Scenario: Create a machine_gun
	    Given an user and a plane in a valid position
	    When create a machine gun
	    Then '200' resp.

	#behave --tags @air_force_machine_gun --no-skipped