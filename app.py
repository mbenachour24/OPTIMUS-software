# This file is part of the OPTIMUS project.
# Licensed under CC BY-NC 4.0. Non-commercial use only.
# For more details, see the LICENSE file in the repository.

from flask import Flask, jsonify, request, render_template
from models.minioptimus import Society

app = Flask(__name__)

# Instantiation of the system
society = Society()

# State tracking for day progression
actions_completed = {"political": False, "judicial": False}

# Example activities data for logs
activities = [
    "Created Norm #1: Tax Policy Reform",
    "Marked Norm #2 as unconstitutional"
]

# Route principale
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Optimus backend API!"})

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
    norm_id = request.json.get('norm_id')
    norm = next((n for n in society.parliament.norms if n.id == norm_id), None)
    if not norm:
        return jsonify({"error": "Norm not found"}), 404

    norm.invalidate()  # Explicitly invalidate the norm
    actions_completed["judicial"] = True  # Mark judicial action as completed
    check_day_progress()
    activities.append(f"Marked Norm #{norm.id} as unconstitutional")
    return jsonify({
        "id": norm.id,
        "text": norm.text,
        "valid": norm.valid,
        "complexity": norm.complexity
    })

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
    cases = [
        {"id": case.id, "text": case.text, "constitutional": case.constitutional}
        for case in society.judicial_system.cases
    ]
    return jsonify(cases)

# API Endpoint for today's activities
@app.route('/api/get_activities', methods=['GET'])
def get_activities():
    return jsonify(activities)

# Helper function to check day progress
def check_day_progress():
    if all(actions_completed.values()):
        print(f"Both actions completed. Ready to simulate the next day (Day {society.iteration + 1}).")

if __name__ == '__main__':
    app.run(debug=True)