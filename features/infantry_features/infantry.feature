Feature: Infantry

    Scenario: An user create an soldier
        Given a user Ignacio
        When you choose your soldier
        Then the soldier is created

    Scenario: An user create an Humvee
        Given a user Matias
        When you choose your Humvee
        Then the humvee is created

    Scenario: An user create an tank
        Given a user Lucas
        When you choose your tank
        Then the tank is created

    Scenario: An user create an artillery
        Given a user Ricardo
        When you choose your artillery
        Then the artillery is created

    Scenario: The creation of the game
        Given the first player
        When you create the game
        Then it is the first player

    Scenario: Join a game
        Given the second player
        When he joins the game
        Then he is the second player