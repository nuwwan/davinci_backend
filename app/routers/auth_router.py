from app.schema.user_schema import UserCreate, UserLogin
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.auth_controller import create_auth_controller, authenticate_user,activate_user_email,verify_user_email_request

router=APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",status_code=201)
def register_user(user:UserCreate,db:Session=Depends(get_db)):
    return create_auth_controller(user,db)

@router.post("/login",status_code=200)
def login_user(user:UserLogin,db:Session=Depends(get_db)):
    return authenticate_user(user,db)

@router.post("/activate",status_code=200)
def request_to_activate_user(email: str, db: Session = Depends(get_db)):
    return verify_user_email_request(email, db)

@router.get("/verify-email",status_code=200)
def verify_email(token: str, db: Session = Depends(get_db)):
    return activate_user_email(token, db)