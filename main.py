# FastAPI로 백엔드 서버 만들기 
# from 모듈이름 import 기능 또는 변수
from fastapi import FastAPI, UploadFile, Form, Response, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
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

#어떻게 인코딩할지 정하기
SECRET = "super-coding"  #secret키 
manager = LoginManager(SECRET, '/login') #/login에서 token 발급

@manager.user_loader()
def query_user(data):
    WHERE_STATEMENTS = f'id = "{data}"'
    if type(data) == dict:
        WHERE_STATEMENTS = f'''id="{data['id']}"'''
    con.row_factory = sqlite3.Row 
    cur = con.cursor()
    user = cur.execute(f"""
                       SELECT * from users WHERE {WHERE_STATEMENTS}
                       """).fetchone()
    return user

@app.post('/login')                         #프론트에서 유저 id, password 받아옴
def login(id:Annotated[str,Form()], 
            password:Annotated[str,Form()]):
    user = query_user(id)
    if not user:                            #존재하는 유저인지 판단
        raise InvalidCredentialsException   #에러메시지 띄우기: 유저가 없거나, 
    elif password != user['password']:      #에러메시지 띄우기: 비번이 틀리거나 
        raise InvalidCredentialsException
    
    #access token에 담을 데이터를 설정하고, token을 만듬
    access_token = manager.create_access_token(data={
        'sub':{
            'id': user['id'],
            'name': user['name'],
            'email':user['email']
    }
    })
    
    #만든 access token을 응답
    return {'access_token': access_token}

#signup API로 요청 데이터를 보내기 때문에, post로 받음.  
@app.post('/signup')
def signup(id:Annotated[str,Form()], 
           password:Annotated[str,Form()],
           name:Annotated[str,Form()],
           email:Annotated[str,Form()]):
    ## DB에 회원정보 저장
    cur.execute(f"""
                INSERT INTO users(id,name,email,password)
                VALUES ('{id}', '{name}', '{email}', '{password}')
                """)
    con.commit() ## DB에 제대로 들어갔는지 확인
    return '200'          #200을 뱉음

#Rest API CRUD의 C/ post-get-put-delete
#post라는 메소드로 /items 경로로 보냄
@app.post('/items')
async def create_item(image:UploadFile,             #create_item라는 함수는 이런 이런 데이터를 받을 것이다. 
                title:Annotated[str,Form()], 
                price:Annotated[int,Form()], 
                description:Annotated[str,Form()], 
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()]
                ):
    
    image_bytes = await image.read()      #image 읽을시간
    cur.execute(f"""
                 INSERT INTO items(title, image, price, description, place, insertAt)
                 VALUES ('{title}', '{image_bytes.hex()}', {price},'{description}', '{place}', {insertAt})
                 """)
    con.commit()
    return '200'

#Rest API CRUD의 R/ post-get-put-delete
#로그인1: 유저가 인증된 상태
@app.get('/items')
async def get_items(user=Depends(manager)):
    con.row_factory = sqlite3.Row     #컬럼명도 같이 불러옴
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
