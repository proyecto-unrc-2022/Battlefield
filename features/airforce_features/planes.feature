Feature: Airplane description

    Scenario: Acces to airplane information
        Given A  plane with information
        When We query the plane information
        Then We see the information from the plane