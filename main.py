import logging
from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from config import settings
from db import SessionLocal, Reading

# Configure standard Python logging format and verbosity level
logging.basicConfig(level=settings.log_level,
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")
# Create a dedicated logger instance named 'api'
log = logging.getLogger("api")
# Initialize the FastAPI application with the title from settings
app = FastAPI(title=settings.app_name)

# Pydantic schema to validate incoming JSON payloads for sensor readings
class ReadingIn(BaseModel):
    sensor_id: str
    temperature: float
# Dependency generator that provides a fresh DB session per request and safely closes it afterward
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Health check endpoint used by Docker and Kubernetes probes to verify the service is alive
@app.get("/health")
def health():
    return {"status": "ok"}
# POST endpoint to receive a new sensor reading and save it into the database
@app.post("/readings")
def add_reading(r: ReadingIn, db: Session = Depends(get_db)):
    # Convert validated Pydantic model to dict and create a SQLAlchemy Reading object
    db.add(Reading(**r.model_dump()))
    # Commit the transaction to persist data in the database
    db.commit()
    # Log the successful operation
    log.info("stored reading from %s", r.sensor_id)
    return {"stored": True}

# GET endpoint to retrieve the 20 most recent sensor readings
@app.get("/readings")
def list_readings(db: Session = Depends(get_db)):
    # Query the database ordered by newest ID first, limited to 20 records
    rows = db.query(Reading).order_by(Reading.id.desc()).limit(20).all()
    # Format the database objects into a clean list of dictionaries for JSON response
    return [{"sensor_id": x.sensor_id, "temperature": x.temperature} for x in rows]

# Placeholder POST endpoint for future AI anomaly detection model
@app.post("/predict")
def predict(r: ReadingIn):
    # Simple rule-based threshold check (returns True if temperature exceeds 35)
    return {"anomaly": r.temperature > 35}
@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")