# Cards-Server

A lightweight FastAPI server that mirrors [Card Kingdom's](https://www.cardkingdom.com/) public pricelist into a local PostgreSQL database and exposes fast lookup endpoints. It serves as the backend for [CK Cart Population](https://github.com/lsotochaves/CK-Cart-Population).

## Why

The original cart-population tool had to visit every card's page in the browser to extract its product ID which was really slow. Cards-Server pulls the entire Card Kingdom catalog once via their public API, stores it locally, and lets the cart tool resolve URLs to product IDs in a single HTTP call.

## Endpoints

**`GET /`** — Health check. Returns `{"status": "alive"}`.

**`GET /card/{url}`** — Look up a single card by its Card Kingdom URL path and get its product ID.

**`POST /url_cards`** — Batch lookup. Accepts a JSON array of URL paths and returns a map of `{ url: product_id }` for each.

## Setup

### Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)
- PostgreSQL

### Installation

```bash
git clone https://github.com/<your-username>/Cards-Server.git
cd Cards-Server
uv sync
```

### Configuration

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/cards_db
```

### Initialize the database

```bash
uv run python init_db.py
```

### Sync the card catalog

This fetches the full pricelist from Card Kingdom's API and populates the database. Run it once initially and periodically to keep prices and stock current.

```bash
uv run python sync_cards.py
```

### Start the server

```bash
uv run uvicorn main:app --reload
```

The server will be available at `http://localhost:8000`.

## Data Model

Each card record stores the following fields synced from Card Kingdom's pricelist API:

| Field | Description |
|-------|-------------|
| `id` | Card Kingdom product ID (primary key) |
| `url` | Card Kingdom URL path |
| `name` | Card name |
| `edition` | Set / edition |
| `variation` | Print variation |
| `is_foil` | Foil indicator |
| `nm_price`, `nm_qty` | Near Mint price and stock |
| `ex_price`, `ex_qty` | Excellent price and stock |
| `vg_price`, `vg_qty` | Very Good price and stock |
| `g_price`, `g_qty` | Good price and stock |

## Project Structure

```
├── main.py           # FastAPI app and route definitions
├── db.py             # SQLAlchemy engine and session setup
├── models.py         # Card ORM model
├── init_db.py        # Creates database tables
├── sync_cards.py     # Fetches and syncs the Card Kingdom pricelist
├── pyproject.toml    # Project metadata and dependencies
├── uv.lock           # Lockfile
└── .env              # Database connection string (not committed)
```

## Integration with CK Cart Population

Point the cart tool at this server by setting `API_SERVER` in the cart project's `.env`:

```env
API_SERVER=http://localhost:8000
```

The `CartManager` will then call `POST /url_cards` to resolve product IDs in bulk instead of scraping each card page individually.