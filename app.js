// This file is part of the OPTIMUS project.
// Licensed under CC BY-NC 4.0. Non-commercial use only.
// For more details, see the LICENSE file in the repository.

const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const { Society } = require('./models/minioptimus'); // Replace with actual module
const socketIO = require('socket.io');

const app = express();
const port = process.env.PORT || 5000;

// Middleware
app.use(bodyParser.json());
app.use(cors());
app.use(express.static(path.join(__dirname, 'static')));

// Ensure the data directory exists
if (!fs.existsSync('data')) {
    fs.mkdirSync('data');
}

// Set up notification manager
class NotificationManager {
    constructor() {
        this.notifications = [];
        this.loadNotifications();
    }

    addNotification(message, type = 'info') {
        const notification = {
            message,
            timestamp: new Date().toISOString(),
            type
        };
        this.notifications.push(notification);
        this.saveNotifications();
    }

    getNotifications() {
        return this.notifications;
    }

    saveNotifications() {
        try {
            const notificationsFile = path.join('data', 'notifications.json');
            fs.writeFileSync(notificationsFile, JSON.stringify(this.notifications.slice(-100)), 'utf8');
        } catch (e) {
            console.error(`Failed to save notifications: ${e}`);
        }
    }

    loadNotifications() {
        try {
            const notificationsFile = path.join('data', 'notifications.json');
            if (fs.existsSync(notificationsFile)) {
                this.notifications = JSON.parse(fs.readFileSync(notificationsFile, 'utf8'));
            }
        } catch (e) {
            console.error(`Failed to load notifications: ${e}`);
            this.notifications = [];
        }
    }
}

// Instantiate systems
const society = new Society();
const notificationManager = new NotificationManager();
let actionsCompleted = { political: false, judicial: false };
const activities = [];

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'index.html'));
});

app.get('/judicial', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'judicial_interface.html'));
});

app.get('/political', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'political_interface.html'));
});

app.post('/api/create_norm', (req, res) => {
    const norm = society.parliament.createNorm();
    actionsCompleted.political = true;
    checkDayProgress();
    activities.push(`Created Norm #${norm.id}: ${norm.text}`);
    res.json({
        id: norm.id,
        text: norm.text,
        valid: norm.valid,
        complexity: norm.complexity
    });
});

app.post('/api/check_constitutionality', (req, res) => {
    const { norm_id } = req.body;
    const norm = society.parliament.norms.find(n => n.id === norm_id);
    if (!norm) return res.status(404).json({ error: 'Norm not found' });

    society.judicialSystem.checkConstitutionality(norm);
    actionsCompleted.judicial = true;
    checkDayProgress();
    activities.push(`Checked constitutionality for Norm #${norm.id}: ${norm.valid ? 'Valid' : 'Invalid'}`);
    res.json({
        id: norm.id,
        valid: norm.valid,
        complexity: norm.complexity
    });
});

app.get('/api/get_notifications', (req, res) => {
    const { type } = req.query;
    const notifications = type
        ? notificationManager.getNotifications().filter(n => n.type === type)
        : notificationManager.getNotifications();
    res.json(notifications);
});

// Check day progress
function checkDayProgress() {
    if (Object.values(actionsCompleted).every(action => action)) {
        console.log(`Both actions completed. Ready for next day (Day ${society.iteration + 1}).`);
    }
}

// Clear notifications on startup
const notificationsFile = path.join('data', 'notifications.json');
if (fs.existsSync(notificationsFile)) fs.unlinkSync(notificationsFile);

// Start server with Socket.IO
const server = app.listen(port, () => console.log(`Server running on port ${port}`));
const io = socketIO(server);

io.on('connection', (socket) => {
    console.log('Socket connected');
});
