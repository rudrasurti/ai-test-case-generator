# User story: Login

As a registered user, I want to log in with my email and password so that I can see my orders.

Acceptance criteria:
- Email and password are required.
- Password must be 8 to 64 characters.
- After 5 wrong passwords in a row the account is locked for 15 minutes.
- On success the user lands on the "My orders" page.
- Error messages must not reveal whether the email exists.
