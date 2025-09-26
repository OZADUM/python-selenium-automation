Feature: Add product to cart

  # You can change the product to a simple/cheap item if needed
  @add_to_cart
  Scenario: Add first listed product to cart and verify cart has items
    Given I open the Target homepage
    When I search for "tea"
    And I open the first search result
    And I add the product to the cart
    Then my cart has at least 1 item