# ALX Travel App

A Django REST Framework project for managing travel listings, bookings, payments (Chapa integration), and async notifications with Celery + RabbitMQ.

## Features
- Listings CRUD API
- Booking system
- Reviews
- Chapa Payment Integration
- Swagger API docs
- Celery + RabbitMQ email notifications

## Setup

```bash
# Clone repo
git clone https://github.com/lexpeachy/alx_travel_app.git
cd alx_travel_app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp alx_travel_app/.env.example alx_travel_app/.env

## running

python manage.py migrate
python manage.py runserver
celery -A alx_travel_app worker -l info


---

## 4. `.env.example`  
So collaborators know what variables they must set (but **not actual values**).  

At `alx_travel_app/.env.example`:  

```env
DEBUG=True
SECRET_KEY=your-secret-key

DB_NAME=alx_travel_db
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306

CHAPA_SECRET_KEY=your_chapa_secret_key
CHAPA_BASE_URL=https://api.chapa.co/v1

EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password

## HERE IS THE STRUCTURE


alx_travel_app/                 # GitHub repo root
├── .gitignore
├── README.md
├── requirements.txt
├── docker-compose.yml          # optional
│
├── alx_travel_app/             # Project directory
│   ├── .env.example            # template, NOT the real .env
│   ├── manage.py
│   ├── alx_travel_app/         # settings, celery, urls
│   ├── listings/               # app
│   └── migrations/
