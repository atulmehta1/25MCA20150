const express = require('express');
const router = express.Router();
const db = require('../db');

// GET /api/admin/stats
router.get('/stats', (req, res) => {
  const data = db.get();
  const totalUsers = data.users.length;
  const studentsCount = data.users.filter(u => u.role === 'student').length;
  const trainersCount = data.users.filter(u => u.role === 'trainer').length;
  const totalCourses = data.courses.length;
  const totalQuizzes = data.quizzes.length;
  const totalCertificates = data.certificates.length;
  const pendingTrainers = data.users.filter(u => u.role === 'trainer' && !u.isApproved);

  res.json({
    success: true,
    stats: {
      totalUsers,
      studentsCount,
      trainersCount,
      totalCourses,
      totalQuizzes,
      totalCertificates,
      pendingTrainersCount: pendingTrainers.length,
      activeToday: 18,
      courseCompletionRate: '78%',
      avgQuizScore: '82%'
    }
  });
});

// GET /api/admin/users
router.get('/users', (req, res) => {
  const users = db.get().users.map(u => ({
    id: u.id,
    name: u.name,
    email: u.email,
    role: u.role,
    isApproved: u.isApproved !== undefined ? u.isApproved : true,
    xp: u.xp || 0,
    streak: u.streak || 0,
    createdAt: u.createdAt
  }));
  res.json({ success: true, count: users.length, users });
});

// PUT /api/admin/users/:id/approve-trainer
router.put('/users/:id/approve-trainer', (req, res) => {
  const user = db.findUserById(req.params.id);
  if (!user) {
    return res.status(404).json({ success: false, message: 'User not found.' });
  }

  user.isApproved = req.body.isApproved !== undefined ? req.body.isApproved : true;
  db.save();

  res.json({
    success: true,
    message: `Trainer status updated for ${user.name}`,
    user
  });
});

// GET /api/admin/certificates
router.get('/certificates', (req, res) => {
  const certificates = db.getCertificates();
  res.json({ success: true, certificates });
});

// GET /api/admin/certificates/:id
router.get('/certificates/:id', (req, res) => {
  const cert = db.getCertificates().find(c => c.id === req.params.id);
  if (!cert) {
    return res.status(404).json({ success: false, message: 'Certificate not found or invalid ID.' });
  }
  res.json({ success: true, certificate: cert, verified: true });
});

module.exports = router;
