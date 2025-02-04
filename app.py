# This file is part of the OPTIMUS project.
# Licensed under CC BY-NC 4.0. Non-commercial use only.
# For more details, see the LICENSE file in the repository.
import os
import random
import logging
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit
import json
from datetime import datetime
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)  # ✅ Define Flask app first
CORS(app, resources={r"/*": {"origins": "*"}})

# ✅ Set database configuration BEFORE initializing db
os.makedirs("data", exist_ok=True)

load_dotenv()  # ✅ Charge .env

# ✅ Essaye plusieurs noms de variables d'env pour être sûr qu'elle est trouvée
app.config["SQLALCHEMY_DATABASE_URI"] = (
    os.getenv("RENDER_DATABASE_URL") or  # 🔄 Sur Render
    os.getenv("DATABASE_URL") or  # 🔄 Peut être utilisé sur d'autres plateformes
    os.getenv("SUPABASE_DATABASE_URL") or  # 🔄 Si tu reviens à Supabase
    "sqlite:///data/optimus.db"  # 🔄 Fallback pour éviter une erreur si rien n'est trouvé
)

# ✅ Assurez-vous que SQLAlchemy ne spamme pas les logs
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Import db AFTER setting config
from models import db
db.init_app(app)  # ✅ Now db.init_app(app) works because config is set

migrate = Migrate(app, db)  # ✅ Initialize Flask-Migrate after db

# ✅ Ensure tables exist at startup
with app.app_context():
    try:
        db.create_all()  # Crée les tables si elles n'existent pas
        print("✅ Base de données PostgreSQL initialisée avec succès !")
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation de la base PostgreSQL : {e}")
print("DEBUG: SQLALCHEMY_DATABASE_URI =", app.config["SQLALCHEMY_DATABASE_URI"])

# ✅ Import models AFTER initializing db to prevent circular imports
from models.norm import Norm
from models.case import Case
from models.society import Society
from models.analysis import Counter, NormativeInflationModel

# Notification System
class NotificationManager:
    def __init__(self):
        self.notifications = []
        self.pending_websocket_events = []
        self.load_notifications()

    def add_notification(self, message, type="info"):
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
            notifications_file = os.path.join('data', 'notifications.json')
            with open(notifications_file, 'w') as f:
                json.dump(self.notifications[-100:], f)
        except Exception as e:
            logging.error(f"Failed to save notifications: {e}")

    def load_notifications(self):
        try:
            notifications_file = os.path.join('data', 'notifications.json')
            with open(notifications_file, 'r') as f:
                self.notifications = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.notifications = []

    async def broadcast_update(self, event, data):
        if socketio:
            socketio.emit(event, data)
            logging.info(f"📢 WebSocket Event Sent: {event} → {data}")
        else:
            logging.warning("⚠️ No active WebSocket! Storing event for later.")
            self.pending_websocket_events.append((event, data))

socketio = SocketIO(app, cors_allowed_origins="*")  # Allow CORS

notification_manager = NotificationManager()

# Instantiation of the system
society = Society()

# State tracking for day progression
actions_completed = {"political": False, "judicial": False}

# Example activities data for logs
activities = []

@socketio.on('connect')
def handle_connect():
    print("Client connected to WebSocket")

    # Send pending WebSocket events
    for event, data in notification_manager.pending_websocket_events:
        socketio.emit(event, data)
    
    # Clear queue
    notification_manager.pending_websocket_events.clear()

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('case_solved')
def handle_case_solved(data):
    case_id = data.get('case_id')
    print(f"🟢 Case Solved WebSocket event received for case ID: {case_id}")
    if case_id:
        emit('case_solved', {'case_id': case_id}, broadcast=True)

# Routes

@app.route('/ws')
def websocket():
    return "WebSocket route is active"

@app.route('/view_cases')
def view_cases():
    cases = Case.query.all()  # Query all cases
    return render_template('cases_view.html', cases=cases)

@app.route('/view_norms', methods=['GET'])
def view_norms():
    return render_template('view_norms.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/judicial')
def judicial_interface():
    return render_template('judicial_interface.html')

@app.route('/political')
def political_interface():
    return render_template('political_interface.html')

@app.route('/general_log')
def general_log():
    return render_template('general_log.html')

@app.route('/statistics')
def statistics_dashboard():
    return render_template('statistics_dashboard.html')

# API Endpoints
@app.route('/api/create_norm', methods=['POST'])
def create_norm():
    try:
        data = request.get_json() if request.is_json else {'text': None}
        norm_text = data.get('text')

        if not norm_text:
            norm_text = f"Law {random.randint(1, 1000)}"

        new_norm = Norm(text=norm_text, valid=True, complexity=random.randint(1, 10), constitutional=False)  # Set constitutional attribute
        db.session.add(new_norm)
        db.session.commit()

        activities.append(f"Created Norm #{new_norm.id}: {new_norm.text}")
        notification_manager.add_notification(f"New norm created: {new_norm.text}")

        socketio.emit('norm_created', {'id': new_norm.id, 'text': new_norm.text, 'valid': new_norm.valid})
        return jsonify(new_norm.to_dict())
    except Exception as e:
        logging.error(f"Error creating norm: {e}")
        db.session.rollback()
        return jsonify({"error": "Failed to create norm"}), 500

@app.route('/api/get_norms', methods=['GET'])
def get_norms():
    try:
        norms = Norm.query.all()
        if not norms:
            return jsonify([])  # Return an empty list if no norms exist
        return jsonify([norm.to_dict() for norm in norms])
    except Exception as e:
        logging.error(f"Error fetching norms: {e}")
        return jsonify({"error": "Failed to fetch norms"}), 500

@app.route('/api/check_constitutionality', methods=['POST'])
def check_constitutionality():
    try:
        # Récupérer l'ID de la norme depuis la requête JSON
        data = request.get_json()
        norm_id = data.get('norm_id')

        # Vérifier si l'ID est valide
        if not norm_id:
            return jsonify({"error": "Missing norm_id"}), 400

        # Rechercher la norme dans la base de données
        norm = Norm.query.get(norm_id)

        if not norm:
            return jsonify({"error": f"Norm with ID {norm_id} not found"}), 404

        # Retourner l'état de constitutionnalité de la norme
        return jsonify({
            "id": norm.id,
            "text": norm.text,
            "valid": norm.valid,  # ✅ true = constitutionnelle, false = inconstitutionnelle
            "complexity": norm.complexity,
            "constitutional": norm.constitutional
        }), 200

    except Exception as e:
        logging.error(f"Error checking norm constitutionality: {e}")
        return jsonify({"error": "Internal server error"}), 500

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

@app.route('/api/simulate_day', methods=['POST'])
def simulate_day():
    try:
        if not all(actions_completed.values()):
            return jsonify({"error": "Both actions must be completed to pass the day"}), 400
        actions_completed["political"] = False
        actions_completed["judicial"] = False
        society.iteration += 1
        activities.append(f"Day {society.iteration} progressed successfully!")
        return jsonify({"message": f"Day {society.iteration} simulated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/get_activities', methods=['GET'])
def get_activities():
    try:
        return jsonify({"activities": activities}), 200
    except Exception as e:
        logging.error(f"Error fetching activities: {e}")
        return jsonify({"error": "Failed to fetch activities"}), 500

@app.route('/api/generate_citizen_cases', methods=['POST'])
def generate_citizen_cases():
    try:
        with app.app_context():  # ✅ Ensure Flask app context is active
            valid_norms = Norm.query.filter_by(valid=True).all()

            if not valid_norms:
                return jsonify({"message": "No valid norm to generate case.", "cases": []}), 200

            generated_cases = society.citizen_pressure.generate_cases_from_norms(valid_norms)

            for case in generated_cases:
                db.session.add(case)  # ✅ Ensure case is added to session
            db.session.commit()  # ✅ Commit to DB

            # ✅ Fetch cases again from DB after commit
            persisted_cases = Case.query.order_by(Case.id.desc()).limit(len(generated_cases)).all()

            case_details = [{
                "id": case.id,
                "text": case.text,
                "norm": case.norm.to_dict() if case.norm else None,  # ✅ Ensure norm is serialized
                "constitutional": case.constitutional
            } for case in persisted_cases]

            return jsonify({
                "message": f"Generated {len(case_details)} citizen pressure cases",
                "cases": case_details
            }), 200

    except Exception as e:
        logging.error(f"Error generating citizen cases: {e}")
        db.session.rollback()  # ✅ Prevents half-complete transactions
        return jsonify({"error": str(e)}), 500

@app.route('/api/get_pending_cases', methods=['GET'])
def get_pending_cases():
    try:
        with app.app_context():  # ✅ Ensure Flask app context
            cases = Case.query.filter(Case.status == 'pending').all()  # Filter by 'pending'

            formatted_cases = [{
                "id": case.id,
                "text": case.text,
                "norm_id": case.norm.id,
                "norm": case.norm.to_dict() if case.norm else None,  # ✅ Ensure norm is serialized
                "constitutional": case.constitutional,
                "resolved_at": "Pending"
            } for case in cases]

            return jsonify({
                "total": len(formatted_cases),
                "pending_cases": formatted_cases
            })
    except Exception as e:
        logging.error(f"Error retrieving pending cases: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/get_solved_cases', methods=['GET'])
def get_solved_cases():
    try:
        solved_cases = Case.query.filter(Case.status == 'solved').all()  # Filter by 'solved'
        formatted_cases = [{
            "id": case.id,
            "text": case.text,
            "norm_id": case.norm.id,
            "constitutional": case.constitutional,
            "resolved_at": case.resolved_at.strftime("%Y-%m-%d") if case.resolved_at else None            if case.resolved_at else None
        } for case in solved_cases]
        return jsonify({
            "total": len(formatted_cases),
            "solved_cases": formatted_cases
        })
    except Exception as e:
        logging.error(f"Error retrieving solved cases: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/get_all_cases', methods=['GET'])
def get_all_cases():
    try:
        cases = Case.query.all()
        formatted_cases = [{
            "id": case.id,
            "text": case.text,
            "norm_id": case.norm.id,
            "constitutional": case.constitutional,
            "status": case.status,
            "resolved_at": case.resolved_at.isoformat() if case.resolved_at else None
        } for case in cases]
        return jsonify({
            "total": len(formatted_cases),
            "cases": formatted_cases
        })
    except Exception as e:
        logging.error(f"Error retrieving all cases: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/mark_unconstitutional', methods=['POST'])
def mark_unconstitutional():
    try:
        # Fetch data from the request
        data = request.get_json()
        norm_id = data.get('norm_id')

        # Query for the norm by ID
        norm = Norm.query.get(norm_id)

        # If the norm is not found, return a 404 error
        if not norm:
            return jsonify({"error": "Norm not found"}), 404

        # Invalidate the norm and commit the change
        norm.valid = False
        db.session.commit()

        # Emit WebSocket event
        socketio.emit('norm_update', {
            'norm_id': norm_id,
            'valid': False
        })

        return jsonify({
            "message": f"Norm #{norm.id} has been marked as unconstitutional."
        }), 200
    except Exception as e:
        logging.error(f"Error marking norm unconstitutional: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/solve_case/<int:case_id>', methods=['POST'])
def solve_case(case_id):
    try:
        # Validate the case ID
        if not isinstance(case_id, int) or case_id <= 0:
            logging.error(f"Invalid case ID provided: {case_id}")
            return jsonify({"error": "Invalid case ID"}), 400

        # Query the database directly for the case
        case = Case.query.get(case_id)

        if not case:
            logging.error(f"Case with ID {case_id} not found in the database")
            return jsonify({"error": "Case not found"}), 404

        # Mark the case as solved
        case.resolved_at = datetime.now()
        case.status = 'solved'  # Ensure the status is updated
        db.session.commit()

        # Emit WebSocket event to update front-end
        socketio.emit('case_solved', {
            "id": case.id,
            "text": case.text,
            "resolved_at": case.resolved_at.isoformat(),
        })

        logging.info(f"Case #{case.id} has been resolved successfully")
        notification_manager.add_notification(f"Case {case.id} has been resolved")

        return jsonify({
            "message": f"Case {case.id} has been solved",
            "case": {
                "id": case.id,
                "text": case.text,
                "resolved_at": case.resolved_at.isoformat()
            }
        }), 200
    except Exception as e:
        logging.error(f"Error solving case ID {case_id}: {e}")
        db.session.rollback()  # Rollback any partial transaction
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/api/get_all_norms', methods=['GET'])
def get_all_norms():
    norms = Norm.query.all()
    return jsonify({
        "norms": [
            {
                "id": norm.id,
                "text": norm.text,
                "complexity": norm.complexity,
                "valid": norm.valid
            }
            for norm in norms
        ]
    })

@app.route('/api/get_valid_norms', methods=['GET'])
def get_valid_norms():
    norms = Norm.query.filter_by(valid=True).all()
    return jsonify({
        "valid_norms": [
            {
                "id": norm.id,
                "text": norm.text,
                "complexity": norm.complexity,
                "valid": norm.valid
            }
            for norm in norms
        ]
    })

@app.route('/api/get_invalid_norms', methods=['GET'])
def get_invalid_norms():
    norms = Norm.query.filter_by(valid=False).all()
    return jsonify({
        "invalid_norms": [
            {
                "id": norm.id,
                "text": norm.text,
                "complexity": norm.complexity,
                "valid": norm.valid
            }
            for norm in norms
        ]
    })
@app.route('/api/get_statistics', methods=['GET'])
def fetch_statistics():
    counter = Counter()
    counter.update_counts()
    return jsonify(counter.to_dict())

@app.route('/api/get_normative_inflation', methods=['GET'])
def get_normative_inflation():
    model = NormativeInflationModel()
    model.update_metrics()
    return jsonify(model.to_dict())

@app.before_request
def init_app():
    with app.app_context():
        cases = Case.query.all()
        for case in cases:
            if case.resolved_at:
                case.status = 'solved'
            else:
                case.status = 'pending'
        db.session.commit()

    # Clear notifications file
    notifications_file = os.path.join('data', 'notifications.json')
    try:
        os.remove(notifications_file)
        logging.info("Cleared old notifications file")
    except FileNotFoundError:
        logging.info("No old notifications file to clear")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
