@wip
Feature: User login (bonus)

  @bonus
  Scenario: User can log in with valid credentials
    Given Open target main page
    When Click Sign In (header)
    And From side navigation, click Sign In
    And I login with valid credentials
    Then Verify user is logged in