# BAB AL SABARR — Logistics Trip Submission System

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![License](https://img.shields.io/badge/License-Proprietary-red)
![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?logo=render&logoColor=white)

> **Built by:** Mohammad Ashraf
> **Contact:** mohdashraf09458@gmail.com
> **Delivered:** May 2026

---

## ⚠️ Important — Read Before Anything Else

This is a **private, proprietary project** built exclusively for BAB AL SABARR. The source code, design, and all associated files are confidential. Do not share, redistribute, or publish any part of this system without authorisation.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Live Application](#live-application)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Local Development Setup](#local-development-setup)
- [Deployment on Render](#deployment-on-render)
- [Static Files Note](#static-files-note)
- [Admin Panel Guide](#admin-panel-guide)
- [PWA Installation for Drivers](#pwa-installation-for-drivers)
- [Email / SMTP (Coming Soon)](#email--smtp-coming-soon)
- [Known Limitations](#known-limitations)
- [Support & Maintenance](#support--maintenance)

---

## Project Overview

The BAB AL SABARR Logistics Trip Submission System is a mobile-first web application that allows truck drivers to submit trip information before departure — directly from their Android phones, with no app installation required.

**Who uses it:**

| User | Role |
|---|---|
| Truck Drivers | Submit trip data from phone before starting a trip |
| Operations Staff | View all submissions in real time via admin panel |
| Management | Export Excel reports for auditing and record-keeping |

**Why there is no driver login:**

Drivers are non-technical users working under time pressure at loading docks. A login system adds friction, forgotten passwords, and support overhead. The form is intentionally open — all security and access control is handled at the admin level.

**Trip submission workflow:**

```
Driver opens web app
        ↓
Enters Truck Number + Trip ID (TRP-XXXX)
        ↓
Photographs container with phone camera
        ↓
Optionally adds second container photo
        ↓
Uploads Electronic Receipt (image or PDF)
        ↓
Taps Submit
        ↓
Data saved to PostgreSQL → Files saved to Cloudinary
        ↓
Operations staff see submission instantly in admin panel
```

---

## Live Application

| Page | URL |
|---|---|
| Driver Submission Form | `https://bab-al-sabar.onrender.com/` |
| Admin Panel | `https://bab-al-sabar.onrender.com/admin/` |
| Excel Export | `https://bab-al-sabar.onrender.com/admin/action/export as excel` |

---

## Features

### Driver-Facing Features
- Single-page form fully optimised for Android phones
- Large touch targets — usable with gloves or in low-light conditions
- TRP- prefix applied automatically to Trip ID
- Phone camera opens directly for container photo
- Browser-side image compression before upload — saves mobile data on slow connections
- Real-time photo preview after selection
- Client-side file size validation — errors shown before any upload begins
- Submit button shows a spinner and locks during upload — prevents accidental double submission
- Clean success page after every submission
- Installable on phone home screen as a PWA (no app store needed)

### Admin-Facing Features
- Full submission list with pagination
- Search by Truck Number or Trip ID
- Filter by submission date and trip status
- Sort by date, truck number, or status
- Direct links to all uploaded files (photos, ER documents) served from Cloudinary
- One-click Excel export of all trip records
- Full Django authentication protects the admin panel

### File Handling
- Container photo (required): JPG, JPEG, PNG — compressed in browser before upload
- Second container photo (optional): JPG, JPEG, PNG
- Electronic Receipt (required): JPG, JPEG, PNG, or PDF
- All files stored permanently on Cloudinary — not deleted on server restarts or redeployments
- File type and size validated both in the browser and on the server

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | Django 5.2 | Web framework, admin panel, form handling |
| Database | PostgreSQL | Persistent trip data storage |
| Media Storage | Cloudinary | Permanent file storage for photos and PDFs |
| Static Files | WhiteNoise 6.7 | Serves CSS/JS in production |
| WSGI Server | Gunicorn | Production web server |
| Hosting | Render | Cloud deployment platform |
| Frontend | Tailwind CSS (CDN) | Mobile-first responsive styling |
| Image Compression | browser-image-compression 2.0.2 | Client-side photo compression |
| Environment Config | python-dotenv | Loads `.env` variables locally |
| Database URL | dj-database-url | Parses `DATABASE_URL` connection string |
| Excel Export | openpyxl | Generates `.xlsx` report files |
| Image Processing | Pillow | Server-side image validation |

---

## Project Structure

```
bab-al-sabar/
│
├── bas_config/                  # Django project configuration
│   ├── settings.py              # All settings — driven by environment variables
│   ├── urls.py                  # Root URL config and admin panel branding
│   └── wsgi.py                  # WSGI entry point for Gunicorn
│
├── trips/                       # Core application
│   ├── migrations/              # Database schema migration files
│   ├── admin.py                 # Admin list display, search, filters, Excel export
│   ├── forms.py                 # TripForm with field-level validation
│   ├── models.py                # Trip model definition
│   ├── urls.py                  # App URL patterns
│   ├── validators.py            # File type and size validation functions
│   └── views.py                 # Form submission view and Excel export view
│
├── templates/
│   ├── index.html               # Driver submission form (mobile-first)
│   └── success.html             # Post-submission confirmation page
│
├── static/
│   ├── images/logo.png          # App icon (PWA + favicon)
│   ├── manifest.json            # PWA manifest file
│   └── service-worker.js        # PWA service worker
│
├── staticfiles/                 # Auto-generated by collectstatic — do not edit
├── .gitignore                   # Excludes .env, db.sqlite3, __pycache__, staticfiles
├── manage.py                    # Django management entry point
├── Procfile                     # Render start command declaration
├── requirements.txt             # Python package dependencies
└── README.md                    # This file
```

---

## Environment Variables

All sensitive configuration is stored as environment variables — never hardcoded in the source code. For production (Render), these are set in the Render dashboard. For local development, they go in a `.env` file.

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django cryptographic secret — must be unique and private | `django-insecure-abc123xyz...` |
| `DEBUG` | `True` for local dev only. Always `False` in production | `False` |
| `ALLOWED_HOSTS` | Comma-separated hostnames Django will serve | `your-app.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated trusted origins for form submissions | `https://your-app.onrender.com` |
| `DATABASE_URL` | Full PostgreSQL connection string from Render | `postgres://user:pass@host:5432/db` |
| `CLOUDINARY_CLOUD_NAME` | Your Cloudinary account cloud name | `dmabcxyz` |
| `CLOUDINARY_API_KEY` | Your Cloudinary API key | `497787839547` |
| `CLOUDINARY_API_SECRET` | Your Cloudinary API secret | `YjqXFXVz...` |

> **Security rule:** Never commit `.env` to GitHub. It is already listed in `.gitignore`. All production values must be set directly in the Render dashboard.

**Generating a new SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Local Development Setup

Follow these steps to run the project on your own machine.

**1. Clone the repository**
```bash
git clone https://github.com/Mohdashraf11/bab-al-sabar.git
cd bab-al-sabar
```

**2. Create and activate a virtual environment**
```bash
# Windows
python -m venv env
env\Scripts\activate

# macOS / Linux
python3 -m venv env
source env/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create your `.env` file**

Create a file named `.env` in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000
DATABASE_URL=sqlite:///db.sqlite3
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

> For local development, `DATABASE_URL=sqlite:///db.sqlite3` uses a local file database so you do not need PostgreSQL installed locally.

**5. Run migrations**
```bash
python manage.py migrate
```

**6. Create an admin user**
```bash
python manage.py createsuperuser
```

**7. Collect static files**
```bash
python manage.py collectstatic --noinput
```

**8. Start the development server**
```bash
python manage.py runserver
```

- Driver form: `http://127.0.0.1:8000/`
- Admin panel: `http://127.0.0.1:8000/admin/`

---

## Deployment on Render

### Step 1 — Create a PostgreSQL database

In the Render dashboard: **New → PostgreSQL**

Create a free instance. Once created, copy the **Internal Database URL** from the database info page.

### Step 2 — Create a Web Service

In the Render dashboard: **New → Web Service**

Connect the GitHub repository: `Mohdashraf11/bab-al-sabar`

### Step 3 — Configure build and start commands

| Setting | Value |
|---|---|
| **Environment** | Python |
| **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
| **Start Command** | `gunicorn bas_config.wsgi:application --bind 0.0.0.0:$PORT` |

### Step 4 — Set environment variables in Render dashboard

Under your web service → **Environment**, add all variables from the [Environment Variables](#environment-variables) table.

Key values to set correctly:
- `DEBUG` → `False`
- `DATABASE_URL` → Internal Database URL from Step 1
- `ALLOWED_HOSTS` → `bab-al-sabar.onrender.com`
- `CSRF_TRUSTED_ORIGINS` → `https://bab-al-sabar.onrender.com/`

### Step 5 — Deploy

Click **Deploy**. Render installs packages, collects static files, runs migrations, and starts Gunicorn automatically. Every push to the `main` branch triggers a new deploy.

### Step 6 — Create the admin superuser on Render

After the first successful deploy, open **Dashboard → your service → Shell** and run:
```bash
python manage.py createsuperuser
```

---

## Static Files Note

This project uses `django.contrib.staticfiles.storage.StaticFilesStorage` rather than WhiteNoise's compressed storage backend.

**Reason:** WhiteNoise 6.8+ uses Python's `concurrent.futures` thread pool to compress static files during `collectstatic`. On Python 3.14 (which Render now runs), a change in thread scheduling causes a race condition — WhiteNoise tries to open a file for compression after the hashing step has already renamed it. This raises a `FileNotFoundError` and fails the entire build.

**Impact:** Static files are served without hash-based cache fingerprinting. This has no effect on functionality — WhiteNoise's middleware (`whitenoise.middleware.WhiteNoiseMiddleware`) handles all static file serving correctly in production. The admin panel, CSS, and JavaScript all load normally.

This is a confirmed upstream bug. When WhiteNoise releases a fix for Python 3.14 compatibility, the storage backend can be updated to `CompressedManifestStaticFilesStorage` with no other changes required.

---

## Admin Panel Guide

### Accessing the admin panel

```
https://bab-al-sabar.onrender.com/admin/
```

Log in with the superuser credentials created during deployment.

### What you can do

| Action | How |
|---|---|
| View all trip submissions | Admin home → Trips |
| Search by Truck Number or Trip ID | Use the search bar at the top of the trip list |
| Filter by date | Use the right-hand date filter (Today / This Week / This Month) |
| Filter by status | Use the right-hand status filter |
| View an individual submission | Click any row in the trip list |
| Open a container photo | Click the Cloudinary URL in the trip detail view |
| Open an ER document | Click the Cloudinary URL in the trip detail view |
| Export all trips to Excel | Visit `/admin/action/export as excel` or use the export link |
| Change a trip's status | Open the trip detail → change the Status field → Save |
| Add a new admin user | Admin home → Users → Add User |

### Creating additional admin users

```bash
# On Render shell, or locally:
python manage.py createsuperuser
```

Or in the admin panel: **Authentication → Users → Add User**. Assign staff status and the required permissions.

---

## PWA Installation for Drivers

Drivers do not need to visit an app store. They install the app directly from the browser.

### Android (Chrome) — Recommended for drivers

1. Open the app URL in Chrome
2. Tap the **three-dot menu (⋮)** in the top-right corner
3. Tap **"Add to Home screen"**
4. Tap **"Add"** to confirm
5. The BAB AL SABARR icon appears on the home screen
6. Tap it — the app opens full-screen with no browser address bar

### iOS (Safari)

1. Open the app URL in Safari
2. Tap the **Share button** (box with arrow pointing up, bottom of screen)
3. Scroll down and tap **"Add to Home Screen"**
4. Tap **"Add"** to confirm

> **Note for operations staff:** Share the app URL with drivers via WhatsApp. Ask them to follow the Android steps above. Once installed, drivers never need to type the URL again.

---

## Email / SMTP (Coming Soon)

Email notifications are not yet implemented. This feature is planned for a future update.

**Planned behaviour:**
- When a driver submits a trip, an automated email is sent to the operations team
- Email will include: Truck Number, Trip ID, submission time, and links to uploaded files

**Future configuration (when implemented):**

For Gmail:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=noreply@babalsabar.com
OPERATIONS_EMAIL=ops@babalsabar.com
```

For SendGrid:
```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

Contact Mohammad Ashraf (details below) to have this feature implemented.

---

## Known Limitations

The following are known gaps that can be addressed in future development:

| Limitation | Details |
|---|---|
| No offline submission queue | If a driver submits on a dropping connection, the form fails and must be resubmitted. Background sync is planned. |
| No Arabic language support | The interface is English-only. Arabic (RTL) localisation is planned. |
| Excel export has no date filter | The export always includes all trips. A date-range filter will be added in a future update. |
| No duplicate warning before submission | If a driver enters a duplicate Trip ID, the error only appears after submission. A real-time check before submit is planned. |
| Render free tier sleep | On Render's free plan, the service sleeps after 15 minutes of inactivity. The first request after sleep can take 30–60 seconds. Upgrading to a paid Render instance eliminates this. |

---

## Support & Maintenance

This system was designed and built by **Mohammad Ashraf** and delivered to BAB AL SABARR in May 2026.

The codebase is clean, documented, and structured for easy handover to any Django developer for future maintenance.

**For technical support or future enhancements, reach out to:**

| | |
|---|---|
| **Developer** | Mohammad Ashraf |
| **Email** | mohdashraf09458@gmail.com |

**What future support can include:**
- Bug fixes and error investigation
- New features (SMTP notifications, Arabic language, offline support, date-filtered export)
- Render infrastructure management
- Cloudinary storage management
- Database backups and migration assistance

> There is no active support contract at this time. Support is available on a case-by-case basis — simply send an email describing the issue or requirement.

---

*BAB AL SABARR Logistics Trip Submission System — Built by Mohammad Ashraf, 2026. All rights reserved.*
