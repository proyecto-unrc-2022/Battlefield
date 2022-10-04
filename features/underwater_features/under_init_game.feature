Feature: Init Under Game

    Background: Two players are logged in
        Given there exists two users and they are logged in:
            |username   |password   |email              |
            |player1    |player1    |player1@example.com|
            |player2    |player2    |player2@example.com|

    Scenario: Create a new game
        When the user 'player1' asks for a new underwater game
        Then A new game is registered
        And an empty board with one player is returned

    Scenario: Join a game
        Given there is a game with no visitor
        When the user 'player2' joins that game
        Then the game now has the new visitor

    Scenario: Get the submarine options
        When I receive a request to show the submarine options
        Then the options are returned

    Scenario: Choose a submarine
        Given the user 'player1' is in a game of dimension '6'x'6' with visitor
        When the user 'player1' chooses a submarine
        Then the game bounds the user to the choosen submarine successfully

    Scenario: Choose an extra submarine
        Given the user 'player1' is in a game of dimension '6'x'6' with visitor
        And the user 'player1' chose 'Saukko' submarine
        When the user 'player1' chooses a submarine
        Then the system should not allow to have an extra submarine

    Scenario: Place a submarine
        Given the user 'player1' is in a game of dimension '6'x'6' with visitor
        And the user 'player1' chose 'Saukko' submarine
        When the user 'player1' chooses the position '2','4' and direction '0'
        Then the submarine is successfully placed

    Scenario: Place a submarine in an invalid position
        Given the user 'player1' is in a game of dimension '6'x'6' with visitor
        And the user 'player1' chose 'Saukko' submarine
        When the user 'player1' chooses the position '-2','4' and direction '0'
        Then the system should not allow to place the submarine in that position
    
    Scenario: Place a submarine already placed
        Given the user 'player1' is in a game of dimension '6'x'6' with visitor
        And the user 'player1' chose 'Saukko' submarine
        When the user 'player1' chooses the position '2','4' and direction '0'
        And the user 'player1' chooses the position '2','5' and direction '0'
        Then the system should not allow to place the submarine again

        #Preguntar si este escenario estaría bien 
    # Scenario: Place a submarine on an occupied position
    #     Given the user 'player1' is in a game of dimension '6'x'6' with visitor
    #     And the user 'player1' chose 'Saukko' submarine
    #     And the board is in the following state:
    #         | X |   |   |   |   |
    #         |   | X |   |   |   |
    #         |   |   | X |   |   |
    #         |   |   |   |   |   |
    #         |   |   |   |   |   |
    #     When the user 'player1' chooses the position '2','2' and direction '2'
    #     Then the system should not allow to place the submarine
