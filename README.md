# Ujamaaflow

## Introduction

Ujamaaflow is a web application that is designed to link resource donors with individuals and families in need.
The platform streamlines the donation process, making it easy for donors to offer items such as food, clothing, devices and equipment and for recipients to request the resources they need. 
Inspired by the spirit of "Ujamaa" (community, cooperation and familyhood), Ujamaaflow fosters a sense of togetherness and support which flows within the local communities, making it easily accessible to everyone in need (hence the flow part).

## Key Features

- **Role‑aware redirects:** After login, users are redirected to a unified dashboard that renders a donor, recipient, or admin view based on their role.
- **Donations (from donors):** Create donations with item, quantity, description, and location. Optional image upload with type/size validation (image/*, <= 5MB). Images are stored and displayed on browse pages.
- **Requests (from recipients):** Submit requests with item needed, quantity, reason, and location.
- **Browse and search (for recipients):** Browse available donations from the database with search by keyword and location. Basic image preview supported.
- **Matching engine (admin):** Admins can match a donation to a request from the admin dashboard, marking both as matched/fulfilled.
- **Media & safety:** Image upload validations and a report mechanism allowing users to flag a donation with a reason for admin review.
- **Secure authentication:** Hashed passwords, sessions via Flask‑Login.
- **SQLite storage:** Models for `User`, `Donation`, `Request`, `Match`, `DonationMedia`, `DonationReport`.

## How it works?

Glad you asked :). 
1. **Donors** register and list available resources.
2. **Recipients** register and submit requests for needed items.
3. **Admins** review and match donations to requests, ensuring resources reach those who need them most.

## Getting started

1. Clone the repo
   ```bash
   git clone https://github.com/RayOgeto/kool-projekt.git
   cd kool-projekt
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Set environment (optional)
   - Copy `.env.example` to `.env` and set `SECRET_KEY` if needed
4. Run the app
   ```bash
   flask run
   ```

On first run, database tables are auto‑created. Uploaded images are saved under `app/static/uploads/` (the folder will be created if missing).

## Routes overview

- `GET /` – Home
- `GET/POST /login`, `GET/POST /register`, `GET /logout`
- `GET /dashboard` – Role‑aware dashboard (donor/recipient/admin)
- `GET/POST /donate` – Donor creates a donation (supports image upload)
- `GET/POST /request-resource` – Recipient creates a request
- `GET /browse` – Recipient browse/search donations
- `GET /admin/matches` – Admin dashboard
- `POST /admin/match` – Admin creates a match
- `POST /donation/<id>/report` – Report a donation

## Data models

- `User(id, role, username, email, password)`
- `Donation(id, donor_id, item, quantity, description, location, matched, flagged)`
- `Request(id, recipient_id, item_needed, quantity, reason, location, fulfilled)`
- `Match(id, donation_id, request_id, status)`
- `DonationMedia(id, donation_id, file_path, created_at)`
- `DonationReport(id, donation_id, reporter_id, reason, created_at)`

## Notes

- Image uploads are validated for MIME type and max size (5MB).
- Reported donations are flagged for admin attention.
