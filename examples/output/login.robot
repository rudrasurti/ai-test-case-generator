*** Settings ***
Documentation    Generated test cases for Login.
...              Implement each keyword, then remove the TODO tag.

*** Test Cases ***
TC-001 Log in with valid email and password
    [Tags]    positive    high    TODO
    [Documentation]    Expected: The My orders page is shown
    Open The Login Page
    Enter A Valid Email And Password
    Click Log In

TC-002 Reject empty email and password
    [Tags]    negative    high    TODO
    [Documentation]    Expected: Both fields show a required-field error
    Open The Login Page
    Leave Both Fields Empty
    Click Log In

TC-003 Accept a password of exactly 8 characters
    [Tags]    boundary    medium    TODO
    [Documentation]    Expected: Login succeeds
    Enter The Email
    Enter The 8Character Password
    Click Log In

TC-004 Reject a password of 65 characters
    [Tags]    boundary    medium    TODO
    [Documentation]    Expected: A password length error is shown
    Enter A Valid Email
    Enter A 65Character Password
    Click Log In

TC-005 Lock the account after 5 wrong passwords
    [Tags]    security    high    TODO
    [Documentation]    Expected: Login is refused and the account stays locked for 15 minutes
    Enter The Email With A Wrong Password 5 Times
    Enter The Correct Password

TC-006 Use the same error for unknown email and wrong password
    [Tags]    security    high    TODO
    [Documentation]    Expected: Both attempts show the same generic error
    Log In With An Unknown Email
    Log In With A Known Email And Wrong Password
    Compare The Messages

*** Keywords ***
Open The Login Page
    Fail    Not implemented: Open the login page

Enter A Valid Email And Password
    Fail    Not implemented: Enter a valid email and password

Click Log In
    Fail    Not implemented: Click Log in

Leave Both Fields Empty
    Fail    Not implemented: Leave both fields empty

Enter The Email
    Fail    Not implemented: Enter the email

Enter The 8Character Password
    Fail    Not implemented: Enter the 8-character password

Enter A Valid Email
    Fail    Not implemented: Enter a valid email

Enter A 65Character Password
    Fail    Not implemented: Enter a 65-character password

Enter The Email With A Wrong Password 5 Times
    Fail    Not implemented: Enter the email with a wrong password 5 times

Enter The Correct Password
    Fail    Not implemented: Enter the correct password

Log In With An Unknown Email
    Fail    Not implemented: Log in with an unknown email

Log In With A Known Email And Wrong Password
    Fail    Not implemented: Log in with a known email and wrong password

Compare The Messages
    Fail    Not implemented: Compare the messages
