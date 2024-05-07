# FastAPI로 백엔드 서버 만들기 
from fastapi import FastAPI, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3 

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()


app = FastAPI()

#post라는 메소드로 /items 경로로 보냄
@app.post('/items')

#create_item라는 함수는 이런 이런 데이터를 받을 것이다. 
async def create_item(image:UploadFile, 
                title:Annotated[str,Form()], 
                price:Annotated[int,Form()], 
                description:Annotated[str,Form()], 
                place:Annotated[str,Form()]):
    #image 읽을시간
    image_bytes = await image.read()
    cur.execute(f"""
                 INSERT INTO items(title, image, price, description, place)
                 VALUES ('{title}', '{image_bytes.hex()}', {price},'{description}', '{place}')
                 """)
    con.commit()
    return '200'
 
#FastAPI static files에서 복붙
#frontend 폴더 별도들고 HTML, CSS 소스 담기
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
