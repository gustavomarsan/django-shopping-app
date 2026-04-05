# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

```bash
# Run development server
python manage.py runserver

# Run tests
python manage.py test shopapp

# Run a single test
python manage.py test shopapp.tests.TestClassName.test_method_name

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Django shell
python manage.py shell

# Create superuser for admin
python manage.py createsuperuser
```

## Architecture Overview

Django MVT app for tracking grocery/supermarket purchases. Users register sellers (stores), create articles (products), record purchases with prices, and analyze price history across sellers.

### Data Model Hierarchy

```
Division → Family → Article → Purchase
                               ↳ Seller
```

- **Division**: Top-level grouping (e.g., Walmart divisions)
- **Family**: Product category, belongs to a Division
- **Article**: A product with quantity, unit (Lt/Kg/Pza/Caja/Paquete/Rollos), package multiplier, and optional EAN
- **Purchase**: A buy event linking Article + Seller with date, quantity, and price per package
- **Seller**: A store/supermarket

Both `Article` and `Purchase` expose `price_per_unit_with_unit()` to normalize prices across different package sizes.

### App Structure

- `shop/` — Django project config (settings, root urls, wsgi)
- `shopapp/` — Single app containing all logic:
  - `models.py` — 5 models with FK relationships using `PROTECT` on delete
  - `views.py` — 19 function-based views organized around CRUD for each model
  - `forms.py` — 3 ModelForms (ArticleForm, SellerForm, PurchaseForm) with Bootstrap styling; PurchaseForm auto-fills date from last purchase
  - `urls.py` — 14 routes
  - `services/weather_service.py` — Async weather via Open-Meteo API with 10-minute cache; maps weather codes to emoji icons
  - `services/location_service.py` — IP geolocation via ipapi.co with 24-hour cache; fallback to Zapopan, Mexico
  - `context_processors.py` — Injects `weather` into all templates via `async_to_sync()`
  - `apps.py` — Starts `weather_refresh_loop()` background task on app ready

### Key Configuration

- Django 2.2.3, Python, SQLite, Bootstrap UI
- Locale: `es-mx`, timezone: `America/Mexico_City`, date format: `d-m-Y`
- No authentication (open access)
- Media files served from project root; excluded from git
- `django.contrib.humanize` enabled for template filters
