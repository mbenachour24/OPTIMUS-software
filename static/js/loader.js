class LoaderManager {
    constructor() {
        document.addEventListener('DOMContentLoaded', () => {
            this.init();
        });
    }

    init() {
        if (document.getElementById('global-loader')) return;
        
        const loader = document.createElement('div');
        loader.id = 'global-loader';
        loader.className = 'loader-container hidden';
        loader.innerHTML = `
            <div class="loader">
                <div class="spinner"></div>
                <div class="loader-text">Chargement en cours...</div>
            </div>
        `;
        document.body.appendChild(loader);
    }

    show() {
        const loader = document.getElementById('global-loader');
        if (loader) loader.classList.remove('hidden');
    }

    hide() {
        const loader = document.getElementById('global-loader');
        if (loader) loader.classList.add('hidden');
    }

    async fetchWithLoader(url, options = {}) {
        try {
            this.show();
            const response = await fetch(url, options);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Erreur lors de la requête:', error);
            throw error;
        } finally {
            this.hide();
        }
    }
}

function updateSolvedCaseCount() {
    fetch('/api/get_solved_cases')
        .then(response => response.json())
        .then(data => {
            const solvedCountElement = document.getElementById('solved-case-count');
            if (solvedCountElement) {
                solvedCountElement.innerText = data.total;
                console.log("Updated solved case count:", data.total);
            } else {
                console.warn("Solved case count element not found.");
            }
        })
        .catch(error => console.error('Error updating solved case count:', error));
}

// Refresh solved case count every 30 seconds
setInterval(updateSolvedCaseCount, 30000);

// Ensure WebSocket updates the solved case count
if (typeof socket !== 'undefined') {
    socket.on('case_solved', updateSolvedCaseCount);
} else {
    console.warn("WebSocket 'socket' is not defined. Ensure it is initialized properly.");
}

// Initialize LoaderManager when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.loaderManager = new LoaderManager();
    updateSolvedCaseCount(); // Initial update when page loads
});
