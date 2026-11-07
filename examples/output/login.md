# Test cases: Login

| ID | Title | Type | Priority | Steps | Expected |
|---|---|---|---|---|---|
| TC-001 | Log in with valid email and password | positive | high | 1. Open the login page<br>2. Enter a valid email and password<br>3. Click Log in | The My orders page is shown |
| TC-002 | Reject empty email and password | negative | high | 1. Open the login page<br>2. Leave both fields empty<br>3. Click Log in | Both fields show a required-field error |
| TC-003 | Accept a password of exactly 8 characters | boundary | medium | 1. Enter the email<br>2. Enter the 8-character password<br>3. Click Log in | Login succeeds |
| TC-004 | Reject a password of 65 characters | boundary | medium | 1. Enter a valid email<br>2. Enter a 65-character password<br>3. Click Log in | A password length error is shown |
| TC-005 | Lock the account after 5 wrong passwords | security | high | 1. Enter the email with a wrong password 5 times<br>2. Enter the correct password | Login is refused and the account stays locked for 15 minutes |
| TC-006 | Use the same error for unknown email and wrong password | security | high | 1. Log in with an unknown email<br>2. Log in with a known email and wrong password<br>3. Compare the messages | Both attempts show the same generic error |
