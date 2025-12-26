from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List

from FastApi.sharedlib.pydantic_models import (
            participant, 
            userProfile, 
            event, 
            fixture, 
            organization,
            organizationDisplay
            )

from db import models
from db.database import engine, Base, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@app.get('/getorgs', response_model = List[organizationDisplay])
def getorg(db: Session = Depends(get_db)):
    orgs = db.query(models.org).all()
    return orgs

@app.get('/getorgs/{orgId}')
def getorg(orgId: int , db: Session = Depends(get_db) ):
    orgs = db.query(models.org).filter(models.org.orgId == orgId).all()
    return orgs

@app.delete('/orgs/{orgId}')
def deleteorg(orgId: int , db: Session = Depends(get_db) ):
    db.query(models.org).filter(models.org.orgId == orgId).delete(synchronize_session=False)
    db.commit()
    return {'entry deleted'}

@app.put('/orgs/{orgId}')
def updateorg(orgId: int, req:organization, db: Session = Depends(get_db)):
    orgs = db.query(models.org).filter(models.org.orgId == orgId)
    if not orgs.first():
        pass
    orgs.update(req.dict())
    db.commit()
    return {'updated'}

@app.post('/addorg')
def addorg(req:organization, db: Session = Depends(get_db)):
    new_org = models.org(orgName = req.orgName, contactName = req.contactName)
    db.add(new_org)
    db.commit()
    db.refresh(new_org)

    return req

