Feature: Login

  @positive @high
  Scenario: TC-001 Log in with valid email and password
    Given A registered user exists
    When Open the login page
    And Enter a valid email and password
    And Click Log in
    Then The My orders page is shown

  @negative @high
  Scenario: TC-002 Reject empty email and password
    When Open the login page
    And Leave both fields empty
    And Click Log in
    Then Both fields show a required-field error

  @boundary @medium
  Scenario: TC-003 Accept a password of exactly 8 characters
    Given User's password is 8 characters long
    When Enter the email
    And Enter the 8-character password
    And Click Log in
    Then Login succeeds

  @boundary @medium
  Scenario: TC-004 Reject a password of 65 characters
    When Enter a valid email
    And Enter a 65-character password
    And Click Log in
    Then A password length error is shown

  @security @high
  Scenario: TC-005 Lock the account after 5 wrong passwords
    Given A registered user exists
    When Enter the email with a wrong password 5 times
    And Enter the correct password
    Then Login is refused and the account stays locked for 15 minutes

  @security @high
  Scenario: TC-006 Use the same error for unknown email and wrong password
    When Log in with an unknown email
    And Log in with a known email and wrong password
    And Compare the messages
    Then Both attempts show the same generic error
