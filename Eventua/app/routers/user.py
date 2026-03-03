from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends, 
    Request, 
    status,
    Form
)

from fastapi.security import (
    OAuth2PasswordRequestForm, 
    OAuth2PasswordBearer
)

from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse

import json
from fastapi.staticfiles import StaticFiles

from typing import Optional

from starlette.responses import HTMLResponse 
from pydantic import ValidationError, EmailStr

from app.database.connection import get_connection
from app.sharedlib.util import get_jwt, get_current_user, get_user_details_from_cookie
from app.sharedlib.pydantic import (
    TokenData, 
    Token,
    UserLogin,
    UserDetail
)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/user/adduser", tags=['User'], response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
            "user/adduser.jinja",
            {
                "request": request,
                "form_data": {},   # ✅ empty dict so Jinja has something
                "message": "",
                "status": "",
                "current_user": ""
            }
        )

@router.post('/user/adduser', tags=['User'])
async def adduser(request: Request):
    # Extract form data
    form = await request.form()
    form_data = dict(form)  # {"name": "...", "phone": "...", ...}
    
    try:
        # ✅ Validate using Pydantic
        userData = UserDetail(**form_data)

        print("Validated user input:", userData)
        
        hashed_pwd = pwd_context.hash(userData.password)        

        with get_connection() as conn:   # ensures conn.close() runs automatically
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users 
                    (fullname, phone, usertype, dob, email, password) 
                    VALUES (?,?,?,?,?,?)
                ON CONFLICT(email) DO UPDATE SET
                    fullname = excluded.fullname,
                    phone    = excluded.phone,
                    usertype = excluded.usertype,
                    dob      = excluded.dob,
                    password = excluded.password
                    """,
                (   
                    userData.fullname,
                    userData.phone,
                    userData.usertype,
                    userData.dob,
                    userData.email,
                    hashed_pwd,        
                )
            )
            conn.commit()
            print(f"cursor.lastrowid: {cursor.lastrowid}")

        # ✅ Return success message to template
        return templates.TemplateResponse(
            "user/adduser.jinja",
            {
                "request": request,
                "form_data": form_data,
                "message": "Saved successfully",
                "status": "success",
                "current_user": ""
            }
        )

    except ValidationError as ve:
        # ✅ Extract first validation error message
        print('Exception 1 raised')
        error_msg = ve.errors()[0]["msg"]

        return templates.TemplateResponse(
            "user/adduser.jinja",
            {
                "request": request,
                "form_data": form_data,
                "message": error_msg,
                "status": "error",
                "current_user": ""
            }
        )

    except Exception as e:
        # ✅ Unexpected errors
        print('Exception 2 raised')
        return templates.TemplateResponse(
            "user/adduser.jinja",
            {
                "request": request,
                "form_data": form_data,
                "message": f"Internal server error: {str(e)}",
                "status": "error",
                "current_user": ""
            }
        )
