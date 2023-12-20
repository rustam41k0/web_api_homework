from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from starlette.websockets import WebSocket, WebSocketDisconnect

from models import Book, Film
from config import SessionLocal, engine
from sqlalchemy import event
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()

    @event.listens_for(db, 'before_commit')
    def receive_before_commit(db):
        print("Database has changed")

    try:
        yield db
    finally:
        db.close()


@app.get("/book")
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    return {
        'book_id': book.id,
        'book_name': book.name,
        'book_author': book.author
    }


@app.post("/book/create")
async def create_book_service(name: str, author: str, db: Session = Depends(get_db)):
    book = Book(name=name, author=author)
    db.add(book)
    db.commit()
    db.refresh(book)
    return f'Книга {book.id} {book.name} успешно добавлена'


@app.patch("/book/update")
async def update_book(book_id: int, name: str, author: str, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    book.name = name
    book.author = author
    db.commit()

    db.refresh(book)
    return f'Книга {book.id} {book.name} успешно обновлена'


@app.delete("/book/delete")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    db.delete(book)
    db.commit()
    return f'Книга {book.id} {book.name} удалена'


@app.get("/film")
async def get_film(film_id: int, db: Session = Depends(get_db)):
    film = db.query(Film).filter(Film.id == film_id).first()
    return {
        'film_id': film.id,
        'film_title': film.title,
        'film_rating': film.rating
    }


@app.post("/film/create")
async def create_film(title: str, rating: int, db: Session = Depends(get_db)):
    film = Film(title=title, rating=rating)
    db.add(film)
    db.commit()
    db.refresh(film)
    return f'Фильм {film.id} {film.title} успешно добавлен'


@app.patch("/film/update")
async def update_film(film_id: int, title: str, rating: int, db: Session = Depends(get_db)):
    film = db.query(Film).filter(Film.id == film_id).first()
    film.title = title
    film.rating = rating
    db.commit()
    db.refresh(film)
    return f'Фильм {film.id} {film.title} успешно обновлен'


@app.delete("/film/delete")
async def delete_film(film_id: int, db: Session = Depends(get_db)):
    film = db.query(Film).filter(Film.id == film_id).first()
    db.delete(film)
    db.commit()
    return f'Фильм {film.id} {film.title} удален'


templates = Jinja2Templates(directory="templates")


@app.get("/chat")
async def get(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Сообщение: {data}")

