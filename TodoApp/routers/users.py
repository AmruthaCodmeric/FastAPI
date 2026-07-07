from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, Path, Request, Form
from sqlalchemy.orm import Session
from starlette import status
from ..models import Todos, Users
from ..database import  SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="TodoApp/templates")
router = APIRouter(
    prefix='/users',
    tags=['users']
)


def get_db():
    db = SessionLocal()
    try:
       yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency= Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserVerification(BaseModel):
    password:str
    new_password:str = Field(min_length=6)


#page
@router.get("/profile")
async def render_profile_page(request: Request):

    user = await get_current_user(
        request.cookies.get("access_token")
    )

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "request": request,
            "user": user
        }
    )

@router.get("/change-password")
async def render_change_password_page(
        request: Request):

    return templates.TemplateResponse(
        request=request,
        name="change-password.html",
        context={"request": request}
    )
@router.post("/change-password")
async def change_password(
        request: Request,
        db: db_dependency,
        current_password: str = Form(...),
        new_password: str = Form(...)
):

    current_user = await get_current_user(
        request.cookies.get("access_token")
    )

    user = db.query(Users).filter(
        Users.id == current_user.get("id")
    ).first()

    if not bcrypt_context.verify(
            current_password,
            user.hashed_password):
        return templates.TemplateResponse(
            request=request,
            name="change-password.html",
            context={
                "request": request,
                "msg": "Current password is incorrect"
            }
        )

    user.hashed_password = bcrypt_context.hash(
        new_password
    )

    db.commit()

    return templates.TemplateResponse(
        request=request,
        name="change-password.html",
        context={
            "request": request,
            "msg": "Password updated successfully"
        }
    )

#Endpoints
@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=-401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put("/password",status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency,db: db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

@router.put("/phonenumber/{phone_number}",status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency,db: db_dependency,phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number=phone_number
    db.add(user_model)
    db.commit()





