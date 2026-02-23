from fastapi import FastAPI
from db import SessionLocal
from models import Card


app = FastAPI()

@app.get("/")
def home():
    return {"status": "alive"}

@app.get("/card/{url:path}")
def get_card(url: str):
    session = SessionLocal()
    try:
        card = session.query(Card).filter(Card.url == url).first()
        if not card:
            return {"error": "Card not found"}
        
        return {id: card.id}
    finally: 
        session.close()

@app.post("/url_cards")
def get_cards(urls: list[str]):
    session = SessionLocal()
    try:
        cards = session.query(Card).filter(Card.url.in_(urls)).all()
        found = {card.url: card.id for card in cards}
        return {url: found.get(url, None) for url in urls}
    finally:
        session.close()