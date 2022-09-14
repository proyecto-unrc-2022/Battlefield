Feature: Some training tests

  #Background: Logged in User

  Scenario: Starting game
  Given the initialized application
  And I have some ships available
  When we request to play a game
  Then I should get the available ships

  Scenario: Ship Selection
  Given the available ships
  # Select a determinated ship
  When a ship, it's position and direction is selected
  And the position of the ship is correct
  Then I should see the ships positioned on the board