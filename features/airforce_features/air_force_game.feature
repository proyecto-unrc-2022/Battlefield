Feature: game logic
    
    @air_force_game
    Scenario: User start new game
        Given three logged user
        When enter in empty game
        Then players id who are in the game are returned


    @air_force_game
    Scenario: Second user enter in the game
        Given three logged user
        When second user enter in the game
        Then two users info are returned

    @air_force_game
    Scenario: Third user try enter in the game
        Given three logged user
        When new user try enter in the game
        Then status code 400 is returned

    @air_force_game
    Scenario: Player_a choose a plane and position at the map
        Given player_a and plane in db
        When player_a choose a plane and his position
        Then info of the new flying object are returned

    @air_force_game
    Scenario: Player_a choose an other plane try to add in the battlefield
        Given player_a and plane in db
        When player_a choose try add new plane
        Then 400 response are returned

    @air_force_game
    Scenario: Player_b choose a plane and position at the map
        Given player_b in the game and plane in db
        When player_b choose a plane and his position
        Then info of the new flying object are returned
    
    @air_force_game
    Scenario: Player_a choose a plane and position outside of map
        Given player_a and plane in db
        When choose a plane and position outside of map
        Then 400 response are returned

    @air_force_game
    Scenario: Player_a choose a plane and position in enemy position
        Given player_a and plane in db
        When choose a plane and position in player_b position
        Then Error status code are returned

    @air_force_game
    Scenario: Player_b choose a plane and position in enemy position
        Given player_b in the game and plane in db
        When choose a plane and position in player_a position   
        Then Error status code are returned

    @air_force_game
    Scenario: Player_a move his plane in the same course
        Given a battlefield with player_a's plane 
        When player_a moves his plane in th same course
        Then 201 response code are returned

    @air_force_game
    Scenario: Player_a move his plane in new course
        Given a battlefield with player_a's plane 
        When player_a moves his plane in new valid course
        Then 201 response code are returned
    
    @air_force_game
    Scenario: Player_a move his plane in valid course and colition with a limit
        Given a battlefield with player_a's plane 
        When player_a moves his plane and colition with a limit
        Then 201 response code are returned
    
    @air_force_game
    Scenario: Player_a move his plane in invalid course
        Given a battlefield with player_a's plane 
        When player_a moves his plane in invalid course
        Then 400 response code are returned

    @air_force_game
    Scenario: Player_b move his plane and crash with player_a planes
        Given a battlefield with player_a's and player_b's plane
        When player b moves his plane and crash with player_a planes
        Then battlefield are returned