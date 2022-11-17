Feature: Create, get, update and delete a Navy Game from API

  Background: Login a user and initialize the app
    Given a user '1' logged in

  Scenario: Create a navy game
    When I create a new game 
    Then The game should be created

  Scenario: Get all navy games
    Given Some games have been created  
    When I try to get all navy games in the app 
    Then I should get all navy games in the app 
  
  Scenario: Get all navy games by user
    Given Some games have been created  
    When I try to get all navy games for user1 
    Then I should get all navy games for user1 

  Scenario: Get a navy game by id
    Given Some games have been created  
    When I try to get the game with id 1
    Then I should get the game with id 1  

  Scenario: Join a second player to an existing navy game
    Given A game by another user has been created  
    When I try to join to the game 
    Then The game should be updated 

  Scenario: Delete a navy game
    Given Some games have been created  
    When I try to delete the game with id 1
    Then The game with id 1 should be deleted  
