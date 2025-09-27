Feature: Tests for product page

  @smoke
  Scenario: User can select colors
    Given Open target product A-91269718 page
    Then Verify user can click through colors
