from fastapi import FastAPI,requests,Body,Form,UploadFile,File
from pydantic import BaseModel

app=FastAPI()

class Item(BaseModel):
    name:str
    price:float
    in_stocks:bool

@app.post("/json")
def receive_json(item:Item):
    return{
        "type":"json",
        "name":item.name,
        "price":item.price,
        "instock" : item.in_stocks
    }

@app.post("/text")
def receive_txt(content: str= Body(...,media_type="text/plain")):
    return{
        "type":"Plain Text",
        "content":content
    }

@app.post("/form")
def receive_form(username:str=Form(...),password:str=Form(...)):
    return{
        "type":"Form",
        "username":username,
        "password":password
    }

@app.post("/upload")
def upload_file(file: UploadFile=File(...)):
    return{
        "type":"UploadFile",
        "Filename":file.filename,
        "file_type":file.content_type
    }