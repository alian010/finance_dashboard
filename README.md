```md
# Personal Finance Dashboard — Secure Ledger & Real-Time Insights  
**Stack:** Django REST Framework (DRF) + JWT + Postman + Tailwind UI (Templates) + Chart.js

A private, user-isolated personal finance ledger where users can securely log daily expenditures and view an automatically updating dashboard (monthly total, category breakdown, and month-over-month spending trend).

---

## ✅ Specification Coverage (What This Project Delivers)

### 1) Core Concept
- Secure login (JWT) to access **only your own** financial data
- Add / edit / delete daily expenditures (amount, date, category, note)
- Real-time dashboard that refreshes summary metrics and charts after every change

### 2) System Architecture Requirements
#### A. User-Centric Data Isolation (**Owner-Only Policy**)
- Every transactions query is filtered to `request.user`
- Object-level protection ensures no user can read/update/delete another user’s transactions
- Enforced at API level for every request

#### B. Backend Logic (DRF)
- **Data Model:** decimal amount, date, enum category, FK to user
- **Server Aggregation:** `/api/summary/` returns dashboard-ready data
- **Validation:** rejects invalid payloads with **400 Bad Request**  
  - amount must be **> 0**
  - category must be from predefined list
  - date cannot be in the future

#### C. Frontend Experience
- Premium Tailwind dashboard UI + Chart.js breakdown chart
- Pagination for transaction history (20–50 per page)
- Add/Edit/Delete triggers instant refresh (no full page reload)

### 3) Technical Standards & Documentation ✅
- Swagger/OpenAPI live docs included
- Correct HTTP methodology:
  - `PUT` full replacement
  - `PATCH` partial update
- Modular code structure with separation of concerns:
  - ORM queries & aggregation logic separated from response formatting

---

## Tech Stack

### Backend
- Python 3.12+
- Django 5.x
- Django REST Framework
- JWT auth: `djangorestframework-simplejwt`
- API Docs: `drf-spectacular`

### Frontend
- Django templates
- Tailwind CSS (CDN)
- Chart.js (CDN)

---

## Project Structure

├─ accounts/
│  ├─ admin.py
│  ├─ models.py
│  ├─ serializers.py
│  ├─ urls.py
│  └─ views.py
├─ transactions/
│  ├─ admin.py
│  ├─ models.py
│  ├─ serializers.py
│  ├─ permissions.py
│  ├─ pagination.py
│  ├─ urls.py
│  └─ views.py
├─ reports/
│  ├─ admin.py
│  ├─ urls.py
│  └─ views.py
├─ finance/
│  ├─ settings.py
│  └─ urls.py
├─ templates/
│  ├─ base.html
│  ├─ login.html
│  ├─ register.html
│  └─ dashboard/
│     ├─ index.html
│     ├─ _topbar.html
│     ├─ _kpis.html
│     ├─ _chart.html
│     ├─ _transactions_table.html
│     ├─ _modal_add.html
│     ├─ _modal_edit.html
│     └─ _scripts.html
└─ manage.py

````

---

## Setup Instructions (Local Development)

### 1) Create Virtual Environment
**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
````

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install Dependencies

```bash
pip install -r requirements.txt
```

### 3) Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4) Create Admin (Optional)

```bash
python manage.py createsuperuser
```

### 5) Run Server

```bash
python manage.py runserver
```

---

## Frontend Pages (UI)

* Login Page: `http://127.0.0.1:8000/api/auth/login/`
* Register Page: `http://127.0.0.1:8000/api/auth/register-page/`
* Dashboard: `http://127.0.0.1:8000/dashboard/`

> Dashboard requires a valid access token. If token is missing/expired, it redirects to login.

---

## API Documentation (postman)

<img width="1267" height="961" alt="Screenshot 2026-02-01 164641" src="https://github.com/user-attachments/assets/7d2cb531-aa39-493a-9210-0e1847fffd17" />

---

## Authentication (JWT)

### Get Token (Login)

`POST /api/auth/token/`

Body:

```json
{
  "username": "demo",
  "password": "StrongPass123!"
}
```

Response:

```json
{
  "refresh": "....",
  "access": "...."
}
```

### Use Token

All protected API calls must include:

```
Authorization: Bearer <access_token>
```

### Refresh Token

`POST /api/auth/token/refresh/`

Body:

```json
{
  "refresh": "<refresh_token>"
}
```

---

## API Endpoints

### Auth

* `POST /api/auth/register/` (public)
* `POST /api/auth/token/` (public)
* `POST /api/auth/token/refresh/` (public)
* `GET /api/auth/me/` (protected)
* `GET /api/auth/login/` (page)
* `GET /api/auth/register-page/` (page)

### Transactions (Owner-only, paginated)

* `GET /api/transactions/?page=1&page_size=20`
* `POST /api/transactions/`
* `GET /api/transactions/<id>/`
* `PUT /api/transactions/<id>/`  (full replacement)
* `PATCH /api/transactions/<id>/` (partial update)
* `DELETE /api/transactions/<id>/`

### Reports / Summary (dashboard aggregation)

* `GET /api/summary/`

---

## Validation Rules (400 Bad Request)

The backend enforces strict validation:

* **Amount** must be greater than zero
* **Date** cannot be in the future
* **Category** must match predefined enum choices
* Invalid payload returns `400 Bad Request` with field-level error messages

---

## Owner-only Data Isolation (Security)

Security requirement: a user can never access another user’s transactions.

Implementation principles:

* Queryset filtering: `Transaction.objects.filter(user=request.user)`
* Object-level permission: checks ownership during retrieve/update/delete
* If user tries to access another user’s transaction → returns **404/403** without exposing data

---

## Pagination

Transactions list is paginated:

* Default: 20 per page
* Configurable: 20 / 30 / 50 via query param `page_size`

Example:

```
GET /api/transactions/?page=1&page_size=20
```

DRF response format:

```json
{
  "count": 120,
  "next": "...",
  "previous": null,
  "results": [...]
}
```

---

## Aggregation Logic (`/api/summary/`)

### A) Current Month Total

Sum of all transactions in current calendar month.

### B) Category Breakdown

Group transactions by category (current month) and sum amounts:
`{"FOOD": "300.00", "RENT": "1500.00"}`

### C) Financial Trend (MoM %)

Percentage change vs previous month:

```
trend_percent = ((current_total - prev_total) / prev_total) * 100
```

Edge cases:

* If `prev_total == 0` and `current_total == 0` → trend = `0`
* If `prev_total == 0` and `current_total > 0` → trend = `100` (increase from zero baseline)

---

## PUT vs PATCH Methodology (Spec requirement)

### PATCH (Partial Update)

Updates only specified fields:
`PATCH /api/transactions/<id>/`

```json
{ "note": "Updated note only" }
```

### PUT (Full Replacement)

Requires full object payload:
`PUT /api/transactions/<id>/`

```json
{
  "amount": "250.00",
  "date": "2026-02-01",
  "category": "FOOD",
  "note": "Full update"
}
```

---

## Code Quality & Modularity (Spec requirement)

The project keeps logic modular and maintainable:

* **Models:** define schema + db constraints
* **Serializers:** validate input and format output
* **ViewSets/Views:** handle HTTP request/response only
* **Permissions:** isolate owner-only access
* **Pagination:** centralized config for pagination behavior
* **Reports Summary:** aggregation logic separated to keep views clean and testable

Recommended pattern (already followed / can be extended):

* `reports/services.py` → ORM aggregation + math
* `reports/views.py` → calls service & returns `Response(payload)`

---

## Postman Testing (Manual QA)

All endpoints were tested using Postman.

Typical workflow:

1. `POST /api/auth/register/` → create user
2. `POST /api/auth/token/` → receive `access` + `refresh`
3. Set Postman env vars:

   * `base = http://127.0.0.1:8000`
   * `access`, `refresh`
4. Send requests with header:

   * `Authorization: Bearer {{access}}`
5. Verified:

   * Transaction CRUD
   * Validation errors
   * Summary accuracy
   * Owner-only isolation (User A cannot access User B’s transactions)

---

## Run Tests (Automated)

```bash
python manage.py test
```

Recommended coverage:

* Owner-only isolation tests
* Validation tests (negative amount, future date, invalid category)
* Summary aggregation tests (month totals, category breakdown, trend math)

---

## Optional Configuration: Increase JWT Token Lifetime

In `finance/settings.py`:

```python
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}
```

---

## Future Improvements (Production Hardening)

* Move refresh token to httpOnly cookie (more secure than localStorage)
* Add throttling / rate limiting for auth endpoints
* Add filtering/search on transactions
* Add CI (GitHub Actions) for tests + linting

---

## Notes

This repository is designed to meet the provided project specification with a strong emphasis on:

* Security (JWT + owner-only isolation)
* Server-side aggregation
* Clean API documentation (postman)
* Modular code quality and maintainability

