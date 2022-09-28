Feature: game logic
    
    @air_force_game
    Scenario: User start new game
        Given logged user
        When enter in empty game
        Then players id who are in the game are returned


    @air_force_game
    Scenario: Second user enter in the game
        Given a second user
        When new user enter in the game
        Then two users info are returned

    @air_force_game
    Scenario: Third user try enter in the game
        Given a third user
        When new user try enter in the game
        Then exception are returned

    @air_force_game
    Scenario: User choose a plane and position at the map
        Given a user in the game and plane in db
        When choose a plane and his position
        Then 201 response are returned