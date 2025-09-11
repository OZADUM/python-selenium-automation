Feature: Tests for Target search functionality

  Scenario: User can search for a product on Target
    Given Open target main page
    When Search for a product
    Then Verify search results are shown
