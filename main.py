# FastAPI로 백엔드 서버 만들기 
# from 모듈이름 import 기능 또는 변수
from fastapi import FastAPI, UploadFile, Form, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3 

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

#백엔드에 컬럼생성하는 SQL 코드 삽입
#IF NOT EXISTS -> 테이블이 없을 때만 생성되도록
cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items(   
	            id INTEGER PRIMARY KEY,
	            title INTEGER NO NULL,
	            image BLOB,
	            price INTEGER NOT NULL,
	            description TEXT,
	            place TEXT NOT NULL,
	            insertAt INTEGER NOT NULL
            );      
            """)

app = FastAPI()

#Rest API CRUD의 C/ post-get-put-delete
#post라는 메소드로 /items 경로로 보냄
@app.post('/items')
#create_item라는 함수는 이런 이런 데이터를 받을 것이다. 
async def create_item(image:UploadFile, 
                title:Annotated[str,Form()], 
                price:Annotated[int,Form()], 
                description:Annotated[str,Form()], 
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()]
                ):
    #image 읽을시간
    image_bytes = await image.read()
    cur.execute(f"""
                 INSERT INTO items(title, image, price, description, place, insertAt)
                 VALUES ('{title}', '{image_bytes.hex()}', {price},'{description}', '{place}', {insertAt})
                 """)
    con.commit()
    return '200'

#Rest API CRUD의 R/ post-get-put-delete
@app.get('/items')
async def get_items():
    #컬럼명도 같이 불러옴
    con.row_factory = sqlite3.Row 
    cur = con.cursor()
    rows = cur.execute(f"""
                       SELECT * from items; 
                       """).fetchall()
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))
 
@app.get('/images/{item_id}')
async def get_image(item_id):
     cur = con.cursor()
     image_bytes = cur.execute(f"""
                               SELECT image from items WHERE id = {item_id}
                               """).fetchone()[0]
     return Response(content = bytes.fromhex(image_bytes))
 
#FastAPI static files에서 복붙
#frontend 폴더 별도들고 HTML, CSS 소스 담기
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
