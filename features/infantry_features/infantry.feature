Feature: Infantry

    #Game
    Scenario: The creation of the game
        Given the first player Franco
        When you create the game
        Then it is the first player

    Scenario: Join a game
        Given the second player Tomas
        When he joins the game
        Then he is the second player

    Scenario: A player enters the same game that I create
        Given user any
        When you create a game
        Then he can not join a game that he created himself
    
    #Figure
    Scenario: The creation of the figure
        Given a user with the corresponding coordinates
        When you choose the figure and it is created
        Then wait the opponent

    Scenario: Create the figure incorrectly
          Given a user with the wrong coordinates
          When you choose the figure
          Then it couldn not have been created

    Scenario: The creation of the type 1 figure
          Given a user x
          When you select the type 1 figure
          Then this figure is created for the user x

    Scenario: The creation of the type 2 figure
          Given a user y
          When you select the type 2 figure
          Then this figure is created for the user y

    Scenario: The creation of the type 3 figure
          Given a user z
          When you select the type 3 figure
          Then this figure is created for the user z

    Scenario: The creation of the type 4 figure
          Given a user t
          When you select the type 4 figure
          Then this figure is created for the user t
    
    #Proyectil
   Scenario: Create a projectile for the type 1 figure
          Given figure 1
          When he shoots for figure 1
          Then your projectile is created for figure 1
    
    Scenario: Create a projectile for the type 2 figure
          Given figure 2
          When he shoots for figure 2
          Then your projectile is created for figure 2

    Scenario: Create a projectile for the type 3 figure
          Given figure 3
          When he shoots for figure 3
          Then your projectile is created for figure 3

    Scenario: Create a projectile for the type 4 figure
          Given figure 4
          When he shoots for figure 4
          Then your projectile is created figure 4

    