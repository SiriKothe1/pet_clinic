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

## Features
- **Owner Management**: Track contact details for pet owners.
- **Pet Management**: Manage pets, including species, breed, and birth dates.
- **Vaccinations**: Track vaccination history and upcoming boosters per pet.
- **Vets & Appointments**: Schedule, complete, or cancel appointments with veterinarians.
- **Medical Records**: Maintain detailed medical history for completed appointments.
- **Logging**: Comprehensive logging for debugging and monitoring.

---

## Docker Setup

### 1. Build the Docker Image
To build the container image locally:
```bash
docker build -t pet-clinic-api .
```

### 2. Run the Container
To run the application on port 8000 with persistent data (mounting a local `./data` folder):
```bash
mkdir -p ./data
docker run -p 8000:8000 -v $(pwd)/data:/data pet-clinic-api
```

### 3. Using Docker Compose (Recommended)
Launch the API and a persistent data volume in one command:
```bash
docker compose up --build
```

Once running, visit → **[http://localhost:8000/docs](http://localhost:8000/docs)** for the interactive Swagger UI.

---

## Data Model

```
owners ──< pets ──< appointments >── vets
           │            │
           └──< vaccinations
                        │
                  medical_records
```

| Table | Description |
|---|---|
| `owners` | Pet owners with contact info |
| `pets` | Pets linked to an owner |
| `vaccinations` | Vaccination records linked to a pet |
| `vets` | Veterinarians with specialties |
| `appointments` | Scheduled visits — statuses: `scheduled`, `completed`, `cancelled` |
| `medical_records` | One record per completed appointment |

---

## API Endpoints

### Pets & Vaccinations
| Method | Path | Description |
|---|---|---|
| `POST` | `/pets/` | Create pet |
| `GET` | `/pets/` | List all pets |
| `GET` | `/pets/{id}` | Get pet by ID |
| `PUT` | `/pets/{id}` | Update pet |
| `DELETE` | `/pets/{id}` | Delete pet |
| `GET` | `/pets/{id}/vaccinations` | List all vaccinations for a pet |
| `POST` | `/pets/{id}/vaccinations` | Add a vaccination to a pet |
| `PUT` | `/pets/{id}/vaccinations/{v_id}`| Update a vaccination record |
| `DELETE`| `/pets/{id}/vaccinations/{v_id}`| Delete a vaccination record |

### Owners
| Method | Path | Description |
|---|---|---|
| `POST` | `/owners/` | Create owner |
| `GET` | `/owners/` | List all owners |
| `GET` | `/owners/{id}/pets` | List pets for an owner |

*(See Swagger UI at `/docs` for full list of Vet, Appointment, and Medical Record endpoints)*

---

## Example Requests

### Managing Pets
```bash
# Create a new pet for Owner ID 1
curl -X POST http://localhost:8000/pets/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Buddy", "species": "Dog", "breed": "Golden Retriever", "owner_id": 1}'

# List all pets
curl http://localhost:8000/pets/

# Update a pet's breed
curl -X PUT http://localhost:8000/pets/1 \
  -H "Content-Type: application/json" \
  -d '{"breed": "Golden Retriever Booster"}'
```

### Managing Vaccinations
```bash
# Add a Rabies vaccination to Pet ID 1
curl -X POST http://localhost:8000/pets/1/vaccinations \
  -H "Content-Type: application/json" \
  -d '{"name": "Rabies", "date_administered": "2024-01-01", "next_due_date": "2025-01-01"}'

# List all vaccinations for Pet ID 1
curl http://localhost:8000/pets/1/vaccinations
```

---

## Development (without Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p /data
uvicorn app.main:app --reload
```