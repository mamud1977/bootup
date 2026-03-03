from sqlalchemy import Column, Integer, String
from db.database import Base

class org(Base):
    __tablename__ = 'organization'
    orgId = Column(Integer, primary_key=True, index= True) 
    orgName = Column(String)
    contactName = Column(String)
    
    


    