Feature: Cart (HW5)
  Scenario: 'Your cart is empty' message is shown
    Given Open Target home (HW5)
    When Click Cart icon (HW5)
    Then Verify 'Your cart is empty' message is shown (HW5)