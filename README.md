# Django Shopping App 🛒

A Django app for tracking grocery/supermarket purchases. Register the stores you
buy from, catalog the products you buy, record each purchase with its price, and
compare price history across stores — normalized to a price per unit so a 3-pack
of 1.5 Lt bottles is directly comparable to a single 600 ml one.

## Features

- **CRUD** for articles (products), sellers (stores), and purchases
- **Price normalization** — `price_per_unit_with_unit()` divides package price by
  content × package count, so prices are comparable across package sizes
- **Purchase verification** — pick a date and a store, get the total spent
  (`Σ quantity × price`) to check against your physical receipt
- **Price history per article** — every purchase of a product, across all stores
- **Consult views** — browse the full article and family catalogs
- **Photo uploads** for articles and sellers
- **Weather widget** in the navbar — async fetch from Open-Meteo, geolocated by
  IP, refreshed by a background task and cached
- Bootstrap UI, Spanish (`es-mx`) locale

## Tech Stack

| Layer | Choice |
| --- | --- |
| Framework | Django 4.1.5 (MVT, function-based views) |
| Database | SQLite |
| HTTP | `aiohttp` (async, weather) · `requests` (geolocation) |
| Images | Pillow |
| Frontend | Django templates + Bootstrap |
| Config | `python-dotenv` |

## Data Model

```
Division → Family → Article → Purchase
                               ↳ Seller
```

- **Division** — top-level grouping (e.g. a Walmart division)
- **Family** — product category, belongs to a Division
- **Article** — a product: name, content quantity, unit
  (`Lt`/`Kg`/`Pza`/`Caja`/`Paquete`/`Rollos`), package multiplier, optional EAN
- **Purchase** — a buy event: Article + Seller, date, quantity, price per package
- **Seller** — a store/supermarket

All foreign keys use `on_delete=PROTECT`, so you can't delete a store or product
that has purchases attached to it.

## Getting Started

```bash
# 1. Clone and enter the project
git clone <repo-url>
cd shop

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up the database
python manage.py migrate

# 5. (Optional) Create an admin account
python manage.py createsuperuser

# 6. Run it
python manage.py runserver
```

Then open http://127.0.0.1:8000/.

`settings.py` calls `load_dotenv()`, so a `.env` file at the project root is
picked up automatically if you add one. None is required to run the app today.

## Routes

| Path | Name | Purpose |
| --- | --- | --- |
| `/` | `home` | Landing page |
| `/articles/` | `article_list` | List + create articles |
| `/articles/<pk>/edit/` | `article_edit` | Edit an article |
| `/articles/<pk>/delete/` | `article_delete` | Delete an article |
| `/articles/<id>/purchases/` | `article_purchases` | Price history for a product |
| `/sellers/` | `seller_list` | List + create sellers |
| `/sellers/<pk>/edit/` | `seller_edit` | Edit a seller |
| `/sellers/<pk>/delete/` | `seller_delete` | Delete a seller |
| `/purchases/` | `purchase_list` | List purchases |
| `/purchases/create` | `purchase_create` | Record a purchase |
| `/purchases/<pk>/edit/` | `purchase_edit` | Edit a purchase |
| `/purchases/<pk>/delete/` | `purchase_delete` | Delete a purchase |
| `/purchases/verification/` | `purchase_verification` | Total by date + store |
| `/consult_articles/` | `consult_articles` | Article catalog |
| `/consult_families/` | `consult_familes` | Family catalog |
| `/admin/` | — | Django admin |

## Project Layout

```
shop/
├── manage.py
├── requirements.txt
├── shop/                        # Project config
│   ├── settings.py              # es-mx locale, America/Mexico_City, d-m-Y dates
│   ├── urls.py
│   └── wsgi.py
└── shopapp/                     # All application logic
    ├── models.py                # Division, Family, Seller, Article, Purchase
    ├── views.py                 # 19 function-based views
    ├── forms.py                 # ArticleForm, SellerForm, PurchaseForm
    ├── urls.py
    ├── context_processors.py    # Injects `weather` into every template
    ├── apps.py                  # Starts the weather refresh background task
    ├── services/
    │   ├── weather_service.py   # Open-Meteo, 10-min cache, code → emoji
    │   └── location_service.py  # ipapi.co, 24-h cache, falls back to Zapopan, MX
    └── templates/
```

## Development

```bash
# Run the test suite
python manage.py test shopapp

# Run a single test
python manage.py test shopapp.tests.TestClassName.test_method_name

# Migrations
python manage.py makemigrations
python manage.py migrate

# Interactive shell
python manage.py shell
```

## Notes

- The app currently has **no authentication** — all views are open. A
  `registration/login.html` template exists but no login flow is wired up.
- `DEBUG = True` and `SECRET_KEY` is hardcoded in `settings.py`. Move both to
  environment variables before deploying anywhere public.
- `MEDIA_ROOT` is the project root and uploads land in `images/`. `db.sqlite3`
  and `/media/` are gitignored.
