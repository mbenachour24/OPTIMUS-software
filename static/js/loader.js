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

// Créer l'instance uniquement quand le DOM est prêt
document.addEventListener('DOMContentLoaded', () => {
    window.loaderManager = new LoaderManager();
}); 