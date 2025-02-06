<<<<<<< HEAD
# This file is part of the OPTIMUS project.
# Licensed under CC BY-NC 4.0. Non-commercial use only.
# For more details, see the LICENSE file in the repository.

import logging
from flask import Flask, jsonify, request, render_template, abort
from models.minioptimus import Society
from datetime import datetime
import json
from flask_cors import CORS
import os
from flask_socketio import SocketIO, emit

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# Ensure the data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Only set absolute paths if we're on PythonAnywhere
if 'PYTHONANYWHERE_SITE' in os.environ:
    app.template_folder = os.path.abspath('templates')
    app.static_folder = os.path.abspath('static')

# Instantiation of the system
society = Society()

# State tracking for day progression
actions_completed = {"political": False, "judicial": False}

# Example activities data for logs
activities = [

]

# Replace the simple notifications list with a more structured system
class NotificationManager:
    def __init__(self):
        self.notifications = []
        self.load_notifications()
    
    def add_notification(self, message, type="info"):
=======
#new fastAPI 

# This file is part of the OPTIMUS project.
# Licensed under CC BY-NC 4.0. Non-commercial use only.
# For more details, see the LICENSE file in the repository.
import os
import random
import logging
import asyncio
from fastapi import FastAPI, HTTPException, WebSocket, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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

# Pydantic models for request/response validation
class NormCreate(BaseModel):
    text: Optional[str] = None

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

app = FastAPI()  # Create FastAPI app
socket_manager = SocketManager(app=app)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Database setup
os.makedirs("data", exist_ok=True)
load_dotenv()

# Database configuration
DATABASE_URL = (
    os.getenv("RENDER_DATABASE_URL") or
    os.getenv("DATABASE_URL") or
    os.getenv("SUPABASE_DATABASE_URL") or
    "sqlite:///data/optimus.db"
)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# Import models after engine creation
from models import Base
from models.norm import Norm
from models.case import Case
from models.society import Society
from models.citizen_pressure import CitizenPressure
from models.analysis import Counter, NormativeInflationModel

# Dependency for database sessions
from sqlalchemy.ext.asyncio import AsyncSession

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
>>>>>>> FastAPIversion
        notification = {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "type": type
        }
        self.notifications.append(notification)
        self.save_notifications()
<<<<<<< HEAD
        
    def get_notifications(self):
        return self.notifications
        
    def save_notifications(self):
        try:
            notifications_file = os.path.join('data', 'notifications.json')
            with open(notifications_file, 'w') as f:
                json.dump(self.notifications[-100:], f)  # Keep last 100 notifications
        except Exception as e:
            logging.error(f"Failed to save notifications: {e}")
            
    def load_notifications(self):
        try:
            notifications_file = os.path.join('data', 'notifications.json')
            with open(notifications_file, 'r') as f:
                self.notifications = json.load(f)
        except FileNotFoundError:
            self.notifications = []

# Replace the global notifications list with an instance
notification_manager = NotificationManager()

# Route principale
@app.route('/')
def home():
    return render_template('index.html')

# Route pour le système judiciaire
@app.route('/judicial')
def judicial_interface():
    return render_template('judicial_interface.html')

# Route pour le système politique
@app.route('/political')
def political_interface():
    return render_template('political_interface.html')

# Route for the General Log interface
@app.route('/general_log')
def general_log():
    return render_template('general_log.html')

# API Endpoint pour créer un nouveau Norm
@app.route('/api/create_norm', methods=['POST'])
def create_norm():
    norm = society.parliament.create_norm()
    actions_completed["political"] = True  # Mark political action as completed
    check_day_progress()
    activities.append(f"Created Norm #{norm.id}: {norm.text}")
    return jsonify({
        "id": norm.id,
        "text": norm.text,
        "valid": norm.valid,
        "complexity": norm.complexity
    })

# API Endpoint pour vérifier la constitutionnalité d'un Norm
@app.route('/api/check_constitutionality', methods=['POST'])
def check_constitutionality():
    norm_id = request.json.get('norm_id')
    norm = next((n for n in society.parliament.norms if n.id == norm_id), None)
    if not norm:
        return jsonify({"error": "Norm not found"}), 404
    society.judicial_system.check_constitutionality(norm)
    actions_completed["judicial"] = True  # Mark judicial action as completed
    check_day_progress()
    activities.append(f"Checked constitutionality for Norm #{norm.id}: {'Valid' if norm.valid else 'Invalid'}")
    return jsonify({
        "id": norm.id,
        "valid": norm.valid,
        "complexity": norm.complexity
    })

# API Endpoint to mark a norm as unconstitutional
@app.route('/api/mark_unconstitutional', methods=['POST'])
def mark_unconstitutional():
    data = request.get_json()
    norm_id = data.get('norm_id')
    norm = next((n for n in society.parliament.norms if n.id == norm_id), None)
    
    if norm:
        norm.invalidate()
        # Emit WebSocket event
        socketio.emit('norm_update', {
            'norm_id': norm_id,
            'valid': False
        })
        return jsonify({
            "success": True,
            "id": norm_id,  # Include the norm_id in the response
            "message": f"Norm #{norm_id} has been marked as unconstitutional."
        })
    return jsonify({"error": "Norm not found"}), 404

# Update the get_notifications endpoint
@app.route('/api/get_notifications', methods=['GET'])
def get_notifications():
    try:
        notification_type = request.args.get('type')
        notifications = notification_manager.get_notifications()
        if notification_type:
            notifications = [n for n in notifications if n['type'] == notification_type]
        return jsonify(notifications)
    except Exception as e:
        logging.error(f"Error getting notifications: {e}")
        return jsonify({"error": "Internal server error"}), 500

# API Endpoint to notify the political system
@app.route('/api/notify_political', methods=['POST'])
def notify_political():
    norm_id = request.json.get('norm_id')
    status = request.json.get('status')
    norm = next((n for n in society.parliament.norms if n.id == norm_id), None)
    if not norm:
        return jsonify({"error": "Norm not found"}), 404
    print(f"Notification sent to Political System: Norm #{norm_id} marked as {status}.")
    return jsonify({"message": f"Political System notified about Norm #{norm_id} status: {status}."})

# API Endpoint for day progression
@app.route('/api/simulate_day', methods=['POST'])
def simulate_day():
    try:
        if not all(actions_completed.values()):
            return jsonify({"error": "Both actions (political and judicial) must be completed to pass the day"}), 400

        actions_completed["political"] = False
        actions_completed["judicial"] = False
        society.iteration += 1  # Advance the day
        activities.append(f"Day {society.iteration} progressed successfully!")
        return jsonify({"message": f"Day {society.iteration} simulated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API Endpoint pour récupérer toutes les norms
@app.route('/api/get_norms', methods=['GET'])
def get_norms():
    norms = [
        {"id": norm.id, "text": norm.text, "valid": norm.valid, "complexity": norm.complexity}
        for norm in society.parliament.norms
    ]
    return jsonify(norms)

# API Endpoint pour récupérer toutes les cases
@app.route('/api/get_cases', methods=['GET'])
def get_cases():
    try:
        cases = society.judicial_system.cases
        logging.info(f"Total cases in system: {len(cases)}")
        
        formatted_cases = [
            {
                "id": case.id,
                "text": case.text,
                "constitutional": case.constitutional,
                "norm_id": case.norm.id if hasattr(case, 'norm') else None
            }
            for case in cases
        ]
        
        logging.info(f"Formatted cases: {formatted_cases}")
        return jsonify({
            "total_cases": len(cases),
            "cases": formatted_cases
        })
    except Exception as e:
        logging.error(f"Error retrieving cases: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/add_test_case', methods=['POST'])
def add_test_case():
    norm = society.parliament.create_norm()
    case = society.judicial_system.create_case(norm)
    return jsonify({"message": "Test case added", "case_id": case.id})

# API Endpoint for today's activities
@app.route('/api/get_activities', methods=['GET'])
def get_activities():
    return jsonify(activities)

# Helper function to check day progress
def check_day_progress():
    if all(actions_completed.values()):
        print(f"Both actions completed. Ready to simulate the next day (Day {society.iteration + 1}).")

# Add this near the top where society is instantiated
@app.route('/api/debug/init_test_cases', methods=['POST'])
def init_test_cases():
    """Debug endpoint to initialize some test cases"""
    try:
        # Create a few test norms and cases
        results = []
        for i in range(3):
            norm = society.parliament.create_norm()
            case = society.judicial_system.create_case(norm)
            results.append({
                "norm_id": norm.id,
                "case_id": case.id if case else None,
                "case_text": case.text if case else None
            })
        
        return jsonify({
            "message": "Test cases initialized",
            "cases_created": results,
            "total_cases": len(society.judicial_system.cases)
        })
    except Exception as e:
        logging.error(f"Error initializing test cases: {e}")
        return jsonify({"error": str(e)}), 500

# Add this new endpoint
@app.route('/api/generate_citizen_cases', methods=['POST'])
def generate_citizen_cases():
    try:
        # Generate daily cases
        generated_cases = society.citizen_pressure.generate_daily_cases()
        
        if generated_cases == "No valid norm to generate case.":
            # Return the specific message if no valid norms exist
            return jsonify({
                "message": "No valid norm to generate case.",
                "cases": []
            }), 200
        
        # If cases are generated, prepare the case details
        case_details = [{
            "id": case.id,
            "text": case.text,
            "norm_id": case.norm.id,
            "constitutional": case.constitutional
        } for case in generated_cases]
        
        return jsonify({
            "message": f"Generated {len(generated_cases)} citizen pressure cases",
            "cases": case_details
        }), 200
    
    except Exception as e:
        logging.error(f"Error generating citizen cases: {e}")
        return jsonify({"error": str(e)}), 500

# Add these new endpoints
@app.route('/api/get_pending_cases', methods=['GET'])
def get_pending_cases():
    try:
        cases = society.judicial_system.pending_cases
        formatted_cases = [{
            "id": case.id,
            "text": case.text,
            "constitutional": case.constitutional,
            "norm_id": case.norm.id if hasattr(case, 'norm') else None
        } for case in cases]
        
        return jsonify({
            "total_pending": len(cases),
            "pending_cases": formatted_cases
        })
    except Exception as e:
        logging.error(f"Error retrieving pending cases: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/get_solved_cases', methods=['GET'])
def get_solved_cases():
    try:
        cases = society.judicial_system.solved_cases
        formatted_cases = [{
            "id": case.id,
            "text": case.text,
            "constitutional": case.constitutional,
            "norm_id": case.norm.id if hasattr(case, 'norm') else None,
            "resolved_at": case.resolved_at
        } for case in cases]
        
        return jsonify({
            "total_solved": len(cases),
            "solved_cases": formatted_cases
        })
    except Exception as e:
        logging.error(f"Error retrieving solved cases: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/solve_case/<int:case_id>', methods=['POST'])
def solve_case(case_id):
    try:
        case = society.judicial_system.solve_case(case_id)
        # Only log the resolution internally, do not notify the political system
        logging.info(f"Case #{case.id} has been resolved by the Judicial System")
        return jsonify({
            "message": f"Case {case_id} has been solved",
            "case": {
                "id": case.id,
                "text": case.text,
                "resolved_at": case.resolved_at
            }
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logging.error(f"Error solving case: {e}")
        return jsonify({"error": str(e)}), 500

# Add this new route
@app.route('/statistics')
def statistics_dashboard():
    return render_template('statistics_dashboard.html')

@app.before_first_request
def init_app():
    # Clear notifications file
    notifications_file = os.path.join('data', 'notifications.json')
    try:
        os.remove(notifications_file)
        logging.info("Cleared old notifications file")
    except FileNotFoundError:
        logging.info("No old notifications file to clear")

socketio = SocketIO(app)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Default to 5000 if $PORT is not set
    app.run(host="0.0.0.0", port=port)
=======

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
            if len(connected_clients) > 0:  # ✅ Prevent emitting to an empty list
                await socket_manager.emit(event, data)
                logging.info(f"📢 WebSocket Event Sent: {event} → {data}")
            else:
                logging.warning("⚠️ No active WebSockets to send event.")
        else:
            logging.warning("⚠️ No active WebSocket! Storing event for later.")
            self.pending_websocket_events.append((event, data))

notification_manager = NotificationManager()

# ✅ WebSocket Connection Management
connected_clients = set()

# Global variable for society
society = None

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
                        for client in list(connected_clients):  # ✅ Iterate over a copy to avoid modification issues
                            try:
                                await client.send_json({"event": "case_solved", "data": {"case_id": case_id}})
                            except Exception as e:
                                logging.error(f"❌ Failed to send WebSocket message: {e}")
                                connected_clients.remove(client)  # ✅ Remove faulty clients
            except WebSocketDisconnect as e:
                logging.warning(f"⚠️ WebSocket disconnected: {e.code} - {e.reason}")
                break  # ✅ Exit loop when client disconnects
            except asyncio.CancelledError:
                logging.info("✅ WebSocket task was cancelled.")
                break
            except Exception as e:
                logging.error(f"❌ Unexpected WebSocket error: {e}")
                break
    finally:
        # ✅ Ensure client is removed & socket is closed properly
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        try:
            await websocket.close()
        except Exception as e:
            logging.warning(f"⚠️ Attempted to close an already closed WebSocket: {e}")

# ✅ WebSocket Event Handling
@socket_manager.on('connect')
async def handle_connect(sid, environ):
    print("Client connected to WebSocket")

    # ✅ Send pending WebSocket events upon connection
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

# Routes for HTML templates
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    # Query total norms
    norm_query = await db.execute(select(func.count()).select_from(Norm))
    total_norms = norm_query.scalar()
    
    # Query valid and invalid norms
    valid_query = await db.execute(select(func.count()).where(Norm.valid == True))
    valid_norms = valid_query.scalar()
    
    invalid_query = await db.execute(select(func.count()).where(Norm.valid == False))
    invalid_norms = invalid_query.scalar()

    # Query total cases
    case_query = await db.execute(select(func.count()).select_from(Case))
    total_cases = case_query.scalar()
    
    # Query resolved and pending cases
    resolved_query = await db.execute(select(func.count()).where(Case.status == "resolved"))
    resolved_cases = resolved_query.scalar()
    
    pending_query = await db.execute(select(func.count()).where(Case.status == "pending"))
    pending_cases = pending_query.scalar()

    # Prepare stats for the template
    stats = {
        "norm_stats": {
            "total": total_norms,
            "valid": valid_norms,
            "invalid": invalid_norms
        },
        "case_stats": {
            "total": total_cases,
            "resolved": resolved_cases,
            "pending": pending_cases
        }
    }

    # Pass stats to the template
    return templates.TemplateResponse("index.html", {"request": request, **stats})

@app.get("/judicial", response_class=HTMLResponse)
async def judicial_interface(request: Request):
    return templates.TemplateResponse("judicial_interface.html", {"request": request})

@app.get("/political", response_class=HTMLResponse)
async def political_interface(request: Request):
    return templates.TemplateResponse("political_interface.html", {"request": request})

@app.get("/view_cases", response_class=HTMLResponse)
async def view_cases(request: Request, db: AsyncSession = Depends(get_db)):
    # Query all cases using async select
    try:
        result = await db.execute(select(Case))
        cases = result.scalars().all()  # This gets the list of cases from the result
        
        return templates.TemplateResponse("cases_view.html", {"request": request, "cases": cases})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/view_norms", response_class=HTMLResponse)
async def view_norms(request: Request, db: AsyncSession = Depends(get_db)):
    # Query all norms asynchronously using select
    try:
        result = await db.execute(select(Norm))
        norms = result.scalars().all()  # Extract norms from the result
        
        return templates.TemplateResponse("view_norms.html", {"request": request, "norms": norms})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/general_log", response_class=HTMLResponse)
async def general_log(request: Request):
    return templates.TemplateResponse("general_log.html", {"request": request})

@app.get("/statistics", response_class=HTMLResponse)
async def statistics_dashboard(request: Request):
    return templates.TemplateResponse("statistics_dashboard.html", {"request": request})

# API Endpoints
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
        await db.commit()  # ✅ Await commit
        await db.refresh(new_norm)  # ✅ Await refresh

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
        await db.rollback()  # ✅ Await rollback
        logging.error(f"Error creating norm: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/get_norms", response_model=List[NormResponse])
async def get_norms(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Norm))  # ✅ Correct async query
        norms = result.scalars().all()  # ✅ Extract actual Norm objects
        return norms
    except Exception as e:
        logging.error(f"Error fetching norms: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve norms.")

@app.post("/api/check_constitutionality")
async def check_constitutionality(norm_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Norm).where(Norm.id == norm_id))  # ✅ Correct async query
        norm = result.scalars().first()  # ✅ Extract the norm object

        if not norm:
            raise HTTPException(status_code=404, detail=f"Norm with ID {norm_id} not found")
        
        return {
            "id": norm.id,
            "text": norm.text,
            "valid": norm.valid,
            "complexity": norm.complexity,
            "constitutional": norm.constitutional
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
        # ✅ Ensure Norm is preloaded to avoid lazy-loading issues
        result = await db.execute(select(Case).options(selectinload(Case.norm)))
        cases = result.scalars().all()

        # ✅ Format the cases for response
        formatted_cases = [{
            "id": case.id,
            "text": case.text,
            "norm_id": case.norm.id if case.norm else None,
            "constitutional": case.constitutional,
            "status": case.status,
            "resolved_at": case.resolved_at.isoformat() if case.resolved_at else None
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
        
        # ✅ Debugging log
        logging.info(f"📌 Returning {len(pending_cases_list)} pending cases")

        return {"pending_cases": pending_cases_list}  # ✅ Ensure this key matches frontend
    except Exception as e:
        logging.error(f"❌ Error retrieving pending cases: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve pending cases.")

@app.get("/api/get_solved_cases")
async def get_solved_cases(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Case).filter(Case.status == "solved"))
        solved_cases_list = result.scalars().all()
        
        # ✅ Debugging log
        logging.info(f"📌 Returning {len(solved_cases_list)} solved cases")

        return {"solved_cases": solved_cases_list}  # ✅ Ensure this key matches frontend
    except Exception as e:
        logging.error(f"❌ Error retrieving solved cases: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve solved cases.")

@app.get("/api/get_notifications")
async def get_notifications():
    try:
        # ✅ Ensure notification_manager exists
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

# ✅ Define a request model for `mark_unconstitutional`
class NormIDRequest(BaseModel):
    norm_id: int

@app.post("/api/mark_unconstitutional")
async def mark_unconstitutional(request: NormIDRequest, db: AsyncSession = Depends(get_db)):
    try:
        norm_id = request.norm_id  # ✅ Extract norm_id from the request body

        # ✅ Use async query for compatibility
        result = await db.execute(select(Norm).where(Norm.id == norm_id))
        norm = result.scalars().first()

        if not norm:
            raise HTTPException(status_code=404, detail=f"Norm with ID {norm_id} not found")

        # ✅ Update and commit changes
        norm.constitutional = False
        norm.valid = False
        await db.commit()
        await db.refresh(norm)  # ✅ Ensure session is updated

        return {"message": f"Norm with ID {norm_id} marked as unconstitutional"}
    except Exception as e:
        try:
            await db.rollback()  # ✅ Prevent partial commits
        except Exception as rollback_error:
            logging.error(f"Rollback failed: {rollback_error}")

        logging.error(f"Error marking norm as unconstitutional: {e}")
        raise HTTPException(status_code=500, detail="Failed to mark norm as unconstitutional.")

@app.post("/api/solve_case/{case_id}")
async def solve_case(case_id: int, db: AsyncSession = Depends(get_db)):
    try:
        # ✅ Use select() instead of db.get() for async compatibility
        result = await db.execute(select(Case).where(Case.id == case_id))
        case = result.scalars().first()

        if not case:
            raise HTTPException(status_code=404, detail=f"Case with ID {case_id} not found")

        # ✅ Update and commit changes
        case.status = "solved"
        case.resolved_at = datetime.utcnow()  # ✅ Use UTC timestamp
        await db.commit()
        await db.refresh(case)  # ✅ Ensure session is updated

        # ✅ Ensure activities list exists
        activities = globals().get("activities", [])
        activities.append(f"Solved Case #{case.id}: {case.text}")

        # ✅ Ensure notification manager exists before using it
        notification_manager = globals().get("notification_manager")
        if notification_manager:
            notification_manager.add_notification(f"Case #{case.id} has been solved.")

        # ✅ Ensure socket manager exists before emitting event
        socket_manager = globals().get("socket_manager")
        if socket_manager:
            await socket_manager.emit('case_solved', {'case_id': case.id})

        return {"message": f"Case with ID {case_id} solved"}
    except Exception as e:
        try:
            await db.rollback()  # ✅ Prevent partial commits
        except Exception as rollback_error:
            logging.error(f"Rollback failed: {rollback_error}")

        logging.error(f"Error solving case: {e}")
        raise HTTPException(status_code=500, detail="Failed to solve case.")
    
@app.get("/api/get_all_norms", response_model=List[NormResponse])
async def get_all_norms(db: AsyncSession = Depends(get_db)):
    try:
        # ✅ Ensure relationships (like cases) are loaded to prevent lazy-loading issues
        result = await db.execute(select(Norm).options(selectinload(Norm.cases)))
        norm_list = result.scalars().all()
        return norm_list
    except Exception as e:
        logging.error(f"Error retrieving norms: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve norms.")

@app.get("/api/get_valid_norms", response_model=List[NormResponse])
async def get_valid_norms(db: AsyncSession = Depends(get_db)):
    try:
        # ✅ Ensure relationships (like cases) are loaded to prevent lazy-loading issues
        result = await db.execute(select(Norm).options(selectinload(Norm.cases)).filter(Norm.valid == True))
        valid_norms_list = result.scalars().all()
        return valid_norms_list
    except Exception as e:
        logging.error(f"Error retrieving valid norms: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve valid norms.")

@app.get("/api/get_invalid_norms", response_model=List[NormResponse])
async def get_invalid_norms(db: AsyncSession = Depends(get_db)):
    try:
        # ✅ Ensure relationships (like cases) are loaded to prevent lazy-loading issues
        result = await db.execute(select(Norm).options(selectinload(Norm.cases)).filter(Norm.valid == False))
        invalid_norms_list = result.scalars().all()
        return invalid_norms_list
    except Exception as e:
        logging.error(f"Error retrieving invalid norms: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve invalid norms.")

@app.get("/api/get_statistics")
async def get_statistics(db: AsyncSession = Depends(get_db)):
    try:
        # ✅ Optimize Norms query: Fetch all counts in one query
        norm_counts = await db.execute(
            select(
                func.count(Norm.id),
                func.count().filter(Norm.valid == True),
                func.count().filter(Norm.valid == False),
            )
        )
        total_norms, valid_norms, invalid_norms = norm_counts.one()

        # ✅ Optimize Cases query: Fetch all counts in one query
        case_counts = await db.execute(
            select(
                func.count(Case.id),
                func.count().filter(Case.status == "pending"),
                func.count().filter(Case.status == "solved"),
            )
        )
        total_cases, pending_cases, solved_cases = case_counts.one()

        # ✅ Prepare optimized statistics
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
        
        return {"inflation_data": inflation_data}
    except Exception as e:
        logging.error(f"Error retrieving normative inflation: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve normative inflation.")
    
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
>>>>>>> FastAPIversion
