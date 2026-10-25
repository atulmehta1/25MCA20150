const express = require('express');
const router = express.Router();
const db = require('../db');

// GET /api/courses (with optional category & search filter)
router.get('/', (req, res) => {
  const { category, search } = req.query;
  let courses = db.getCourses();

  if (category && category !== 'All') {
    courses = courses.filter(c => c.category.toLowerCase() === category.toLowerCase());
  }

  if (search) {
    const q = search.toLowerCase();
    courses = courses.filter(c =>
      c.title.toLowerCase().includes(q) ||
      c.description.toLowerCase().includes(q) ||
      c.trainerName.toLowerCase().includes(q)
    );
  }

  res.json({ success: true, count: courses.length, courses });
});

// GET /api/courses/categories
router.get('/categories', (req, res) => {
  const data = db.get();
  res.json({ success: true, categories: data.categories || [] });
});

// GET /api/courses/:id
router.get('/:id', (req, res) => {
  const course = db.getCourseById(req.params.id);
  if (!course) {
    return res.status(404).json({ success: false, message: 'Course not found.' });
  }
  res.json({ success: true, course });
});

// POST /api/courses/enroll/:id
router.post('/enroll/:id', (req, res) => {
  const { userId } = req.body;
  const courseId = req.params.id;

  if (!userId) {
    return res.status(400).json({ success: false, message: 'User ID is required to enroll.' });
  }

  const user = db.findUserById(userId);
  const course = db.getCourseById(courseId);

  if (!user || !course) {
    return res.status(404).json({ success: false, message: 'User or course not found.' });
  }

  user.enrolledCourses = user.enrolledCourses || [];
  if (!user.enrolledCourses.includes(courseId)) {
    user.enrolledCourses.push(courseId);
    course.enrollments = (course.enrollments || 0) + 1;
    db.save();
  }

  res.json({
    success: true,
    message: `Enrolled successfully in ${course.title}!`,
    enrolledCourses: user.enrolledCourses
  });
});

// POST /api/courses/complete-lesson
router.post('/complete-lesson', (req, res) => {
  const { userId, lessonId, courseId } = req.body;
  if (!userId || !lessonId) {
    return res.status(400).json({ success: false, message: 'User ID and Lesson ID required.' });
  }

  const user = db.findUserById(userId);
  if (!user) {
    return res.status(404).json({ success: false, message: 'User not found.' });
  }

  user.completedLessons = user.completedLessons || [];
  let xpAwarded = 0;

  if (!user.completedLessons.includes(lessonId)) {
    user.completedLessons.push(lessonId);
    xpAwarded = 10; // +10 XP for completing a lesson
    user.xp = (user.xp || 0) + xpAwarded;

    // Check if user completed all lessons in course for +100 XP
    if (courseId) {
      const course = db.getCourseById(courseId);
      if (course && course.lessons) {
        const allCompleted = course.lessons.every(l => user.completedLessons.includes(l.id));
        if (allCompleted) {
          user.xp += 100;
          xpAwarded += 100;
        }
      }
    }

    db.save();
  }

  res.json({
    success: true,
    message: xpAwarded > 0 ? `Lesson completed! Earned +${xpAwarded} XP` : 'Lesson already completed.',
    xpEarned: xpAwarded,
    totalXp: user.xp,
    completedLessons: user.completedLessons
  });
});

// POST /api/courses (Create course - Trainer role)
router.post('/', (req, res) => {
  const { title, category, description, duration, level, thumbnail, trainerName, trainerId } = req.body;

  if (!title || !category || !description) {
    return res.status(400).json({ success: false, message: 'Title, category, and description are required.' });
  }

  const newCourse = db.createCourse({
    title,
    category,
    description,
    duration: duration || '10 Hours',
    level: level || 'Beginner',
    thumbnail: thumbnail || 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&auto=format&fit=crop&q=60',
    trainerName: trainerName || 'Instructor',
    trainerId: trainerId || 'u2'
  });

  res.status(201).json({
    success: true,
    message: 'Course created successfully by trainer!',
    course: newCourse
  });
});

// POST /api/courses/:id/lesson (Add lesson - Trainer role)
router.post('/:id/lesson', (req, res) => {
  const { title, duration, videoUrl, pdfTitle, summary, codePractice } = req.body;
  const courseId = req.params.id;

  if (!title) {
    return res.status(400).json({ success: false, message: 'Lesson title is required.' });
  }

  const lesson = db.addLessonToCourse(courseId, {
    title,
    duration: duration || '20 mins',
    videoUrl: videoUrl || 'https://www.w3schools.com/html/mov_bbb.mp4',
    pdfTitle: pdfTitle || 'Lesson_Notes.pdf',
    pdfUrl: '#',
    summary: summary || 'Comprehensive lesson summary and technical insights.',
    codePractice: codePractice || {
      title: 'Practice Challenge',
      instructions: 'Write a function to demonstrate the core concept.',
      starterCode: 'function practice() {\n  return "Done";\n}\nconsole.log(practice());',
      solution: 'function practice() { return "Done"; }'
    }
  });

  if (!lesson) {
    return res.status(404).json({ success: false, message: 'Course not found.' });
  }

  res.status(201).json({
    success: true,
    message: 'Lesson added successfully!',
    lesson
  });
});

module.exports = router;
