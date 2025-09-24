Feature: Target Sign In navigation

  Scenario: Logged out user can navigate to Sign In
    Given Open target main page
    When Click Sign In
    And From right side navigation menu, click Sign In
    Then Verify Sign In form opened