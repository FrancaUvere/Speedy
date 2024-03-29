# SPEEDY

> Speedy is an online banking system, a straight forward digital service offering the fundamental financial services, that allows customers to perform various banking transactions and manage their accounts over the internet using a secure website.

# ROUTES

| API Method | Route         | Authenticated | Roles Permitted | Description  |
| ---------- |:-------------:| -------------:| --------------- |:------------:|
| POST       | /signup | No            | User            | Register a new user with an email and password.|
| POST       | /login    | No            | User            | Authenticate a user   |
| GET        | /logout   | Yes           | User            | Log out the user      |
| POST       |  /<username>/create_account   | Yes           | User            | Create a new bank account for a user.    |
| GET        | /<username>/transactions/  | Yes           | User            | Retrieve the list of transactions the user made.  |
| POST        | /<username>/add_address  | Yes           | User            | Sets address of the user.  |
| POST        | /<username>/home  | Yes           | User            | Home page of the user |
| POST        | /<username>/profile/edit_profile/ | Yes           | User            | Edit profile information of the user |
| GET        | /<username>/transfer | Yes           | User            | Make an Inter bank or Intra bank transfer  |
| GET        | /<username>/accounts  | Yes           | Admin            | Returns a list of accounts owned by the user |
| POST        | /<username>/accounts/<id>  | Yes           | Admin            | Creates an account with the specific ID. |
| GET        | /<username>/services | Yes           | Admin            | Lists the services rendered by the bank. |
| POST        | /<username>/profile/manage_accounts  | Yes           | Admin            | Manages the list of accounts owned by a specific user. |
| GET        | /<username>/profile/manage_accounts/close_account  | Yes           | Admin            | Close a specific account. |
| GET        | /<username>/profile/manage_user_account/delete_account  | Yes           | Admin            | Delete a specific account |