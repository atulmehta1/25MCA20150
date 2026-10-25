const express = require('express');
const router = express.Router();
const db = require('../db');

// GET /api/quizzes/course/:courseId
router.get('/course/:courseId', (req, res) => {
  const quiz = db.getQuizByCourseId(req.params.courseId);
  if (!quiz) {
    return res.status(404).json({ success: false, message: 'No quiz found for this course yet.' });
  }
  res.json({ success: true, quiz });
});

// GET /api/quizzes/:id
router.get('/:id', (req, res) => {
  const quiz = db.getQuizById(req.params.id);
  if (!quiz) {
    return res.status(404).json({ success: false, message: 'Quiz not found.' });
  }
  res.json({ success: true, quiz });
});

// POST /api/quizzes/submit
router.post('/submit', (req, res) => {
  const { quizId, userId, answers } = req.body;
  // answers: { questionId: selectedIndex }

  if (!quizId || !answers) {
    return res.status(400).json({ success: false, message: 'Quiz ID and answers required.' });
  }

  const quiz = db.getQuizById(quizId);
  if (!quiz) {
    return res.status(404).json({ success: false, message: 'Quiz not found.' });
  }

  let correctCount = 0;
  const review = [];

  quiz.questions.forEach((q) => {
    const selected = answers[q.id];
    const isCorrect = selected === q.correctIndex;
    if (isCorrect) correctCount++;

    review.push({
      questionId: q.id,
      question: q.question,
      options: q.options,
      selectedIndex: selected !== undefined ? selected : null,
      correctIndex: q.correctIndex,
      isCorrect,
      explanation: q.explanation
    });
  });

  const totalQuestions = quiz.questions.length;
  const scorePercent = Math.round((correctCount / totalQuestions) * 100);
  const passed = scorePercent >= (quiz.passingScore || 70);

  let xpAwarded = 0;
  let certificate = null;

  if (userId) {
    const user = db.findUserById(userId);
    if (user) {
      if (passed) {
        xpAwarded = 20; // +20 XP for passing quiz
        user.xp = (user.xp || 0) + xpAwarded;

        // Auto-generate certificate if passed and not already issued
        const course = db.getCourseById(quiz.courseId);
        const existingCert = db.getCertificates().find(c => c.userId === userId && c.courseId === quiz.courseId);
        
        if (!existingCert && course) {
          certificate = db.createCertificate({
            userId: user.id,
            studentName: user.name,
            courseId: course.id,
            courseTitle: course.title,
            score: scorePercent,
            instructor: course.trainerName || 'Dr. Priya Nair'
          });
        } else if (existingCert) {
          certificate = existingCert;
        }

        db.save();
      }
    }
  }

  res.json({
    success: true,
    score: scorePercent,
    correctCount,
    totalQuestions,
    passed,
    xpAwarded,
    certificate,
    review
  });
});

// POST /api/quizzes (Trainer creates new quiz)
router.post('/', (req, res) => {
  const { courseId, title, durationMinutes, passingScore, questions } = req.body;

  if (!courseId || !title || !questions || !questions.length) {
    return res.status(400).json({ success: false, message: 'Course ID, title, and questions array required.' });
  }

  const newQuiz = db.createQuiz({
    courseId,
    title,
    durationMinutes: durationMinutes || 10,
    passingScore: passingScore || 70,
    questions
  });

  res.status(201).json({
    success: true,
    message: 'Quiz created successfully!',
    quiz: newQuiz
  });
});

module.exports = router;
