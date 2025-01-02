Optimus: Rule of Law Interactive System
--

Optimus is a computational model designed to simulate the institutional logic of the State and the Rule of Law. This project builds on the principles of systems theory, legal philosophy, and agent-based modeling (ABM) to demonstrate how political and judicial systems interact while maintaining coherence through structured decision-making.

This Repository Includes:

- A Flask backend to manage state progression and interactions between the political and judicial systems.
- A dynamic day progression system, ensuring both systems complete their tasks before advancing to the next day.
- Fully integrated HTML frontends for the political and judicial systems.

Project Highlights
--
Key Features

- Day Progression Logic: Days only advance when both systems have completed their actions, mirroring decision-based games like Werewolf (Loup-Garou).

- Political System:
  	- Create norms (laws).
	- Send norms to the judicial system for review.

- Judicial System:
	- Mark norms as unconstitutional.
	- Provide feedback to the political system.

- Dynamic Notifications and Logs: Real-time updates on actions taken by each system.

The Four Rules of the Optimus Method
--
This project adheres to Mohamed Ben Achour’s Optimus Framework:

1. Functional Differentiation: Political and judicial systems operate autonomously with their own logic.
Autopoiesis: Each system self-regulates based on binary distinctions (valid/invalid, constitutional/unconstitutional).
3. Structural Coupling: Systems interact through stable, interdependent feedback loops.
4. Societal Orchestration: A central orchestrator (Flask backend) manages iterations and ensures proper synchronization.

Architecture
--

- Backend: Flask
- Frontend: HTML/CSS (basic UI for Political and Judicial systems)
- Simulation: Agent-based model with Python classes for norms, cases, and systems.
- State Management: Simple in-memory tracking for day progression and completed actions.

How to Run
--
1. Clone the Repository

2. Set Up the Environment
Install Python dependencies:
requirements. txt

3. Run the Flask App
app.py

4. Access the Interfaces

Political System: http://127.0.0.1:5000/political
Judicial System: http://127.0.0.1:5000/judicial
General Log: http://127.0.0.1:5000/general_log

How It Works
--

Day Progression
1. The political system creates a norm.
2. The judicial system evaluates the norm:
Marks it as constitutional/unconstitutional.
Sends feedback to the political system.
3. Once both systems have completed their actions, the day progresses.

Endpoints Backend API
--

/api/create_norm - Creates a new norm (Political System).
/api/check_constitutionality - Marks a norm as constitutional/unconstitutional (Judicial System).
/api/simulate_day - Advances the day when both systems have completed actions.
/api/get_norms - Retrieves all norms created so far.
/api/get_cases - Retrieves all cases reviewed by the judicial system.

Frontend Pages
--
Political System: Allows users to create norms and review feedback.
Judicial System: Allows users to evaluate norms and send notifications.

Future Improvements
--
Expand the society orchestration to simulate more complex systems and feedback loops.
Add user authentication for role-based access (e.g., Political or Judicial actors).
Implement persistent state storage (e.g., database) for norms and cases.
Introduce more dynamic frontends with ReactJS or similar frameworks.

Contributing
--
To contribute to this project:
- Fork the repository instead of cloning it directly.
- Make your changes in the forked version.
- Submit a Pull Request to propose your changes to the original repository.

Credits
--
	- Author: Mohamed Ben Achour
	- Email: mbenachour24@gmail.com	
 	- Blog: Imwerdensein.wordpress.com

Following this workflow ensures that all contributions are tracked and respects the collaborative nature of open-source work. Thank you for helping to maintain a transparent and community-driven project!

Explore, expand, and contribute to Coding the State with Optimus. 🚀

License
--
This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).
Non-commercial use only. For commercial licensing inquiries, contact mbenachour24@gmail.com
