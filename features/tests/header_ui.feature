Feature: Tests to verify Header UI elements

  Scenario: Verify header has correct amount of links
    Given Open target main page
    Then Verify header has 6 links

  Scenario: Verify can click on 1st header link
    Given Open target main page
    When Click on 1st header link
    Then Verify Target Circle opens