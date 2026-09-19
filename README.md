# Zyanya – Django E-commerce Store

An online clothing store built with Django: product sections, product pages, cart, wishlist, coupons, Stripe card payments, email OTP sign-up with reCAPTCHA, and order confirmation emails.

## Tech stack
- Django 4.2, Python 3.12
- PostgreSQL in production (SQLite locally)
- Stripe (payments), Google reCAPTCHA, Gmail SMTP
- Bootstrap 5 + django-crispy-forms
- Hosted on Render (gunicorn + WhiteNoise)

## Run locally
```bash
python -m venv venv
venv\Scripts\activate          # Windows  (source venv/bin/activate on Mac/Linux)
pip install -r requirements.txt
copy .env.example .env         # then fill in your keys
python manage.py migrate
python manage.py loaddata shop_data.json
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000

## Deploy on Render
1. Create a free PostgreSQL database (e.g. on neon.tech) and copy its connection string.
2. On render.com: **New → Web Service**, select this repo.
   - Build Command: `bash build.sh`
   - Start Command: `gunicorn ecommerece.wsgi`
3. Add the environment variables listed in `.env.example` (`DATABASE_URL` = the PostgreSQL string, `DEBUG` = `False`).
4. Deploy. `build.sh` collects static files, runs migrations, loads the products on the first deploy and creates the admin user.

## Project structure
```
ecommerece/      project settings and URLs
shoppingapp/     models, views, forms, URLs
templates/       HTML pages
static/          CSS, JS, images
media/           product and section images
shop_data.json   sections and products to load into a new database
build.sh         Render build script
```
