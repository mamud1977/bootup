from fastapi import FastAPI, Request, HTTPException, Depends
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.routers import auth 
from app.routers import user 
from app.routers import event
from app.routers import eventbuilder
from app.routers import test

import os
from app.sharedlib.util import (
    get_jwt, 
    get_current_user, 
    get_user_details_from_cookie
)
   


app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
app.mount( "/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static" )

uploads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads")) 
app.mount("/uploads", StaticFiles(directory=uploads_path), name="uploads")

templates = Jinja2Templates(directory="app/templates")

@app.exception_handler(HTTPException) 
async def http_exception_handler(request: Request, exc: HTTPException): 
    return templates.TemplateResponse( 
        "base.html", 
        { "request": request, 
          "error_message": exc.detail, # populate error section 
          "status_code": exc.status_code, 
          "current_user": None # or decode cookie if you want 
          }, 
          status_code=exc.status_code 
        )


@app.get("/", response_class=HTMLResponse, tags=['Test API '])
async def home(request: Request):
    current_user = get_user_details_from_cookie(request)
    return templates.TemplateResponse("home.html", {"request": request, "current_user": current_user})

@app.get('/home', tags=['Home'])
async def home(request: Request):
    current_user = get_user_details_from_cookie(request)
    return templates.TemplateResponse("home.html", {"request": request, "current_user": current_user})

@app.get('/main', tags=['Home'])
async def home(request: Request):
    current_user = get_user_details_from_cookie(request)
    return templates.TemplateResponse("home.html", {"request": request, "current_user": current_user})

@app.get('/index', tags=['Home'])
async def home(request: Request):
    current_user = get_user_details_from_cookie(request)
    return templates.TemplateResponse("home.html", {"request": request, "current_user": current_user})

@app.get("/about", response_class=HTMLResponse, tags=['Test API '])
async def about(request: Request):
    current_user = get_user_details_from_cookie(request)
    return templates.TemplateResponse("about.html", {"request": request, "current_user": current_user})

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(event.router)
app.include_router(test.router)
app.include_router(eventbuilder.router)

# @app.get('/events')
# def events():
#     return {'Event list':{'event 1','event 2','event 3'}}

# @app.get('/event/{event_id}')
# def property(event_id :str):
#     return f"We display you /event/{event_id}"

# @app.get('/property')
# def property():
#     return 'This is the property page'

# @app.post('/adduser')
# def adduser(profile: userProfile):
    
#     return f"Hello {profile.name}, your profile is {profile}"

# @app.post('/{year}/addevent')
# def addevent(profile: userProfile, year: int, lang: str):
    
#     ret = {
#         "name": profile.name,
#         "year": year,
#         "lang": lang,
#         "profile": profile
#         }
    
#     return ret

# @app.post('/organization')
# def participation(organization: organization):
    
#     ret = {
#         "organization": organization
#         }
    
#     return ret

# @app.post('/participation')
# def participation(profile: userProfile, event: event):
    
#     ret = {
#         "userProfile": profile,
#         "event": event
#         }
    
#     return ret


# @app.post('/fixture')
# def fixture(fixture: fixture):
    
#     ret = {
#         "fixture": fixture
#         }
    
#     return ret








 
# # participants: list[participant] = []

# # @app.post("/participant/add")
# # def participant_add(p: participant):
# #     new_participant = participant(**p.dict())
# #     participants.append(find_participant_id(new_participant))

# #     return participants

# # def find_participant_id(p : participant ):
# #     if len(participants) > 0:
# #         p.id = participants[-1].id + 1
# #     else:
# #         p.id = 1

# #     return p





# # @app.get("/events")
# # def first_api():
# #     events = load_events()
# #     return events

# # # Static Path Parameters
# # @app.get("/events/all")
# # def first_api():
# #     events = load_events()
# #     return events


# # # Dynamic Path Parameters
# # @app.get("/events/{event}")
# # def first_api(event : str):
# #     events = load_events()
# #     for e in events:
# #         if e.get('event-name').casefold() == event.casefold():
# #             return e
# #     raise HTTPException (status_code = 404, detail = "Event not found ...")       

# # # Query Parameters
# # @app.get("/events/")
# # def first_api(event : str):
# #     events = load_events()
# #     for e in events:
# #         if e.get('event-name').casefold() == event.casefold():
# #             return e

# # # Path & Query Parameters
# # @app.get("/events/{event}/")
# # def get_group_from_event(event: str, group: str):
# #     events = load_events()
# #     for evt in events:
# #         if evt["event-name"].lower() == event.lower():
# #             if group:
# #                 for grp in evt["age-groups"]:
# #                     if grp["name"] == group:
# #                         return {
# #                             "event-name": evt["event-name"],
# #                             "group": grp
# #                         }
# #                 return JSONResponse(status_code=404, content={"error": f"Group '{group}' not found in event '{event}'"})
# #             return evt
# #     return JSONResponse(status_code=404, content={"error": f"Event '{event}' not found"})

# # @app.post("/events/create_event")
# # def create_event(new_event = Body()):
# #     events = load_events()
# #     events.append(new_event)
# #     save_events(events)
# #     return {"message": "New event saved", "New event": new_event}

# # @app.put("/events/update_event")
# # def update_event(update_event = Body()):
# #     try:
# #         events = load_events()
# #         updated = False

# #         for i in range(len(events)):
# #             if events[i].get("event-name") == update_event.get("event-name"):
# #                 events[i] = update_event
# #                 updated = True
# #                 break

# #         if updated:
# #             save_events(events)
# #         return {"message": "Update complete", "event": update_event}

            

# #     except Exception as e:
# #         print(e)
# #         return {"error": f"Event '{update_event.get('event-name')}' not found"}
        

# # @app.delete("/events/delete_event/")
# # def delete_event(event :str):
# #     events = load_events()
# #     deleted = False

# #     for i, e in enumerate(events):
# #         if e.get("event-name") == event:
# #             del events[i]
# #             deleted = True
# #             break  # Stop after deleting one match

# #     if deleted:
# #         save_events(events)
# #         return {"message": f"Event '{event}' deleted successfully"}
# #     else:
# #         return {"error": f"Event '{event}' not found"}




# # @app.post("/participant/insert")
# # def add_participant(body : participant = Body()):
# #     try:
# #         conn = get_connection()
# #         cursor = conn.cursor()
# #         cursor.execute(
# #             "INSERT INTO participants (name, mobileNo, age) VALUES (?, ?, ?)",
# #             (body.name, body.mobileNo, body.age)
# #         )
# #         conn.commit()
# #         new_id = cursor.lastrowid
# #         return {"message": f"{body}' data successfully inserted"}
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))
# #     finally:
# #         conn.close()

# # @app.get("/participant/select")
# # def select_participants():
# #     try:
        
# #         conn = get_connection()
# #         cursor = conn.cursor()
# #         cursor.execute("SELECT id, name, mobileNo, age FROM participants")
# #         rows = cursor.fetchall()
# #         #return {"message": f"{rows}"}
# #         return [participant(**dict(row)) for row in rows]
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))
# #     finally:
# #         conn.close()