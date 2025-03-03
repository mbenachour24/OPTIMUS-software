# Optimus: Rule of Law Interactive System

## Overview

Optimus is a computational model designed to simulate and analyze the interaction between political and judicial systems. It translates theoretical concepts of the Rule of Law into a dynamic, iterative software framework, leveraging system theory and agent-based modeling. The project is built upon an "algorithm of the Rule of Law" based on Niklas Luhmann's systems theory into legal informatics.

## Features

- **Norm Creation & Evaluation**: The political system generates legal norms, which are then assessed by the judicial system for validity and constitutionality.
- **Case Management**: The judicial system processes legal cases, referencing norms and making constitutional decisions.
- **Normative Inflation Analysis**: Tracks the creation of norms and the backlog of unresolved cases, using quantitative legal analysis.
- **Citizen Pressure Modeling**: Simulates public influence on legal cases, introducing real-world complexity into the judicial process.
- **Web Interface**: Provides interactive dashboards for monitoring judicial and political activities.
- **WebSocket Support**: Enables real-time updates and notifications.

## The Four Rules of the Optimus Method

This project adheres to Mohamed Ben Achour’s Optimus Framework:

- **Functional Differentiation**: Political and judicial systems operate autonomously with their own logic. 
- **Autopoiesis**: Each system self-regulates based on binary distinctions (valid/invalid, constitutional/unconstitutional).
- **Structural Coupling**: Systems interact through stable, interdependent feedback loops.
- **Societal Orchestration**: A central orchestrator (Flask backend) manages iterations and ensures proper synchronization.

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL (or SQLite for local testing)
- FastAPI
- SQLAlchemy (async support)
- Jinja2 for templating

### Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/mbenachour24/OPTIMUS-software.git
   cd optimus
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   - Copy `.env.example` to `.env` and update database settings.
4. Initialize the database:
   ```sh
   python database.py
   ```
5. Start the server:
   ```sh
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

## Project Structure

```
.
├── app.py (Main FastAPI application)
├── database.py (Database connection and initialization)
├── models
│   ├── norm.py (Norm model)
│   ├── case.py (Case model)
│   ├── political_system.py (Political system logic)
│   ├── judicial_system.py (Judicial system logic)
│   ├── citizen_pressure.py (Citizen influence modeling)
│   └── society.py (Central coordinator)
├── templates
│   ├── index.html (Main UI)
│   ├── judicial_interface.html (Judicial system interface)
│   ├── political_interface.html (Political system interface)
│   ├── view_norms.html (Norms management UI)
│   ├── cases_view.html (Cases management UI)
│   ├── statistics_dashboard.html (Analytics UI)
│   ├── general_log.html (System logs UI)
│   └── judicial_interface.html (Judicial management UI)
└── static (Frontend assets)
```



The UI provides users with an interactive dashboard where they can:

- **Manage Norms**: Users can view, create, and assess the validity of norms within the system.
- **Track Cases**: The judicial system interface allows users to see pending and resolved cases, as well as make constitutional assessments.
- **View Real-Time Data**: The statistics dashboard provides insights into normative inflation, case resolution rates, and overall system health. Normative inflation refers to the increasing volume of legal norms relative to the system’s capacity to process and enforce them. The dashboard tracks this phenomenon by analyzing the rate of norm creation versus judicial resolution, identifying backlogs, and assessing systemic efficiency. Users can monitor trends over time, evaluate the impact of new legal norms, and predict potential legal bottlenecks.
- **Receive Notifications**: Users get real-time updates on norm modifications, judicial decisions, and system events via WebSockets.
- **Interact with Systems**: The political and judicial interfaces allow respective actions, such as creating norms, generating and solving cases.

## API Endpoints

### Norm Management

- **Create a norm**: `POST /api/create_norm`
- **Fetch all norms**: `GET /api/get_norms`
- **Validate a norm's constitutionality**: `POST /api/check_constitutionality`
- **Mark norm as unconstitutional**: `POST /api/mark_unconstitutional`

### Case Management

- **Fetch all cases**: `GET /api/get_all_cases`
- **Generate citizen cases**: `POST /api/generate_citizen_cases`
- **Solve a case**: `POST /api/solve_case/{case_id}`

### Analytics

- **Get system statistics**: `GET /api/get_statistics`
- **Retrieve normative inflation metrics**: `GET /api/get_normative_inflation`

## License

This project is licensed under **CC BY-NC 4.0** (Non-Commercial Use Only). See `LICENSE` for details.

## Contact

For inquiries, reach out to the project author at [mbenachour24@gmail.com](mailto\:mbenachour24@gmail.com)
