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

from database.connection import get_connection
from sharedlib.util import get_jwt, get_current_user, get_user_details_from_cookie
from sharedlib.pydantic import (
    TokenData, 
    Token,
    UserLogin,
    UserDetail
)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/auth/login", response_class=HTMLResponse, tags=['Auth'])
def login(request: Request, current_user: Optional[TokenData] = Depends(get_user_details_from_cookie)):
    return templates.TemplateResponse(
        "auth/login.jinja", 
        {
            "request": request,
            "form_data": {},
            "message": None,
            "status": "",
            "current_user": current_user
        }
        )

@router.post('/auth/login', tags=['Auth'] )
async def login(request: Request):
#def login(request: pydantic.user):
#def login(request: OAuth2PasswordRequestForm = Depends()):

    # Step 1: Read form data
    
    form = await request.form()
    form_data = dict(form)
    print(f"form_data: {form_data}")
        
 
    try:
        # ✅ Validate using Pydantic
        userData = UserLogin(**form_data)
        
        p_username = userData.username
        p_password = userData.password
        
        # Decide query based on type
        if p_username.isdigit():
            query = "SELECT id, phone, password FROM user WHERE phone = ?"
        else:
            query = "SELECT id, email, password FROM user WHERE email = ?"
                   
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, (p_username,))
            row = cur.fetchone()
            
        if not row:
            return templates.TemplateResponse(
                "auth/login.jinja", 
                {
                    "request": request, 
                    "form_data": form_data,
                    "message": "Invalid username",
                    "status": "error",
                    "current_user": None
                }
            )

        if not pwd_context.verify(p_password, row["password"]):
            return templates.TemplateResponse(
                "auth/login.jinja", 
                {
                    "request": request, 
                    "form_data": form_data,
                    "message": "Invalid password",
                    "status": "error",
                    "current_user": None
                }
            )
              
        access_token = get_jwt(data = {"sub": p_username})
        print(f"Token: {access_token}")

        # check if "next" was passed in form (default to home or event page)
        next_page = form_data.get("next") or "/"
        response = RedirectResponse(url=next_page, status_code=302)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,   # safer, prevents JS access
            secure=False,    # set True if HTTPS
            samesite="lax"
        )

        return response
  
    except ValidationError as e:
        error_msg = [err["msg"] for err in e.errors()]
        return templates.TemplateResponse(
            "auth/login.jinja", 
            {
                "request": request,
                "form_data": form_data,
                "message": error_msg,
                "status": "error",
                "current_user": None
            }
        )

@router.get("/auth/logout")
def logout(request: Request):
    response = templates.TemplateResponse(
        "base.html",
        {"request": request, "message": "You have successfully logged out"}
    )
    response.delete_cookie("access_token")
    return response


@router.get("/auth/adduser", tags=['Auth'], response_class=HTMLResponse)
async def login(request: Request, current_user: TokenData = Depends(get_current_user)):
    return templates.TemplateResponse(
            "auth/adduser.jinja",
            {
                "request": request,
                "form_data": {},   # ✅ empty dict so Jinja has something
                "message": "",
                "status": "",
                "current_user": current_user
            }
        )

@router.post('/auth/adduser', tags=['Auth'])
async def adduser(request: Request, current_user: TokenData = Depends(get_current_user)):
    # Extract form data
    form = await request.form()
    form_data = dict(form)  # {"name": "...", "phone": "...", ...}
    
    print(f"current_user: {current_user}")

    try:
        # ✅ Validate using Pydantic
        userData = UserDetail(**form_data)

        print("Validated user input:", userData)
        
        hashed_pwd = pwd_context.hash(userData.password)        

        with get_connection() as conn:   # ensures conn.close() runs automatically
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO user 
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
            "auth/adduser.jinja",
            {
                "request": request,
                "form_data": form_data,
                "message": "Saved successfully",
                "status": "success",
                "current_user": current_user
            }
        )

    except ValidationError as ve:
        # ✅ Extract first validation error message
        print('Exception 1 raised')
        error_msg = ve.errors()[0]["msg"]

        return templates.TemplateResponse(
            "auth/adduser.jinja",
            {
                "request": request,
                "form_data": form_data,
                "message": error_msg,
                "status": "error",
                "current_user": current_user
            }
        )

    except Exception as e:
        # ✅ Unexpected errors
        print('Exception 2 raised')
        return templates.TemplateResponse(
            "auth/adduser.jinja",
            {
                "request": request,
                "form_data": form_data,
                "message": f"Internal server error: {str(e)}",
                "status": "error",
                "current_user": current_user
            }
        )
