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
    
    Scenario: Un unidad se mueve hacia el este
        Given un usuario Franco
        When elige mover su unidad hacia el este
        Then entonces la unidad se mueve hacia el este