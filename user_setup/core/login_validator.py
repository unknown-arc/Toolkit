import re

class Validator:
    EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    PASSWORD_REGEX = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

    @staticmethod
    def is_valid_email(email: str) -> bool:
        return re.match(Validator.EMAIL_REGEX, email) is not None

    @staticmethod
    def is_valid_password(password: str) -> bool:
        return re.match(Validator.PASSWORD_REGEX, password) is not None
