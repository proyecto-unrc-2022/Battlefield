Feature: game logic

Scenario: User start new game
Given logged user
When start new game
Then new game is created
And resoponse are 200

Scenario: Unlogged ser start new game
Given unlogged user
When try start new game
Then 401 resoponse

Scenario: User choice a plane
Given new game and logged user 
When choice a plane
Then plane id is returnes
And 200 resoponse

Scenario: second user enter to a game
Given created game with one user and new logged user
When new user enter to a game
Then two players id are returnes
And 200 resoponse

Scenario: start to play
Given created game with two logged users
When to logged are ready
Then map are created
And 200 resoponse