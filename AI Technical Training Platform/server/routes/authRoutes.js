const express = require('express');
const router = express.Router();
const db = require('../db');

// POST /api/auth/login
router.post('/login', (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ success: false, message: 'Please provide email and password.' });
  }

  const user = db.findUserByEmail(email);
  if (!user || user.password !== password) {
    return res.status(401).json({ success: false, message: 'Invalid email or password.' });
  }

  // Generate lightweight mock JWT token
  const token = 'jwt-token-' + Buffer.from(`${user.id}:${user.email}:${user.role}`).toString('base64');

  res.json({
    success: true,
    message: `Welcome back, ${user.name}!`,
    token,
    user: {
      id: user.id,
      name: user.name,
      email: user.email,
      role: user.role,
      avatar: user.avatar,
      xp: user.xp,
      streak: user.streak,
      badges: user.badges,
      enrolledCourses: user.enrolledCourses || []
    }
  });
});

// POST /api/auth/register
router.post('/register', (req, res) => {
  const { name, email, password, role = 'student' } = req.body;

  if (!name || !email || !password) {
    return res.status(400).json({ success: false, message: 'All fields are required.' });
  }

  const existing = db.findUserByEmail(email);
  if (existing) {
    return res.status(400).json({ success: false, message: 'User with this email already exists.' });
  }

  const avatar = `https://api.dicebear.com/7.x/bottts/svg?seed=${encodeURIComponent(name)}`;
  const newUser = db.createUser({
    name,
    email,
    password,
    role,
    avatar,
    isApproved: role === 'student' ? true : false // Trainers await admin approval
  });

  const token = 'jwt-token-' + Buffer.from(`${newUser.id}:${newUser.email}:${newUser.role}`).toString('base64');

  res.status(201).json({
    success: true,
    message: 'Registration successful!',
    token,
    user: newUser
  });
});

// GET /api/auth/profile/:id
router.get('/profile/:id', (req, res) => {
  const user = db.findUserById(req.params.id);
  if (!user) {
    return res.status(404).json({ success: false, message: 'User not found.' });
  }
  res.json({ success: true, user });
});

// PUT /api/auth/profile/:id
router.put('/profile/:id', (req, res) => {
  const updated = db.updateUser(req.params.id, req.body);
  if (!updated) {
    return res.status(404).json({ success: false, message: 'User not found.' });
  }
  res.json({ success: true, message: 'Profile updated successfully.', user: updated });
});

module.exports = router;
