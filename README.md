# Python Based Finance System Backend
This project demonstrates the design and development of a Python backend system for managing financial records, implementing business logic, and generating analytical summaries with role-based access control.


## Tech Stack

- **FastAPI** — API framework
- **PostgreSQL** — Database
- **SQLAlchemy** — ORM
- **Pydantic** — Data validation
- **JWT (python-jose)** — Authentication
- **Passlib + bcrypt** — Password hashing
- **Docker + Docker Compose** — Containerization

## Project Structure

```
app/
├── api/                  # Route handlers
│   ├── auth.py           # Register, login, me
│   ├── transactions.py   # CRUD + filters + summary
│   └── users.py          # Admin user management
├── core/                 # App configuration
│   ├── config.py         # Environment variables
│   ├── database.py       # DB engine and session
│   └── security.py       # JWT, hashing, role checks
├── models/               # SQLAlchemy table definitions
│   ├── users.py
│   └── transactions.py
├── schemas/              # Pydantic validation schemas
│   ├── user.py
│   └── transaction.py
├── services/             # Business logic
│   └── transaction_services.py
└── main.py               # App entry point
```

## Setup Instructions

### Prerequisites
- Docker
- Docker Compose

### Running the Project

```bash
# Clone the repository
git clone <your-repo-url>
cd fin-backend

# Start the application
sudo docker compose up --build
```

API will be available at `http://localhost:8000`

Swagger UI (interactive docs) at `http://localhost:8000/docs`

## Environment Variables

Set in `docker-compose.yml`:

| Variable | Default | Description |
|----------|---------|-------------|
| `PG_DATABASE_URL` | `postgresql+psycopg2://root:root@db:5432/user_data` | PostgreSQL connection URL |
| `SECRET_KEY` | `supersecretkey123` | JWT signing key |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Token expiry (24 hours) |

## Seeding Data

To populate the database with sample users and transactions:

```bash
sudo docker compose exec app python seed.py
```

This creates:
- 3 users — admin, analyst, viewer
- 10 sample transactions — mix of income and expense across multiple categories

**Seeded credentials:**

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@finance.com | admin123 |
| Analyst | analyst@finance.com | analyst123 |
| Viewer | viewer@finance.com | viewer123 |

## API Endpoints

### Auth
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/auth/register` | Register new user | Public |
| POST | `/api/auth/login` | Login and get JWT token | Public |
| GET | `/api/auth/me` | Get current user | All roles |

### Health Check
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/` | Check if API is running | Public |


### Transactions
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/transactions/` | Create transaction | Admin |
| GET | `/api/transactions/` | List transactions (with filters) | All roles |
| GET | `/api/transactions/summary` | Analytics and summary | All roles |
| GET | `/api/transactions/{id}` | Get single transaction | All roles |
| PATCH | `/api/transactions/{id}` | Update transaction | Admin |
| DELETE | `/api/transactions/{id}` | Delete transaction | Admin |

### Users
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/users/` | List all users | Admin |
| DELETE | `/api/users/{id}` | Delete a user | Admin |

### Filters available on `GET /api/transactions/`
- `type` — filter by `income` or `expense`
- `category` — filter by category name
- `date_from` — filter from date (YYYY-MM-DD)
- `date_to` — filter to date (YYYY-MM-DD)

## Roles and Access

| Feature | Viewer | Analyst | Admin |
|---------|--------|---------|-------|
| View transactions | ✅ | ✅ | ✅ |
| Filter transactions | ✅ | ✅ | ✅ |
| View summary | ✅ | ✅ | ✅ |
| Create transaction | ❌ | ❌ | ✅ |
| Update transaction | ❌ | ❌ | ✅ |
| Delete transaction | ❌ | ❌ | ✅ |
| Manage users | ❌ | ❌ | ✅ |

## Summary Analytics

`GET /api/transactions/summary` returns:
- Total income
- Total expenses
- Current balance
- Category-wise breakdown
- Recent 5 transactions

## Testing with Swagger

1. Open `http://localhost:8000/docs`
2. Register a user via `POST /api/auth/register`
3. Login via `POST /api/auth/login` — copy the `access_token`
4. Click the **Authorize** 🔒 button at the top
5. Paste the token and click Authorize
6. All protected endpoints are now accessible

## Important Note on Updating Transactions

When using `PATCH /api/transactions/{id}`, only include the fields you want to update in the request body. Remove all other fields.

**Correct:**
```json
{
  "amount": 75000
}
```

**Incorrect — will cause errors:**
```json
{
  "amount": 75000,
  "type": "income",
  "category": "string",
  "date": null,
  "notes": "string"
}
```

## Assumptions

1. Each transaction belongs to the user who created it — users can only see their own transactions
2. Role is assigned at registration — defaults to `viewer` if not specified
3. Admin credentials must be created manually via `/api/auth/register` with `"role": "admin"`
4. Categories are free-text — no predefined list, users can use any category name
5. Amounts must be positive floats — negative amounts are rejected
6. Date field is required when creating a transaction — format: `YYYY-MM-DD`
7. SQLite was not used — PostgreSQL was chosen for production readiness and resume signal
