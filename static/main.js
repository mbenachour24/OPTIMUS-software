// Initialize WebSocket connection (Replace Socket.IO)
let socket;

function connectWebSocket() {
    socket = new WebSocket("ws://localhost:8000/ws");

    socket.onopen = () => {
        console.log("✅ Connected to WebSocket");
    };

    socket.onmessage = (event) => {
        try {
            let data = JSON.parse(event.data);
            
            if (data.event === "case_solved") {
                console.log("📡 Live update: Case Solved received via WebSocket");
                fetchSolvedCases();  // ✅ Refresh solved cases
            }
        } catch (error) {
            console.error("❌ WebSocket message error:", error);
        }
    };

    socket.onclose = (event) => {
        console.warn("🔴 WebSocket disconnected, attempting to reconnect in 5s...");
        setTimeout(connectWebSocket, 5000);
    };

    socket.onerror = (error) => {
        console.error("❌ WebSocket encountered an error:", error);
    };
}

// ✅ Start WebSocket Connection
connectWebSocket();

// Function to update the UI when a norm's validity changes
function updateNormStatus(normId, isValid) {
    const normElement = document.querySelector(`[data-norm-id="${normId}"]`);
    if (normElement) {
        normElement.querySelector('.validity-status').textContent = isValid ? 'Valid' : 'Invalid';
        normElement.classList.toggle('invalid', !isValid);
    }
}

// Function to manually fetch solved cases (fallback for page refresh)
function fetchSolvedCases() {
    fetch('/api/get_solved_cases')
        .then(response => response.json())
        .then(data => {
            console.log("📊 Updated solved cases:", data);

            const solvedCasesList = document.getElementById('solved-cases-list');
            if (solvedCasesList) {
                solvedCasesList.innerHTML = data.solved_cases.map(caseItem => `
                    <div class="case-item solved">
                        <p><strong>Case #${caseItem.id}:</strong> ${caseItem.text}</p>
                        <small>Resolved at: ${caseItem.resolved_at || "Unknown Time"}</small>
                    </div>
                `).join('');
            }

            // Also update the solved case count in statistics
            const solvedCaseCount = document.getElementById('solved-case-count');
            if (solvedCaseCount) {
                solvedCaseCount.innerText = data.total || 0;
            }
        })
        .catch(error => console.error('❌ Error fetching solved cases:', error));
}

// Call fetch on page load
document.addEventListener('DOMContentLoaded', () => {
    fetchSolvedCases();
});

// Sidebar toggle functionality
document.querySelector('.sidebar-toggle').addEventListener('click', () => {
    document.querySelector('.sidebar').classList.toggle('collapsed');
});
