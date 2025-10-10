Feature: Access Sign In as a logged-out user

  Scenario: Logged-out user can open the Sign In form
    Given Open target main page
    When Click Sign In (header)
    And From side navigation, click Sign In
    Then Verify Sign In form is shown
