Feature: Search results contain required data (HW5)
  Scenario: Validate each result has a name and image
    Given Open Target home (HW5)
    When I search for "tea" (HW5)
    Then Every product has a name and image (HW5)