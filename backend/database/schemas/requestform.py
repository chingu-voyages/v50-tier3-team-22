from fastapi import Form

class OAuth2CustomPasswordRequestForm:
    def __init__(
        self,
        email: str = Form(),
        password: str = Form(),
    ):
        self.email = email
        self.password = password
    