Feature: Infantry

    Scenario: An user create an soldier
        Given a user Ignacio
        When you choose your soldier
        Then the soldier is created

    Scenario: An user create an Humvee
        Given a user Matias
        When you choose your Humvee 
        Then the humvee is created

    Scenario: The creation of the game
          Given the first player
          When they press play
          Then the game begins