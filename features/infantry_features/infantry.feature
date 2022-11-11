Feature: Infantry

    Scenario: The creation of the game
        Given the first player Franco
        When you create the game
        Then it is the first player

    Scenario: Join a game
        Given the second player Tomas
        When he joins the game
        Then he is the second player
    