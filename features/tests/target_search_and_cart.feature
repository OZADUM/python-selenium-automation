Feature: Target search and cart

  Scenario: User can search for a product on Target
    Given Open target main page
    When Search for a product
    Then Verify search results are shown

  Scenario: 'Your cart is empty' message is shown for empty cart
    Given Open target main page
    When Click on Cart icon
    Then Verify 'Your cart is empty' message is shown
