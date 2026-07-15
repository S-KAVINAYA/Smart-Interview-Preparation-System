from fastapi import HTTPException, status


class EmailAlreadyExistsException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered."
        )


class MobileAlreadyExistsException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Mobile number already registered."
        )


class InvalidCredentialsException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )


class UserNotFoundException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )


class UnauthorizedException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access."
        )

class InvalidOTPException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP."
        )


class ExpiredOTPException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired."
        )

class OTPAlreadyUsedException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has already been used."
        )