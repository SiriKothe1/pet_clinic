# 🐾 Pet Clinic API

A demo **Pet Clinic REST API** built with:

| Technology | Role |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | REST framework + auto Swagger UI |
| [SQLAlchemy 2](https://docs.sqlalchemy.org/) | ORM + query layer |
| SQLite | Embedded SQL database (zero setup) |
| [Pydantic v2](https://docs.pydantic.dev/) | Request/response validation |
| [Docker](https://www.docker.com/) | Single-container deployment |

---

## Quick Start

```bash
docker compose up --build
```

Then open → **[http://localhost:8000/docs](http://localhost:8000/docs)** for the interactive Swagger UI.

The database is auto-created and seeded with demo data on first startup.

---

## Data Model

```
owners ──< pets ──< appointments >── vets
                         │
                    medical_records
```

| Table | Description |
|---|---|
| `owners` | Pet owners with contact info |
| `pets` | Pets linked to an owner (dog, cat, bird, …) |
| `vets` | Veterinarians with specialties |
| `appointments` | Scheduled visits — statuses: `scheduled`, `completed`, `cancelled` |
| `medical_records` | One record per completed appointment (diagnosis, treatment, notes) |

---

## API Endpoints

### Owners
| Method | Path | Description |
|---|---|---|
| `POST` | `/owners/` | Create owner |
| `GET` | `/owners/` | List all owners |
| `GET` | `/owners/{id}` | Get owner by ID |
| `PUT` | `/owners/{id}` | Update owner |
| `DELETE` | `/owners/{id}` | Delete owner |
| `GET` | `/owners/{id}/pets` | List pets for an owner |

### Pets
| Method | Path | Description |
|---|---|---|
| `POST` | `/pets/` | Create pet |
| `GET` | `/pets/` | List all pets |
| `GET` | `/pets/{id}` | Get pet by ID |
| `PUT` | `/pets/{id}` | Update pet |
| `DELETE` | `/pets/{id}` | Delete pet |

### Vets
| Method | Path | Description |
|---|---|---|
| `POST` | `/vets/` | Create vet |
| `GET` | `/vets/` | List all vets |
| `GET` | `/vets/{id}` | Get vet by ID |
| `PUT` | `/vets/{id}` | Update vet |
| `DELETE` | `/vets/{id}` | Delete vet |
| `GET` | `/vets/{id}/appointments` | All appointments for a vet |

### Appointments
| Method | Path | Description |
|---|---|---|
| `POST` | `/appointments/` | Book an appointment |
| `GET` | `/appointments/` | List appointments (optional `?status=` filter) |
| `GET` | `/appointments/{id}` | Get appointment |
| `PUT` | `/appointments/{id}/cancel` | Cancel a scheduled appointment |
| `PUT` | `/appointments/{id}/complete` | Mark appointment as completed |

### Medical Records
| Method | Path | Description |
|---|---|---|
| `POST` | `/medical-records/` | Create record (appointment must be completed) |
| `GET` | `/medical-records/appointment/{id}` | Get record for an appointment |
| `GET` | `/medical-records/` | List all records |

---

## Example Requests

```bash
# List all pets
curl http://localhost:8000/pets/

# Book an appointment
curl -X POST http://localhost:8000/appointments/ \
  -H "Content-Type: application/json" \
  -d '{"pet_id": 1, "vet_id": 1, "scheduled_at": "2025-06-01T10:00:00", "reason": "Annual checkup"}'

# Complete an appointment
curl -X PUT http://localhost:8000/appointments/3/complete

# Add a medical record
curl -X POST http://localhost:8000/medical-records/ \
  -H "Content-Type: application/json" \
  -d '{"appointment_id": 3, "diagnosis": "Healthy", "treatment": "None required", "notes": "All good!"}'

# Filter appointments by status
curl "http://localhost:8000/appointments/?status=scheduled"
```

---

## Project Structure

```
pet_clinic/
├── app/
│   ├── main.py              # FastAPI app + startup lifecycle
│   ├── database.py          # SQLAlchemy engine + session
│   ├── seed.py              # Demo data seeder
│   ├── models/              # ORM table definitions
│   │   ├── owner.py
│   │   ├── pet.py
│   │   ├── vet.py
│   │   ├── appointment.py
│   │   └── medical_record.py
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── owner.py
│   │   ├── pet.py
│   │   ├── vet.py
│   │   ├── appointment.py
│   │   └── medical_record.py
│   └── routers/             # FastAPI route handlers
│       ├── owners.py
│       ├── pets.py
│       ├── vets.py
│       ├── appointments.py
│       └── medical_records.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Development (without Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p /data
uvicorn app.main:app --reload
```