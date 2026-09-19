# Zyanya – Django E-commerce Store

An online clothing store built with Django: product sections, product pages, cart, wishlist, coupons, Stripe card payments, email OTP sign-up, and order confirmation emails.

## Tech stack
- Django 4.2, Python 3.12
- PostgreSQL in production (SQLite locally)
- Stripe (payments), Gmail SMTP
- Bootstrap 5 + django-crispy-forms
- Hosted on Vercel (serverless Python + WhiteNoise), database on Neon

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

## Deploy on Vercel
1. Create a free PostgreSQL database on neon.tech and copy its connection string.
2. From your computer, set up the database once:
   ```bash
   set DATABASE_URL=<neon connection string>
   python manage.py migrate
   python manage.py loaddata shop_data.json
   python manage.py createsuperuser
   ```
3. On vercel.com: **Add New → Project**, import this repo, add the environment variables from `.env.example`, and deploy.
   `vercel.json` routes every request to `ecommerece/wsgi.py`.

After changing models, run `python manage.py migrate` against the Neon database again.

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
