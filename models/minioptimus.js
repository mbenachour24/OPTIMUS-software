// This file is part of the OPTIMUS project.
// Licensed under CC BY-NC 4.0. Non-commercial use only.
// For more details, see the LICENSE file in the repository.

const fs = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

const COMPLEXITY_MIN = 1;
const COMPLEXITY_MAX = 10;
const SIMULATION_DAYS = 100;

// Setup logging
const log = (message) => {
    console.log(message);
};

class NotificationManager {
    constructor() {
        this.notifications = [];
        this.clearNotificationsFile();
    }

    clearNotificationsFile() {
        const notificationsFile = path.join('data', 'notifications.json');
        try {
            fs.mkdirSync('data', { recursive: true });
            if (fs.existsSync(notificationsFile)) fs.unlinkSync(notificationsFile);
            log("Cleared old notifications file");
        } catch (err) {
            log("No old notifications file to clear");
        }
    }

    async broadcastUpdate(data) {
        log(`Broadcasting update: ${JSON.stringify(data)}`);
    }
}

const notificationManager = new NotificationManager();

class Norm {
    constructor(id, text, valid = true, complexity = 1) {
        this.id = id;
        this.text = text;
        this.valid = valid;
        this.complexity = complexity;
        this.logEvent(`Initialized with complexity ${complexity} and validity ${valid}`);
    }

    invalidate() {
        this.valid = false;
        this.logEvent("Invalidated");
        notificationManager.broadcastUpdate({
            type: 'norm_update',
            norm_id: this.id,
            valid: this.valid,
        });
    }

    logEvent(message) {
        log(`Norm ${this.id}: ${message}`);
    }
}

class Case {
    constructor(id, text, norm) {
        this.id = id;
        this.text = text;
        this.norm = norm;
        this.constitutional = norm.valid;
        this.resolvedAt = null;
        this.logEvent("A new case is brought to the Courts");
    }

    logEvent(message) {
        log(`Case ${this.id}: ${message}`);
    }
}

class CitizenPressure {
    constructor(judicialSystem, parliament) {
        this.judicialSystem = judicialSystem;
        this.parliament = parliament;
        this.dailyCaseCount = 5;
        this.caseTypes = [
            "Environmental Concern",
            "Civil Rights Issue",
            "Labor Dispute",
            "Consumer Protection",
            "Luhmann's theory Public Safety Concern",
            "Mohamed got funds and it's not fair",
            "Alien invasion",
            "Zombie outbreak",
        ];
    }

    generateDailyCases() {
        const validNorms = this.parliament.norms.filter((norm) => norm.valid);
        if (!validNorms.length) {
            log("No valid norm to generate case.");
            return "No valid norm to generate case.";
        }

        return Array.from({ length: this.dailyCaseCount }, () => {
            const norm = validNorms[Math.floor(Math.random() * validNorms.length)];
            const caseType = this.caseTypes[Math.floor(Math.random() * this.caseTypes.length)];
            return this.judicialSystem.createCaseFromPressure(
                norm,
                `Citizen Petition: ${caseType} regarding ${norm.text}`
            );
        });
    }
}

class PoliticalSystem {
    constructor() {
        this.normCounter = 0;
        this.norms = [];
    }

    createNorm() {
        this.normCounter += 1;
        const norm = new Norm(
            this.normCounter,
            `Law ${this.normCounter}`,
            true,
            Math.floor(Math.random() * (COMPLEXITY_MAX - COMPLEXITY_MIN + 1)) + COMPLEXITY_MIN
        );
        this.norms.push(norm);
        log(`Debug: Created Norm #${this.normCounter}`);
        return norm;
    }
}

class JudicialSystem {
    constructor() {
        this.caseCounter = 0;
        this.pendingCases = [];
        this.solvedCases = [];
    }

    checkConstitutionality(norm) {
        log(`Checking constitutionality of norm ${norm.id} with complexity ${norm.complexity}`);
        log(`Norm ${norm.id} has been checked. Valid status: ${norm.valid}`);
    }

    createCaseFromPressure(norm, pressureText) {
        if (!norm.valid) {
            log(`Cannot create a case for an invalid norm (Norm #${norm.id})`);
            return null;
        }
        this.caseCounter += 1;
        const caseObj = new Case(this.caseCounter, pressureText, norm);
        this.pendingCases.push(caseObj);
        caseObj.logEvent("Created from citizen pressure");
        return caseObj;
    }
}

class Society {
    constructor() {
        this.parliament = new PoliticalSystem();
        this.judicialSystem = new JudicialSystem();
        this.citizenPressure = new CitizenPressure(this.judicialSystem, this.parliament);
        this.iteration = 0;
    }

    async simulate() {
        while (this.iteration < SIMULATION_DAYS) {
            this.iteration += 1;
            log(`Debug: Starting Day ${this.iteration}`);

            const norm = this.parliament.createNorm();
            log(`Debug: Created Norm: ${norm.text}, Valid: ${norm.valid}`);

            this.judicialSystem.checkConstitutionality(norm);

            const generatedCases = this.citizenPressure.generateDailyCases();
            log(`Debug: Generated ${generatedCases.length || 0} citizen pressure cases`);

            log(`Debug: Ending Day ${this.iteration}`);
            await new Promise((resolve) => setTimeout(resolve, 1000));
        }
    }
}

(async () => {
    const society = new Society();
    await society.simulate();
})();

module.exports = { Society }; // Ensure you're exporting it
