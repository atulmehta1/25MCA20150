const express = require('express');
const cors = require('cors');
const path = require('path');

const authRoutes = require('./routes/authRoutes');
const courseRoutes = require('./routes/courseRoutes');
const quizRoutes = require('./routes/quizRoutes');
const aiRoutes = require('./routes/aiRoutes');
const forumRoutes = require('./routes/forumRoutes');
const adminRoutes = require('./routes/adminRoutes');
const db = require('./db');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve frontend static assets from client folder
app.use(express.static(path.join(__dirname, '../client')));

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/courses', courseRoutes);
app.use('/api/quizzes', quizRoutes);
app.use('/api/ai', aiRoutes);
app.use('/api/forum', forumRoutes);
app.use('/api/admin', adminRoutes);

// General Gamification & Platform Endpoints
app.get('/api/leaderboard', (req, res) => {
  res.json({ success: true, leaderboard: db.getLeaderboard() });
});

app.get('/api/coding-challenges', (req, res) => {
  res.json({ success: true, challenges: db.getCodingChallenges() });
});

app.get('/api/notifications', (req, res) => {
  res.json({ success: true, notifications: db.getNotifications() });
});

// Fallback route: serve index.html for direct navigation
app.use((req, res) => {
  res.sendFile(path.join(__dirname, '../client/index.html'));
});

// Start Server
app.listen(PORT, () => {
  console.log('========================================================');
  console.log(`[SERVER] AI Technical Training Platform (MCA Project Server)`);
  console.log(`[URL] Running at: http://localhost:${PORT}`);
  console.log('--------------------------------------------------------');
  console.log('Demo Credentials for Testing & Viva:');
  console.log('   Student: student@demo.com  / password123 (Atul Mehta)');
  console.log('   Trainer: trainer@demo.com  / password123');
  console.log('   Admin:   admin@demo.com    / password123');
  console.log('5 AI Features Active: Tutor, Explainer, QuizGen, Mock Interview, Resume Review');
  console.log('========================================================');
});
