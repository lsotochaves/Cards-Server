import requests
from db import SessionLocal
from models import Card

def sync():
    print("Fetching pricelist...")
    data = requests.get("https://api.cardkingdom.com/api/v2/pricelist").json()["data"]
    print(f"Got {len(data)} cards.")

    session = SessionLocal()

    try:
        session.query(Card).delete()

        cards = []
        for item in data:
            cv = item.get("condition_values", {})
            cards.append(Card(
                id=item["id"],
                url=item["url"],
                nm_price=cv.get("nm_price"),
                nm_qty=cv.get("nm_qty", 0),
                ex_price=cv.get("ex_price"),
                ex_qty=cv.get("ex_qty", 0),
                vg_price=cv.get("vg_price"),
                vg_qty=cv.get("vg_qty", 0),
                g_price=cv.get("g_price"),
                g_qty=cv.get("g_qty", 0),
            ))

        session.add_all(cards)
        session.commit()
        print(f"Saved {len(cards)} cards to database.")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    sync()