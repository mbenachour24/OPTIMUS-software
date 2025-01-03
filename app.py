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
    try:
        data = request.get_json()
        if not data or 'norm_id' not in data:
            return jsonify({"error": "Missing norm_id in request"}), 400
            
        norm_id = data['norm_id']
        norm = next((n for n in society.parliament.norms if n.id == norm_id), None)
        if not norm:
            return jsonify({"error": "Norm not found"}), 404

        # Invalidate the norm
        norm.invalidate()

        # Create a notification
        notification = f"Norm #{norm.id} ({norm.text}) marked as unconstitutional."
        notification_manager.add_notification(notification, type="judicial")

        return jsonify({
            "id": norm.id,
            "text": norm.text,
            "valid": norm.valid,
            "complexity": norm.complexity,
            "message": f"Political System notified: {notification}"
        })
    except Exception as e:
        logging.error(f"Error in mark_unconstitutional: {e}")
        return jsonify({"error": "Internal server error"}), 500

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
        generated_cases = society.citizen_pressure.generate_daily_cases()
        
        case_details = [{
            "id": case.id,
            "text": case.text,
            "norm_id": case.norm.id,
            "constitutional": case.constitutional
        } for case in generated_cases]
        
        return jsonify({
            "message": f"Generated {len(generated_cases)} citizen pressure cases",
            "cases": case_details
        })
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get the port from Heroku's environment variables
    debug_mode = os.environ.get("DEBUG", "False").lower() == "true"  # Enable debug mode only if DEBUG=true
    app.run(host="0.0.0.0", port=port, debug=debug_mode)