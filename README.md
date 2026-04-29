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
- **Lost & Found**: Community platform to report lost or found pets.

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

lost_found_pets
```

| Table | Description |
|---|---|
| `owners` | Pet owners with contact info |
| `pets` | Pets linked to an owner |
| `vaccinations` | Vaccination records linked to a pet |
| `vets` | Veterinarians with specialties |
| `appointments` | Scheduled visits — statuses: `scheduled`, `completed`, `cancelled` |
| `medical_records` | One record per completed appointment |
| `lost_found_pets` | Reports for lost or found pets |

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
| `POST` | `/lost-found/` | Create a lost/found report |
| `GET` | `/lost-found/` | List all reports |
| `PUT` | `/lost-found/{id}` | Update a report (e.g. resolve) |

*(See Swagger UI at `/docs` for full list of Vet, Appointment, and Medical Record endpoints)*

---

## Example Requests

### 1. Create an Owner
```bash
curl -X POST http://localhost:8000/owners/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "phone": "555-0199", "address": "123 Main St"}'
```

### 2. Add a Pet
```bash
curl -X POST http://localhost:8000/pets/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Max", "species": "Dog", "breed": "Beagle", "date_of_birth": "2022-05-10", "owner_id": 1}'
```

### 3. Manage Vaccinations
```bash
# Add a vaccination
curl -X POST http://localhost:8000/pets/1/vaccinations \
  -H "Content-Type: application/json" \
  -d '{"name": "Parvovirus", "date_administered": "2024-04-28", "next_due_date": "2025-04-28"}'

# List vaccinations for a pet
curl http://localhost:8000/pets/1/vaccinations
```

### 4. Schedule & Complete Appointments
```bash
# Book an appointment
curl -X POST http://localhost:8000/appointments/ \
  -H "Content-Type: application/json" \
  -d '{"pet_id": 1, "vet_id": 1, "scheduled_at": "2024-06-15T10:30:00", "reason": "Routine Checkup"}'

# Mark as completed
curl -X PUT http://localhost:8000/appointments/1/complete
```

### 5. Add Medical Records
```bash
curl -X POST http://localhost:8000/medical-records/ \
  -H "Content-Type: application/json" \
  -d '{"appointment_id": 1, "diagnosis": "Healthy", "treatment": "None", "notes": "Heart rate normal."}'
```

### 6. Report a Lost Pet
```bash
curl -X POST http://localhost:8000/lost-found/ \
  -H "Content-Type: application/json" \
  -d '{"report_type": "LOST", "pet_name": "Luna", "species": "cat", "location": "Central Park", "contact_info": "Emma: 555-0122"}'
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