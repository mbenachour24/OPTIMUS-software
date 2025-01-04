// Initialize WebSocket connection
const ws = new WebSocket(`ws://${window.location.host}/ws`);

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'norm_update') {
        // Update the norm's validity in the UI without refresh
        updateNormStatus(data.norm_id, data.valid);
    }
};

function updateNormStatus(normId, isValid) {
    const normElement = document.querySelector(`[data-norm-id="${normId}"]`);
    if (normElement) {
        normElement.querySelector('.validity-status').textContent = isValid ? 'Valid' : 'Invalid';
        normElement.classList.toggle('invalid', !isValid);
    }
} 