from fastapi import FastAPI
from db import SessionLocal
from models import Card


app = FastAPI()


# Health check
@app.get("/")
def home():
    return {"status": "alive"}


# Look up a single card's product ID by its URL path
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


# Batch lookup: accepts a list of URL paths, returns a map of url -> product_id
@app.post("/url_cards")
def get_cards(urls: list[str]):
    session = SessionLocal()
    try:
        # Query all matching cards in one shot
        cards = session.query(Card).filter(Card.url.in_(urls)).all()
        found = {card.url: card.id for card in cards}
        # Return every requested URL, with None for any that weren't found
        return {url: found.get(url, None) for url in urls}
    finally:
        session.close()
