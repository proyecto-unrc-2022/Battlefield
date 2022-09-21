Feature: All possible movements and rotations of the plane

    Scenario: Rotation of the plane
        Given A plane on the map
        When I make the rotation
        Then I should obtain a '201' response