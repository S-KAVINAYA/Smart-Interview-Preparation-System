import random
import secrets
import string


def generate_otp(length: int = 6):

    return "".join(
        random.choices(
            string.digits,
            k=length
        )
    )


def generate_secure_token(length: int = 32):

    return secrets.token_urlsafe(length)