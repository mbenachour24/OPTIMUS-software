# This file is part of the OPTMUS project.
# Licensed under CC BY-NC 4.0. Non-commercial use only.
# For more details, see the LICENSE file in the repository.

from flask import Flask, jsonify, request, render_template
from models.minioptimus import Society

app = Flask(__name__)

# Instantiation of the system
society = Society()

# State tracking for day progression
actions_completed = {"political": False, "judicial": False}

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

# API Endpoint pour créer un nouveau Norm
@app.route('/api/create_norm', methods=['POST'])
def create_norm():
    norm = society.parliament.create_norm()
    actions_completed["political"] = True  # Mark political action as completed
    check_day_progress()
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

    return jsonify({
        "id": norm.id,
        "text": norm.text,
        "valid": norm.valid,
        "complexity": norm.complexity
    })

# API Endpoint pour notifier le système politique
@app.route('/api/notify_political', methods=['POST'])
def notify_political():
    norm_id = request.json.get('norm_id')
    status = request.json.get('status')
    norm = next((n for n in society.parliament.norms if n.id == norm_id), None)
    if not norm:
        return jsonify({"error": "Norm not found"}), 404
    # Log the notification
    print(f"Notification sent to Political System: Norm #{norm_id} marked as {status}.")
    return jsonify({"message": f"Political System notified about Norm #{norm_id} status: {status}."})

# API Endpoint pour créer un nouveau Case
@app.route('/api/create_case', methods=['POST'])
def create_case():
    norm_id = request.json.get('norm_id')
    norm = next((n for n in society.parliament.norms if n.id == norm_id), None)
    if not norm:
        return jsonify({"error": "Norm not found"}), 404
    case = society.judicial_system.create_case(norm)
    if not case:
        return jsonify({"error": "Cannot create case for invalid norm"}), 400
    actions_completed["judicial"] = True  # Mark judicial action as completed if a case was created
    check_day_progress()
    return jsonify({
        "id": case.id,
        "text": case.text,
        "constitutional": case.constitutional
    })

# API Endpoint pour simuler un jour
@app.route('/api/simulate_day', methods=['POST'])
def simulate_day():
    try:
        # Ensure both actions are completed before advancing the day
        if not all(actions_completed.values()):
            return jsonify({"error": "Both actions (political and judicial) must be completed to pass the day"}), 400

        # Reset actions for the new day
        actions_completed["political"] = False
        actions_completed["judicial"] = False
        society.iteration += 1  # Advance the day
        return jsonify({"message": f"Day {society.iteration} simulated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API Endpoint pour récupérer tous les norms
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

# Helper function to check day progress
def check_day_progress():
    if all(actions_completed.values()):
        print(f"Both actions completed. Ready to simulate the next day (Day {society.iteration + 1}).")

if __name__ == '__main__':
    app.run(debug=True)
