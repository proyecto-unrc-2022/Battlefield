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
    
    Scenario: Una unidad se mueve hacia el este
        Given un usuario Franco
        When elige mover su unidad hacia el este
        Then entonces la unidad se mueve hacia el este
    
    Scenario: Una unidad se mueve hacia el oeste
        Given un usuario Tomas
        When elige mover su unidad hacia el oeste
        Then entonces la unidad se mueve hacia el oeste

    Scenario: Una unidad hace un movimiento invalido
        Given un usuario Tomas
        When elige un movimiento invalido
        Then la unidad no se mueve

    Scenario: A user shoots
        Given a user Nicolas
        When Shoot
        Then create the projectile
    