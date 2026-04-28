"""
Seed script — inserts demo data on first startup (skips if data already exists).
"""
from datetime import date, datetime, timezone, timedelta
from sqlalchemy.orm import Session

from app.models.owner import Owner
from app.models.pet import Pet
from app.models.vet import Vet
from app.models.appointment import Appointment, AppointmentStatus
from app.models.medical_record import MedicalRecord


def seed(db: Session) -> None:
    if db.query(Owner).count() > 0:
        return  # already seeded

    # --- Owners ---
    alice = Owner(first_name="Alice", last_name="Walker", email="alice@example.com",
                  phone="555-1001", address="10 Elm St, Springfield")
    bob = Owner(first_name="Bob", last_name="Smith", email="bob@example.com",
                phone="555-1002", address="22 Oak Ave, Shelbyville")
    carol = Owner(first_name="Carol", last_name="Jones", email="carol@example.com",
                  phone="555-1003", address="7 Pine Rd, Ogdenville")
    db.add_all([alice, bob, carol])
    db.flush()

    # --- Pets ---
    buddy = Pet(name="Buddy", species="dog", breed="Golden Retriever",
                date_of_birth=date(2019, 3, 15), owner_id=alice.id)
    whiskers = Pet(name="Whiskers", species="cat", breed="Siamese",
                   date_of_birth=date(2020, 7, 4), owner_id=alice.id)
    rex = Pet(name="Rex", species="dog", breed="German Shepherd",
              date_of_birth=date(2018, 11, 20), owner_id=bob.id)
    tweety = Pet(name="Tweety", species="bird", breed="Canary",
                 date_of_birth=date(2021, 1, 10), owner_id=carol.id)
    db.add_all([buddy, whiskers, rex, tweety])
    db.flush()

    # --- Vets ---
    dr_patel = Vet(first_name="Priya", last_name="Patel", specialty="General Practice",
                   email="priya.patel@clinic.com")
    dr_nguyen = Vet(first_name="David", last_name="Nguyen", specialty="Surgery",
                    email="david.nguyen@clinic.com")
    db.add_all([dr_patel, dr_nguyen])
    db.flush()

    # --- Appointments ---
    now = datetime.now(timezone.utc)
    appt1 = Appointment(pet_id=buddy.id, vet_id=dr_patel.id,
                        scheduled_at=now - timedelta(days=10),
                        reason="Annual checkup", status=AppointmentStatus.completed)
    appt2 = Appointment(pet_id=rex.id, vet_id=dr_nguyen.id,
                        scheduled_at=now - timedelta(days=5),
                        reason="Limping on left hind leg", status=AppointmentStatus.completed)
    appt3 = Appointment(pet_id=whiskers.id, vet_id=dr_patel.id,
                        scheduled_at=now + timedelta(days=3),
                        reason="Vaccination booster", status=AppointmentStatus.scheduled)
    appt4 = Appointment(pet_id=tweety.id, vet_id=dr_patel.id,
                        scheduled_at=now + timedelta(days=7),
                        reason="Wing feather concern", status=AppointmentStatus.scheduled)
    db.add_all([appt1, appt2, appt3, appt4])
    db.flush()

    # --- Medical Records (for completed appointments) ---
    rec1 = MedicalRecord(appointment_id=appt1.id,
                         diagnosis="Healthy — mild tartar buildup",
                         treatment="Dental cleaning recommended",
                         notes="Weight 32 kg. Next checkup in 12 months.")
    rec2 = MedicalRecord(appointment_id=appt2.id,
                         diagnosis="Soft tissue strain",
                         treatment="Anti-inflammatory medication for 7 days, rest",
                         notes="X-ray ruled out fracture. Follow-up in 2 weeks.")
    db.add_all([rec1, rec2])
    db.commit()
    print("✅ Database seeded with demo data.")
