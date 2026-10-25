const express = require('express');
const router = express.Router();
const aiEngine = require('../utils/aiEngine');

// 1. AI Chat Tutor
// POST /api/ai/tutor
router.post('/tutor', (req, res) => {
  const { prompt, topic } = req.body;
  if (!prompt) {
    return res.status(400).json({ success: false, message: 'Please provide a technical question or prompt.' });
  }

  const response = aiEngine.generateTutorResponse(prompt, topic);
  res.json({
    success: true,
    data: response
  });
});

// 2. AI Code Explainer
// POST /api/ai/code-explain
router.post('/code-explain', (req, res) => {
  const { code, language } = req.body;
  if (!code) {
    return res.status(400).json({ success: false, message: 'Please paste code to explain.' });
  }

  const response = aiEngine.explainCode(code, language || 'javascript');
  res.json({
    success: true,
    data: response
  });
});

// 3. AI Quiz Generator
// POST /api/ai/generate-quiz
router.post('/generate-quiz', (req, res) => {
  const { topic, count } = req.body;
  if (!topic) {
    return res.status(400).json({ success: false, message: 'Please provide a topic for quiz generation.' });
  }

  const response = aiEngine.generateQuiz(topic, count || 5);
  res.json({
    success: true,
    data: response
  });
});

// 4. AI Interview Preparation
// POST /api/ai/interview
router.post('/interview', (req, res) => {
  const { role, round } = req.body;
  const response = aiEngine.generateInterviewMock(role || 'Full Stack Developer', round || 'Technical');
  res.json({
    success: true,
    data: response
  });
});

// 5. AI Resume Review
// POST /api/ai/resume-review
router.post('/resume-review', (req, res) => {
  const { resumeText } = req.body;
  if (!resumeText) {
    return res.status(400).json({ success: false, message: 'Please paste or upload your resume text.' });
  }

  const response = aiEngine.reviewResume(resumeText);
  res.json({
    success: true,
    data: response
  });
});

module.exports = router;
