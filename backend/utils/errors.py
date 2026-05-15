from fastapi import HTTPException, status

class AuthError(HTTPException):
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

class AIServiceError(HTTPException):
    def __init__(self, detail: str = "AI service unavailable. Please retry."):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)