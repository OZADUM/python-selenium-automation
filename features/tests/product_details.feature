Feature: Tests for product page

  Scenario: User can select colors
    Given Open target product A-91269718 page
    Then Verify user can click through colors

    Feature: Product details page

  Scenario: Click each color and verify selection
    Given I open the product page "https://www.target.com/p/A-91511634"
    When I click each available color
    Then Each color is selected successfully
