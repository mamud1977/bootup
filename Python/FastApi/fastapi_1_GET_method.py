from fastapi import FastAPI
from enum import Enum
from typing import Optional




app = FastAPI()

@app.get('/')
def index():
    return "Hello World ..."

@app.get('/blog/all')
def get_blogs_all():
    return {'message' : f"All blogs provided"} 

@app.get('/blog/page')
def get_blogs_by_page(page = 1 ,page_size: Optional[int]= None):
    return {'message' : f"page = {page}, page_size = {page_size}"} 

@app.get('/blog/{id}')
def get_blogs_by_id(id: int):
    return {'message' : f"We intended to retrieve the blog with id = {id}"} 

class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@app.get('/blog/type/{type}')
def get_blogs_by_type(type: BlogType):
    return {'message' : f"Blog type {type}"} 

