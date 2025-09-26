Feature: Target product search (parameterized)

  # Scenario Outline demonstrates Behave variables for the search term
  @search
  Scenario Outline: User can search for a product on Target with a variable
    Given I open the Target homepage
    When I search for "<term>"
    Then I see results for "<term>"

    Examples:
      | term      |
      | tea       |
      | coffee    |
      | headphones|