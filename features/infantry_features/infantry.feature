Feature: Infantry

    Scenario: The creation of the game
        Given the first player Franco
        When you create the game
        Then it is the first player

    Scenario: Join a game
        Given the second player Tomas
        When he joins the game
        Then he is the second player

        Scenario: An user create an soldier
        Given a user Franco
        When you choose your soldier
        Then the soldier is created

    Scenario: An user create an Humvee
        Given a user Tomas
        When you choose your Humvee
        Then the humvee is created
    
    Scenario: One unit moves east
        Given a user Franco
        When you choose to move your unit east
        Then the unit moves east
    
    Scenario: One unit moves west
        Given a user Tomas
        When you choose to move your unit west
        Then the unit moves west

    Scenario: A unit makes an invalid move
        Given a user Tomas
        When choose an invalid move
        Then the unit does not move

    Scenario: A user shoots
        Given a user Nicolas
        When Shoot
        Then create the projectile
    