Feature: Target Help - Dropdown navigation (HW9)

  @hw9 @help
  Scenario Outline: Select a help topic and verify navigation via URL
    Given Open Help page (default Returns & Exchanges)
    When I choose "<topic>" in the Help topics dropdown
    Then The Help URL contains "<url_fragment>"

    Examples:
      | topic               | url_fragment                         |
      | Returns             | childcat=Returns                     |
      | Returns & Exchanges | parentcat=Returns+%26+Exchanges      |