import json
import os
from jose import jwt, JWSError, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from app.sharedlib.pydantic import Token, TokenData
from typing import Optional





EVENTS_PATH = os.path.join("Data", "events.json")

def load_events():
    if os.path.exists(EVENTS_PATH):
        with open(EVENTS_PATH, "r") as f:
            return json.load(f)
    return []

def save_events(events):
    with open(EVENTS_PATH, "w") as f:
        json.dump(events, f, indent=4)
        
# Run below command
# $ openssl rand -hex 32
SECRET_KEY = "0f393ba18b31bdc9e83a3538fa4b68ef5725345d398d1cacf7365f42748a83d3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUES = 60 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_jwt(data: dict):
    try:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUES)
        to_encode.update({"exp":expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWSError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# # Below one is strict API driven implementation
# def get_current_user(token:str = Depends(oauth2_scheme)):
#     cred_exception = HTTPException(
#         status_code = status.HTTP_401_UNAUTHORIZED,
#         detail = "Invalid auth credentials",
#         headers = {'WWW-Authenticate': "Bearer"}  
#         )
#     try:
#        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#        username:str = payload.get('sub')
#        if username is None:
#            raise cred_exception
#        token_data = TokenData(username = username)
       
#     except JWSError:
#         raise cred_exception
    
#     except ExpiredSignatureError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token has expired",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     except JWSError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

# # Reads the JWT token from  Authorization header
# def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
        
#         if username is None:
#             return RedirectResponse(url=f"/auth/login?next={request.url.path}")
#         return TokenData(username=username)
    
#     except ExpiredSignatureError:
#         # Token expired → return None
#         #return None
#         return RedirectResponse(url=f"/auth/login?next={request.url.path}")
#     except JWTError:
#         # Invalid token → return None
#         #return None
#         return RedirectResponse(url=f"/auth/login?next={request.url.path}")

# Cookie‑based version

async def get_current_user(request: Request) -> TokenData:
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        
        return TokenData(username=username)
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def get_user_details_from_cookie(request: Request) -> Optional[TokenData]:
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        return TokenData(username=username)
    
    except JWTError:
        return None