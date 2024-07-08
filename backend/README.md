# Documentation
## Installation
Fork the represitory from github and enter the parent directory

1 Download dependencies
```bash
pip install -r requirements.txt
```

2 Set environmental variables
Database url:
```bash
setx DATABASE_URL user:yourpassword@database_url:port/dbname
```
Secret key for JWT token generation (use gitbash)
```bash
openssl rand -hex 32
```
Save the generated secret key
```bash
setx SECRET_KEY your secret key here
```
3 Run the project in developement mode
```bash
fastapi dev main.py
```
4 Fast API's built in documetnation can be accessed at the root of the API

## Usage
- **/token:** Login for JWTTokent
- **/register:** Register new user to the database for future login
- **/deleteuser:** Delete the user data of the token owner with the username and password
