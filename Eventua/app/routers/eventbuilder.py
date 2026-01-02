from fastapi import (
    APIRouter, 
    status, 
    HTTPException, 
    Depends, 
    Request, 
    Form,
    Query,
    File, 
    UploadFile
)

import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer

from pydantic import ValidationError
from datetime import datetime, timezone

import sys
import json
import logging
from typing import Optional

from app.database.connection import get_connection
from app.sharedlib.util import (
    get_jwt, 
    get_current_user,
    get_user_details_from_cookie
    )


from app.sharedlib.pydantic import (
    EventStructure, 
    TokenData
)    


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

templates = Jinja2Templates(directory="app/templates")
   
router = APIRouter()


from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
import json

router = APIRouter()

@router.get("/eventbuilder/create_event", tags=['Event Builder'])
async def create_event(request: Request, current_user: TokenData = Depends(get_current_user)):

    return templates.TemplateResponse(
        "eventbuilder/create_event.jinja", 
        {
            "request": request, 
            "form_data": {},
            "message": None,
            "status": None,
            "current_user": current_user
        }
    )

@router.get("/eventbuilder/edit_event", tags=['Event Builder'])
async def create_event(request: Request, current_user: TokenData = Depends(get_current_user)):

    return templates.TemplateResponse(
        "eventbuilder/edit_event.jinja", 
        {
            "request": request, 
            "form_data": {},
            "message": None,
            "status": None,
            "current_user": current_user
        }
    )


@router.get("/eventbuilder/user_events", tags=["Event Builder"])
async def get_user_events(current_user: TokenData = Depends(get_current_user)):
    """
    Returns a list of all events created by the current user
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT eventYear, eventName
                FROM events
                WHERE created_by = ?
                ORDER BY eventYear DESC
                """,
                (current_user.username,)
            )
            rows = cursor.fetchall()

        events = [{"eventYear": r[0], "eventName": r[1]} for r in rows]
        return events

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Fetch single event details for edit
@router.get("/eventbuilder/get_event", tags=["Event Builder"])
async def get_event(eventName: str, current_user: TokenData = Depends(get_current_user)):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT eventName, eventYear, eventCountry, eventArea, eventAreaPin, eventStruct,
                       storageType, storageKey
                FROM events
                WHERE eventName = ? AND created_by = ?
                """,
                (eventName, current_user.username)
            )
            row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Event not found")
        event = {
            "eventName": row[0],
            "eventYear": row[1],
            "eventCountry": row[2],
            "eventArea": row[3],
            "eventAreaPin": row[4],
            "eventStruct": json.loads(row[5]) if row[5] else [],
            "storageType": row[6],
            "storageKey": row[7],
        }
        return event
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/eventbuilder/save_event", tags=["Event Builder"])
async def save_event(
    eventName: str = Form(...),
    eventYear: Optional[int] = Form(None),
    eventCountry: Optional[str] = Form(None),
    eventArea: Optional[str] = Form(None),
    eventAreaPin: Optional[int] = Form(None),
    eventStruct: Optional[str] = Form(None),
    eventLeaflet: Optional[UploadFile] = File(None),   
    current_user: TokenData = Depends(get_current_user)
    ):
    

    try:
        # Parse event structure JSON string into Python list
        try:
            event_struct_list = json.loads(eventStruct) if eventStruct else []
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid event structure JSON")


        # Handle file upload 
        storageType, storageKey = None, None 
        if eventLeaflet: # Decide storage type automatically 
            storageType = "local" # or "s3"/"gcs" if using cloud 
            
            # Use filename as storage key 
            storageKey = eventLeaflet.filename 
            
            # Save file locally 
            upload_folder = "uploads" 
            user_folder = os.path.join(upload_folder, current_user.username) 
            year_folder = os.path.join(user_folder, str(eventYear or "unknown_year")) 
            event_folder = os.path.join(year_folder, eventName.replace(" ", "_"))
            
            os.makedirs(event_folder, exist_ok=True) 
            
            # Remove any existing files in this event folder 
            for old_file in os.listdir(event_folder): 
                os.remove(os.path.join(event_folder, old_file))
            
            # Define storage key (relative) and path (absolute) 
            storageKey = os.path.join(current_user.username, 
                                      str(eventYear or "unknown_year"), 
                                      eventName.replace(" ", "_"), 
                                      eventLeaflet.filename) 
            
            storagePath = os.path.join(upload_folder, storageKey) 
            
            # Save file 
            with open(storagePath, "wb") as f: 
                  f.write(await eventLeaflet.read())
            
            storageType = "local"


        try:
            validated = EventStructure(
                eventName=eventName,
                eventYear=eventYear,
                eventCountry=eventCountry,
                eventArea=eventArea,
                eventAreaPin=eventAreaPin,
                eventStruct=event_struct_list,
                storageType=storageType,
                storageKey=storageKey,
            )
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())


        # Save to database
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
            """
            INSERT INTO events (
                eventName, eventYear, eventCountry, eventArea, eventAreaPin,
                eventStruct, storageType, storageKey,
                created_by, created_dt
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(eventName, created_by) DO UPDATE SET
                eventYear    = excluded.eventYear,
                eventCountry = excluded.eventCountry,
                eventArea    = excluded.eventArea,
                eventAreaPin = excluded.eventAreaPin,
                eventStruct  = excluded.eventStruct,
                storageType  = excluded.storageType,
                storageKey   = excluded.storageKey,
                created_dt   = excluded.created_dt
            """,
            (
                eventName,
                eventYear,
                eventCountry,
                eventArea,
                eventAreaPin,
                json.dumps(event_struct_list),
                storageType,
                storageKey,
                current_user.username,                  
                datetime.now(timezone.utc).isoformat()
            ))

        conn.commit()

        return JSONResponse(content={"message": "Event saved successfully"})

    except HTTPException:
        raise  # re-raise HTTPExceptions (e.g., invalid JSON)
    except Exception as e:
        # Optional: log error in production
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")    

