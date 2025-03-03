#app.py 

# This file is part of the OPTIMUS project.
# Licensed under CC BY-NC 4.0. Non-commercial use only.
# For more details, see the LICENSE file in the repository.

import os
import sys
import random
import logging
import asyncio
from fastapi import FastAPI, HTTPException, WebSocket, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from datetime import datetime
import json
from dotenv import load_dotenv
from typing import List, Optional, Dict
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy.sql import func
from database import get_db
from starlette.websockets import WebSocketDisconnect
from sqlalchemy.orm import selectinload
from fastapi_socketio import SocketManager
from pathlib import Path

# Pydantic models for request/response validation
class NormCreate(BaseModel):
    text: Optional[str] = None

class NormIdRequest(BaseModel):
    norm_id: int

class NormResponse(BaseModel):
    id: int
    text: str
    valid: bool
    complexity: int
    constitutional: bool

class CaseResponse(BaseModel):
    id: int
    text: str
    norm_id: int
    constitutional: bool
    status: str
    resolved_at: Optional[datetime]

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
socket_manager = SocketManager(app=app)

# Define paths
frontend_path = Path(__file__).parent / "frontend" / "dist"

# Ensure frontend build exists
if not frontend_path.exists():
    raise RuntimeError(f"Frontend build not found at: {frontend_path}")

# Serve the entire frontend dist folder
app.mount("/assets", StaticFiles(directory=str(frontend_path / "assets")), name="assets")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Load environment variables from .env file
load_dotenv()  # This will look for a .env file in the current working directory

# Access the DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is not set! Check your .env file or environment variables.")

print("Loaded environment variables:")
print("DATABASE_URL:", DATABASE_URL)

print("Current working directory:", os.getcwd())

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

from backend.models import Base
from backend.models.norm import Norm
from backend.models.case import Case
from backend.models.society import Society
from backend.models.citizen_pressure import CitizenPressure
from backend.models.analysis import Counter, NormativeInflationModel
from backend.models.activity import Activity
#from backend.models import Base

# Dependency for database sessions
async def get_db():
    async with SessionLocal() as session:
        yield session

# Initialize activities list
activities = []

# Notification System
class NotificationManager:
    def __init__(self):
        self.notifications = []
        self.pending_websocket_events = []
        self.load_notifications()

    def add_notification(self, message: str, type: str = "info"):
        notification = {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "type": type
        }
        self.notifications.append(notification)
        self.save_notifications()

    def get_notifications(self):
        return self.notifications

    def save_notifications(self):
        try:
            notifications_file = "data/notifications.json"
            with open(notifications_file, "w") as f:
                json.dump(self.notifications[-100:], f)
        except Exception as e:
            logging.error(f"Failed to save notifications: {e}")

    def load_notifications(self):
        try:
            notifications_file = "data/notifications.json"
            with open(notifications_file, "r") as f:
                self.notifications = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.notifications = []

    async def broadcast_update(self, event: str, data: dict):
        if socket_manager:
            if len(connected_clients) > 0:  # Prevent emitting to an empty list
                await socket_manager.emit(event, data)
                logging.info(f"📢 WebSocket Event Sent: {event} → {data}")
            else:
                logging.warning("⚠️ No active WebSockets to send event.")
        else:
            logging.warning("⚠️ No active WebSocket! Storing event for later.")
            self.pending_websocket_events.append((event, data))

notification_manager = NotificationManager()

# WebSocket Connection Management
connected_clients = set()

# Global variable for society
society = None

@app.get("/api/test")
async def test_api():
    return {"message": "API is working"}

@app.on_event("startup")
async def initialize_society():
    global society
    society = Society()
    async with SessionLocal() as session:
        society.initialize_systems(session)
    if hasattr(society, "citizen_pressure"):
        print("✅ `society.citizen_pressure` initialized successfully.")
    else:
        print("❌ `society.citizen_pressure` is missing.")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)

    try:
        while True:
            try:
                data = await websocket.receive_json()
                if data.get("type") == "case_solved":
                    case_id = data.get("case_id")
                    if case_id:
                        for client in list(connected_clients):  # Iterate over a copy to avoid modification issues
                            try:
                                await client.send_json({"event": "case_solved", "data": {"case_id": case_id}})
                            except Exception as e:
                                logging.error(f"❌ Failed to send WebSocket message: {e}")
                                connected_clients.remove(client)  # Remove faulty clients
            except WebSocketDisconnect as e:
                logging.warning(f"⚠️ WebSocket disconnected: {e.code} - {e.reason}")
                break  # Exit loop when client disconnects
            except asyncio.CancelledError:
                logging.info("✅ WebSocket task was cancelled.")
                break
            except Exception as e:
                logging.error(f"❌ Unexpected WebSocket error: {e}")
                break
    finally:
        # Ensure client is removed & socket is closed properly
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        try:
            await websocket.close()
        except Exception as e:
            logging.warning(f"⚠️ Attempted to close an already closed WebSocket: {e}")

# WebSocket Event Handling
@socket_manager.on('connect')
async def handle_connect(sid, environ):
    print("Client connected to WebSocket")

    # Send pending WebSocket events upon connection
    for event, data in notification_manager.pending_websocket_events:
        await socket_manager.emit(event, data)
    notification_manager.pending_websocket_events.clear()

@socket_manager.on('disconnect')
async def handle_disconnect(sid):
    print("Client disconnected")

@socket_manager.on('case_solved')
async def handle_case_solved(sid, data):
    case_id = data.get('case_id')
    print(f"🟢 Case Solved WebSocket event received for case ID: {case_id}")
    if case_id:
        await socket_manager.emit('case_solved', {'case_id': case_id}, broadcast=True)

# API Endpoints

@app.get("/api/activities")
async def get_activities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Activity))
    activities = result.scalars().all()
    return {"activities": [activity.__dict__ for activity in activities]}

@app.post("/api/create_norm", response_model=NormResponse)
async def create_norm(norm_data: NormCreate, db: AsyncSession = Depends(get_db)):
    try:
        norm_text = norm_data.text or f"Law {random.randint(1, 1000)}"
        new_norm = Norm(
            text=norm_text,
            valid=True,
            complexity=random.randint(1, 10),
            constitutional=False
        )
        db.add(new_norm)
        await db.commit()  # Await commit
        await db.refresh(new_norm)  # Await refresh

        # Ensure activities list exists
        if "activities" in globals():
            activities.append(f"Created Norm #{new_norm.id}: {new_norm.text}")

        # Send notification
        if "notification_manager" in globals():
            notification_manager.add_notification(f"New norm created: {new_norm.text}")

        # WebSocket event
        if "socket_manager" in globals():
            await socket_manager.emit('norm_created', {
                'id': new_norm.id,
                'text': new_norm.text,
                'valid': new_norm.valid
            })

        return new_norm
    except Exception as e:
        await db.rollback()  # Await rollback
        logging.error(f"Error creating norm: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/get_norms", response_model=List[NormResponse])
async def get_norms(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Norm).order_by(Norm.created_at))  # Trier par date de création
        norms = result.scalars().all()  # Extraire les objets Norm
        return norms
    except Exception as e:
        logging.error(f"Error fetching norms: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve norms.")

@app.post("/api/check_constitutionality")
async def check_constitutionality(request: NormIdRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Norm).where(Norm.id == request.norm_id))
        norm = result.scalars().first()

        if not norm:
            raise HTTPException(status_code=404, detail=f"Norm with ID {request.norm_id} not found")

        return {
            "id": norm.id,
            "text": norm.text,
            "valid": norm.valid,
            "complexity": norm.complexity
        }
    except Exception as e:
        logging.error(f"Error checking constitutionality: {e}")
        raise HTTPException(status_code=500, detail="Failed to check constitutionality.")

@app.post("/api/simulate_day")
async def simulate_day():
    try:
        # Ensure actions_completed exists
        actions_completed = globals().get("actions_completed")
        if not actions_completed or not isinstance(actions_completed, dict):
            raise HTTPException(status_code=500, detail="`actions_completed` is not properly initialized.")

        if not all(actions_completed.values()):
            raise HTTPException(
                status_code=400,
                detail="Both actions must be completed to pass the day"
            )

        actions_completed["political"] = False
        actions_completed["judicial"] = False

        # Ensure society is defined
        society = globals().get("society")
        if not society:
            raise HTTPException(status_code=500, detail="`society` is not properly initialized.")

        society.iteration += 1

        # Ensure activities exists before appending
        if "activities" in globals():
            activities.append(f"Day {society.iteration} progressed successfully!")

        return {"message": f"Day {society.iteration} simulated successfully!"}
    except Exception as e:
        logging.error(f"Error simulating day: {e}")
        raise HTTPException(status_code=500, detail="Failed to simulate day.")

@app.post("/api/generate_citizen_cases")
async def generate_citizen_cases(db: AsyncSession = Depends(get_db)):
    try:
        # Fetch valid norms
        result = await db.execute(select(Norm).where(Norm.valid == True))
        valid_norms = result.scalars().all()

        if not valid_norms:
            logging.warning("⚠️ No valid norms found.")
            return {"message": "No valid norm to generate case.", "cases": []}

        # Verify citizen_pressure initialization
        if not hasattr(society, "citizen_pressure") or society.citizen_pressure is None:
            raise HTTPException(status_code=500, detail="`citizen_pressure` is not initialized.")

        # Generate cases
        generated_cases = await society.citizen_pressure.generate_cases_from_norms(db, valid_norms)

        # Format response
        return {
            "message": f"Generated {len(generated_cases)} citizen cases",
            "cases": [
                {
                    "id": case.id,
                    "text": case.text,
                    "norm_id": case.norm_id
                } for case in generated_cases
            ]
        }
    except Exception as e:
        await db.rollback()
        logging.error(f"❌ Error generating citizen cases: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate citizen cases.")

@app.get("/api/get_all_cases")
async def get_all_cases(db: AsyncSession = Depends(get_db)):
    try:
        # Ensure Norm is preloaded to avoid lazy-loading issues
        result = await db.execute(select(Case).options(selectinload(Case.norm)))
        cases = result.scalars().all()

        # Format the cases for response
        formatted_cases = [{
            "id": case.id,
            "text": case.text,
            "norm_id": case.norm.id if case.norm else None,
            "constitutional": case.constitutional,
            "status": case.status,
            "created_at": case.created_at.isoformat() if case.created_at else None,
            "resolved_at": case.resolved_at.isoformat() if case.resolved_at else None,
            "decision": case.decision if hasattr(case, "decision") else "Unknown"

        } for case in cases]

        return {"total": len(formatted_cases), "cases": formatted_cases}
    except Exception as e:
        logging.error(f"Error retrieving all cases: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve cases.")

@app.get("/api/get_pending_cases")
async def get_pending_cases(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Case).filter(Case.status == "pending"))
        pending_cases_list = result.scalars().all()

        # Debugging log
        logging.info(f"📌 Returning {len(pending_cases_list)} pending cases")

        return {"pending_cases": pending_cases_list}  # Ensure this key matches frontend
    except Exception as e:
        logging.error(f"❌ Error retrieving pending cases: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve pending cases.")

@app.get("/api/get_solved_cases")
async def get_solved_cases(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Case).filter(Case.status == "solved"))
        solved_cases_list = result.scalars().all()

        # Convert cases to a list of dictionaries and ensure "decision" is included
        solved_cases_with_decision = [
            {
                "id": case.id,
                "text": case.text,
                "norm_id": case.norm_id,
                "created_at": case.created_at.isoformat() if case.created_at else None,
                "resolved_at": case.resolved_at.isoformat() if case.resolved_at else "Pending",
                "status": case.status,
                "decision": case.decision if hasattr(case, "decision") else "Unknown"
            }
            for case in solved_cases_list
        ]

        # Debugging log
        logging.info(f"📌 Returning {len(solved_cases_with_decision)} solved cases with decisions")

        return {"solved_cases": solved_cases_with_decision}  # Matches frontend expectation
    except Exception as e:
        logging.error(f"❌ Error retrieving solved cases: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve solved cases.")

@app.get("/api/get_notifications")
async def get_notifications():
    try:
        # Ensure notification_manager exists
        notification_manager = globals().get("notification_manager")
        if not notification_manager:
            raise HTTPException(status_code=500, detail="Notification manager is not initialized.")

        notifications = notification_manager.get_notifications()
        return notifications
    except Exception as e:
        logging.error(f"Error retrieving notifications: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve notifications.")

@app.get("/api/get_activities")
async def get_activities():
    try:
        return activities  # Return all logged activities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Define a request model for `mark_unconstitutional`
class NormIDRequest(BaseModel):
    norm_id: int

@app.post("/api/mark_unconstitutional")
async def mark_unconstitutional(request: NormIDRequest, db: AsyncSession = Depends(get_db)):
    try:
        norm_id = request.norm_id  # Extract norm_id from the request body

        # Use async query for compatibility
        result = await db.execute(select(Norm).where(Norm.id == norm_id))
        norm = result.scalars().first()

        if not norm:
            raise HTTPException(status_code=404, detail=f"Norm with ID {norm_id} not found")

        # Update and commit changes
        norm.constitutional = False
        norm.valid = False
        await db.commit()
        await db.refresh(norm)  # Ensure session is updated

        return {"message": f"Norm with ID {norm_id} marked as unconstitutional"}
    except Exception as e:
        try:
            await db.rollback()  # Prevent partial commits
        except Exception as rollback_error:
            logging.error(f"Rollback failed: {rollback_error}")

        logging.error(f"Error marking norm as unconstitutional: {e}")
        raise HTTPException(status_code=500, detail="Failed to mark norm as unconstitutional.")

@app.post("/api/solve_case/{case_id}")
async def solve_case(case_id: int, decision: str = Query(..., regex="^(Accepted|Rejected)$"), db: AsyncSession = Depends(get_db)):
    try:
        # Use select() instead of db.get() for async compatibility
        result = await db.execute(select(Case).where(Case.id == case_id))
        case = result.scalars().first()

        if not case:
            raise HTTPException(status_code=404, detail=f"Case with ID {case_id} not found")

        # Update and commit changes
        case.status = "solved"
        case.resolved_at = datetime.utcnow()  # Use UTC timestamp
        case.decision = decision

        await db.commit()
        await db.refresh(case)  # Ensure session is updated

        # Ensure activities list exists
        activities = globals().get("activities", [])
        activities.append(f"Solved Case #{case.id}: {case.text}")

        # Ensure notification manager exists before using it
        notification_manager = globals().get("notification_manager")
        if notification_manager:
            notification_manager.add_notification(f"Case #{case.id} has been solved.")

        # Ensure socket manager exists before emitting event
        socket_manager = globals().get("socket_manager")
        if socket_manager:
            await socket_manager.emit('case_solved', {'case_id': case.id, 'decision': decision})

        return {"message": f"Case {case_id} solved as {decision}"}
    except Exception as e:
        try:
            await db.rollback()  # Prevent partial commits
        except Exception as rollback_error:
            logging.error(f"Rollback failed: {rollback_error}")

        logging.error(f"Error solving case: {e}")
        raise HTTPException(status_code=500, detail="Failed to solve case.")

@app.get("/api/get_all_norms", response_model=List[NormResponse])
async def get_all_norms(db: AsyncSession = Depends(get_db)):
    try:
        # Ensure relationships (like cases) are loaded to prevent lazy-loading issues
        result = await db.execute(select(Norm).options(selectinload(Norm.cases)))
        norm_list = result.scalars().all()
        return norm_list
    except Exception as e:
        logging.error(f"Error retrieving norms: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve norms.")

@app.get("/api/get_valid_norms", response_model=List[NormResponse])
async def get_valid_norms(db: AsyncSession = Depends(get_db)):
    try:
        # Ensure relationships (like cases) are loaded to prevent lazy-loading issues
        result = await db.execute(select(Norm).options(selectinload(Norm.cases)).filter(Norm.valid == True))
        valid_norms_list = result.scalars().all()
        return valid_norms_list
    except Exception as e:
        logging.error(f"Error retrieving valid norms: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve valid norms.")

@app.get("/api/get_invalid_norms", response_model=List[NormResponse])
async def get_invalid_norms(db: AsyncSession = Depends(get_db)):
    try:
        # Ensure relationships (like cases) are loaded to prevent lazy-loading issues
        result = await db.execute(select(Norm).options(selectinload(Norm.cases)).filter(Norm.valid == False))
        invalid_norms_list = result.scalars().all()
        return invalid_norms_list
    except Exception as e:
        logging.error(f"Error retrieving invalid norms: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve invalid norms.")

@app.get("/api/get_statistics")
async def get_statistics(db: AsyncSession = Depends(get_db)):
    try:
        # Optimize Norms query: Fetch all counts in one query
        norm_counts = await db.execute(
            select(
                func.count(Norm.id),
                func.count().filter(Norm.valid == True),
                func.count().filter(Norm.valid == False),
            )
        )
        total_norms, valid_norms, invalid_norms = norm_counts.one()

        # Optimize Cases query: Fetch all counts in one query
        case_counts = await db.execute(
            select(
                func.count(Case.id),
                func.count().filter(Case.status == "pending"),
                func.count().filter(Case.status == "solved"),
            )
        )
        total_cases, pending_cases, solved_cases = case_counts.one()

        # Prepare optimized statistics
        stats = {
            "norms": {
                "total": total_norms,
                "valid": valid_norms,
                "invalid": invalid_norms
            },
            "cases": {
                "total": total_cases,
                "pending": pending_cases,
                "solved": solved_cases
            }
        }
        return stats
    except Exception as e:
        logging.error(f"Error retrieving statistics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics.")

@app.get("/api/get_normative_inflation")
async def get_normative_inflation(db: AsyncSession = Depends(get_db)):
    try:
        # Create an instance of NormativeInflationModel
        model = NormativeInflationModel()

        # Call the instance method
        inflation_data = await model.calculate_inflation(db)

        return JSONResponse(content={"inflation_data": inflation_data})
    except Exception as e:
        logging.error(f"Error retrieving normative inflation: {e}")
        return JSONResponse(content={"error": "Failed to retrieve normative inflation"}, status_code=500)

@app.get("/{full_path:path}")
async def serve_vue(full_path: str):
    """Serve Vue's frontend while handling history mode"""
    
    requested_file = frontend_path / full_path

    # 🔴 1. Serve API routes normally (prevent Vue from hijacking them)
    if full_path.startswith("api/"):
        return JSONResponse(status_code=404, content={"detail": "API Not Found"})

    # 🟢 2. Serve static files (JS, CSS, images)
    if requested_file.exists() and requested_file.is_file():
        return FileResponse(requested_file)

    # 🔵 3. Redirect all other routes to Vue's `index.html`
    return FileResponse(frontend_path / "index.html")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
