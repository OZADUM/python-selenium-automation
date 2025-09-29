Feature: PDP color selection (HW5)
  Scenario: Click each color and verify selection
    Given I open the product page "https://www.target.com/p/A-90982184" (HW5)
    When I click each available color (HW5)
    Then All colors were selectable (HW5)