from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("app")

from app.database import engine, SessionLocal, Base

# Import all models so SQLAlchemy registers them before create_all
import app.models.owner          # noqa: F401
import app.models.pet            # noqa: F401
import app.models.vet            # noqa: F401
import app.models.appointment    # noqa: F401
import app.models.medical_record # noqa: F401
import app.models.vaccination    # noqa: F401

from app.routers import owners, pets, vets, appointments, medical_records
from app.seed import seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    # Create all tables
    Base.metadata.create_all(bind=engine)
    # Seed demo data
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
    yield
    logger.info("Application shutting down...")


app = FastAPI(
    title="🐾 Pet Clinic API",
    description=(
        "A demo Pet Clinic REST API built with **FastAPI** and **SQLAlchemy**.\n\n"
        "Manage owners, pets, vets, appointments, and medical records.\n\n"
        "Start with `docker compose up --build` and visit `/docs` for the interactive UI."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Register routers
app.include_router(owners.router)
app.include_router(pets.router)
app.include_router(vets.router)
app.include_router(appointments.router)
app.include_router(medical_records.router)


@app.get("/", include_in_schema=False)
def root():
    """Redirect root to Swagger UI."""
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
