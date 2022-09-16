Feature: Users

  Scenario: Access to a User profile
     Given there is a Users with Profile
     When we query the user information
     Then I would like to see the Profile information
