# features/tests/signin_invalid_password.feature
Feature: Target Sign In - invalid password (HW9)

  @hw9 @signin
  Scenario: Error is shown when logging in with an incorrect password
    Given I open Target Sign In page
    When I enter email "__FROM_ENV__" and continue
    And I enter password "thisIsWrong123" and submit with password
    Then I see a sign-in error message