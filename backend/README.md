# Documentation
## Installation
Fork the represitory from github and enter the parent directory

1 Download dependencies
```bash
pip install -r requirements.txt
```
2 Run the project in developement mode
```bash
fastapi dev main.py
```
3 Fast API's built in documetnation can be accessed at the root of the API

## Usage
**/token:** Login for JWTTokent
**/register:** Register new user to the database for future login
**/deleteuser:** Delete the user data of the token owner with the username and password
