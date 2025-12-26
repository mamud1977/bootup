from fastapi import (
    APIRouter, 
    status, 
    HTTPException, 
    Depends, 
    Request, 
    Form,
    Query
)

from fastapi.staticfiles import StaticFiles

import logging

from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

import sys
import json
from fastapi.responses import HTMLResponse, JSONResponse

from fastapi.templating import Jinja2Templates

from database.connection import get_connection
from sharedlib.util import (
    get_jwt, 
    get_current_user,
    get_user_details_from_cookie
    )

from sharedlib.pydantic import (
    EventStructure, 
    TokenData
)    

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

templates = Jinja2Templates(directory="templates")
# Load profiles from JSON file
with open("settings/event-map.json") as f:
    profiles = json.load(f)["profiles"]
    

router = APIRouter()


# @router.get("/event/get_event_old", tags=['Event'])
# def get_event(request: Request):
#     api_name = "get_event 1"
#     logging.info("I am invoked: {}")
#     return templates.TemplateResponse("event/get_event.html", {"request": request})

# @router.get("/event/get_event/result", tags=['Event'])
# def get_event(request: Request, eventname: str = Query(...)):
    
#     print(f"eventname: {eventname}")

#     try:
#         with get_connection() as conn:   # ensures conn.close() runs automatically
#             cursor = conn.cursor()
#             cursor.execute("SELECT data FROM events WHERE name = ?", (eventname,))
#             row = cursor.fetchone()
#             if not row:
#                 raise HTTPException(status_code=404, detail="Event not found")

#             # Convert JSON string back to Python dict
#             event_structure = json.loads(row[0])
            
#             logger.info(f"event_data: {event_structure}")

#             # Render template with event_data
#             return templates.TemplateResponse(
#                 "event/get_event_success.html",
#                 {"request": request, "eventname": eventname, "event_structure": event_structure}
#             )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/event/get_event", tags=['Event'])
def get_event(request: Request, eventname: Optional[str] = Query(None), current_user: TokenData = Depends(get_current_user)):
    print(f"Hello {current_user}, you are at /event/get_event")
    print(f"current_user: {current_user}")
    
    api_name = "get_event - all in one"
    logging.info("I am invoked: {api_name}")

    event_structure = None
    error_message = None

    if eventname:
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT data FROM events WHERE name = ?", (eventname,))
                row = cursor.fetchone()
            if row:
                event_structure = json.loads(row[0])
            else:
                error_message = f"Event '{eventname}' not found"
        except Exception as e:
            error_message = f"Internal server error: {str(e)}"

    return templates.TemplateResponse(
        "event/get_event_combined.html",
        {
            "request": request, 
            "eventname": eventname, 
            "event_structure": event_structure,
            "error_message": error_message,
            "current_user": current_user
        }
    )


@router.get("/event/create_event", tags=['Event'])
def get_event(request: Request, current_user: TokenData = Depends(get_current_user)):
    print(f"Hello {current_user}, you are at /event/create_event")
    print(f"current_user: {current_user}")
    
    return templates.TemplateResponse(
        "event/create_event.html", 
        {"request": request,
         "current_user": current_user}
        )

@router.post("/event/save_event", tags=['Event'])
async def save_event(events: EventStructure, current_user: TokenData = Depends(get_current_user)):
    print(f"Hello {current_user}, you are at /event/save_event")
    print(f"current_user: {current_user}")
    try:
        print(f"event: {events}")
        data_json = events.json()

        with get_connection() as conn:   # ensures conn.close() runs automatically
            print(f"DB connection got created")
            cursor = conn.cursor()
            cursor.execute(         
                """
                INSERT INTO events (name, data)
                VALUES (?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    data = excluded.data
                """,
                (events.name, data_json)
            )
            
            conn.commit()
            new_id = cursor.lastrowid

            return JSONResponse(content={
            "message": "Event saved successfully",
            })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/event/edit_event", tags=['Event'])
async def edit_event(request: Request, eventname: Optional[str] = Query(None), current_user: TokenData = Depends(get_current_user)):
    print(f"Hello {current_user}, you are at /event/edit_event")
    print(f"current_user: {current_user}")
    print(f"edit_event(eventname): {eventname}")
    try:
        if not eventname:
            # No eventname → just render empty page (search form)
            return templates.TemplateResponse(
                "event/edit_event.html",
                {
                    "request": request, 
                    "event_structure": None,
                    "current_user": current_user
                }
            )        

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM events WHERE name=?", (eventname,))
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Event not found")
            event_structure = json.loads(row[0])

        return templates.TemplateResponse(
            "event/edit_event.html",
            {
                "request": request, 
                "event_structure": event_structure,
                "current_user": current_user
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
