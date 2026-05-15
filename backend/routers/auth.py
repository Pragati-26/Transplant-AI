from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from ..database import get_db
from ..models import User
from ..schemas import UserRegister, UserOut, Token
from ..dependencies import create_access_token, get_current_user
from ..utils.errors import AuthError, ValidationError

router      = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise ValidationError("Email already registered")
    if db.query(User).filter(User.username == payload.username).first():
        raise ValidationError("Username already taken")

    user = User(
        email           = payload.email,
        username        = payload.username,
        hashed_password = pwd_context.hash(payload.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db:   Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not pwd_context.verify(form.password, user.hashed_password):
        raise AuthError("Invalid username or password")
    if not user.is_active:
        raise AuthError("Account is deactivated")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user