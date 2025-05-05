from datetime import timedelta

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

import auth_utils
from models import User, InputUser
from controller import DBConnection
from queries import get_query_get_user_by_email, get_query_insert_user
from config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth")


@router.post("/signup")
async def create_user(user: InputUser) -> User:
    database = DBConnection()
    insert_user_query = get_query_insert_user(
        user.name,
        user.email,
        auth_utils.get_password_hash(user.password.get_secret_value()),
    )

    async with database.pool.acquire() as conn:
        created_user = await conn.fetchrow(insert_user_query)
        if not created_user:
            raise HTTPException(422, "this email is already in use")

    print(created_user["password"])

    return User(**created_user)


@router.post("/login")
async def user_login(
    login_attempt_data: OAuth2PasswordRequestForm = Depends(),
):
    database = DBConnection()
    get_user_query = get_query_get_user_by_email(login_attempt_data.username)
    async with database.pool.acquire() as conn:
        user_record = await conn.fetchrow(get_user_query)
        if not user_record:
            raise HTTPException(401, "user not found")

    print(auth_utils.get_password_hash(login_attempt_data.password))
    print(user_record["password"])

    if not auth_utils.verify_password(
        login_attempt_data.password, user_record["password"]
    ):
        raise HTTPException(401, "wrong password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": login_attempt_data.username},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
