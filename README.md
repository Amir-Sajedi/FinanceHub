# FinanceHub

FinanceHub is a Django-based web app that provides a simple financial hub with user accounts and a conversion dashboard. It presents a public landing page and a login-protected hub that pulls live market pricing data from an external site.

## What the application does
- Shows a public landing page with links to core pages
- Lets users sign in and manage their session (login, logout, password reset)
- Provides a hub page with conversion tools and price calculators for precious metals and other assets
- Retrieves live market prices by scraping an external site

## Main features
- Django authentication flows (login, logout, password change and reset)
- Login-protected hub page
- Server-side scraper with requests and BeautifulSoup to fetch market prices
- Template-based UI with static CSS and JavaScript

## Tech stack and dependencies
- Python 3
- Django 5.2.7
- SQLite (default database)
- requests
- beautifulsoup4
- HTML, CSS and JavaScript templates

## Project structure
- `bkiblog/` - Django project settings and entry points
- `blog/` - landing page and authentication-related views/templates
- `conversionapp/` - conversion hub view and market data scraper
- `templates/` and `static/` - shared templates and styling

## Setup and run locally
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install Django==5.2.7 requests beautifulsoup4
   ```
3. Apply database migrations:
   ```bash
   cd bkiblog
   python manage.py migrate
   ```
4. Create a user account (needed to access the hub):
   ```bash
   python manage.py createsuperuser
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```
6. Open `http://127.0.0.1:8000/` in your browser. The hub is available at `/hub/` after signing in.

## Environment notes
- An active internet connection is required for live market pricing.
- The project uses SQLite by default and stores the database in `bkiblog/db.sqlite3`.
