// Initialize WebSocket connection using Socket.IO
const socket = io.connect(window.location.origin);

socket.on('connect', () => {
    console.log("✅ Connected to WebSocket");
});

socket.on('case_solved', (data) => {
    console.log("🔄 WebSocket event received: Case Solved", data);
    fetchSolvedCases();
});

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

// Ensure WebSocket updates solved cases
socket.on('case_solved', () => {
    console.log("📡 Live update: Fetching solved cases...");
    fetchSolvedCases();
});
