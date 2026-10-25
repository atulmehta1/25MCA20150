const fs = require('fs');
const path = require('path');

const dataFilePath = path.join(__dirname, 'data', 'initialData.json');

// In-memory working copy
let dbData = null;

function loadDatabase() {
  if (dbData) return dbData;
  try {
    const raw = fs.readFileSync(dataFilePath, 'utf8');
    dbData = JSON.parse(raw);
  } catch (err) {
    console.error('Error loading initialData.json:', err);
    dbData = {
      users: [],
      courses: [],
      quizzes: [],
      categories: [],
      forum: [],
      notifications: [],
      codingChallenges: [],
      leaderboard: [],
      certificates: []
    };
  }
  return dbData;
}

function saveDatabase() {
  try {
    fs.writeFileSync(dataFilePath, JSON.stringify(dbData, null, 2), 'utf8');
  } catch (err) {
    console.error('Error saving data to initialData.json:', err);
  }
}

// Database helper functions resembling Mongoose/ActiveRecord
const db = {
  get: () => loadDatabase(),
  save: () => saveDatabase(),

  // Users
  findUserByEmail: (email) => {
    const data = loadDatabase();
    return data.users.find(u => u.email.toLowerCase() === email.toLowerCase());
  },
  findUserById: (id) => {
    const data = loadDatabase();
    return data.users.find(u => u.id === id);
  },
  createUser: (userData) => {
    const data = loadDatabase();
    const newUser = {
      id: 'u' + Date.now(),
      xp: 0,
      streak: 1,
      enrolledCourses: [],
      completedLessons: [],
      badges: ['Beginner'],
      createdAt: new Date().toISOString(),
      ...userData
    };
    data.users.push(newUser);
    saveDatabase();
    return newUser;
  },
  updateUser: (id, updates) => {
    const data = loadDatabase();
    const idx = data.users.findIndex(u => u.id === id);
    if (idx !== -1) {
      data.users[idx] = { ...data.users[idx], ...updates };
      saveDatabase();
      return data.users[idx];
    }
    return null;
  },

  // Courses
  getCourses: () => loadDatabase().courses,
  getCourseById: (id) => loadDatabase().courses.find(c => c.id === id),
  createCourse: (courseData) => {
    const data = loadDatabase();
    const newCourse = {
      id: 'c' + Date.now(),
      rating: 5.0,
      enrollments: 0,
      lessonsCount: 0,
      lessons: [],
      ...courseData
    };
    data.courses.push(newCourse);
    saveDatabase();
    return newCourse;
  },
  addLessonToCourse: (courseId, lessonData) => {
    const data = loadDatabase();
    const course = data.courses.find(c => c.id === courseId);
    if (course) {
      const newLesson = {
        id: 'l-' + Date.now(),
        ...lessonData
      };
      course.lessons = course.lessons || [];
      course.lessons.push(newLesson);
      course.lessonsCount = course.lessons.length;
      saveDatabase();
      return newLesson;
    }
    return null;
  },

  // Quizzes
  getQuizzes: () => loadDatabase().quizzes,
  getQuizById: (id) => loadDatabase().quizzes.find(q => q.id === id),
  getQuizByCourseId: (courseId) => loadDatabase().quizzes.find(q => q.courseId === courseId),
  createQuiz: (quizData) => {
    const data = loadDatabase();
    const newQuiz = {
      id: 'q' + Date.now(),
      ...quizData
    };
    data.quizzes.push(newQuiz);
    saveDatabase();
    return newQuiz;
  },

  // Forum
  getForumPosts: () => loadDatabase().forum,
  createForumPost: (postData) => {
    const data = loadDatabase();
    const newPost = {
      id: 'f' + Date.now(),
      date: 'Just now',
      upvotes: 0,
      replies: [],
      ...postData
    };
    data.forum.unshift(newPost);
    saveDatabase();
    return newPost;
  },
  addReplyToPost: (postId, replyData) => {
    const data = loadDatabase();
    const post = data.forum.find(f => f.id === postId);
    if (post) {
      const newReply = {
        id: 'r' + Date.now(),
        upvotes: 0,
        ...replyData
      };
      post.replies = post.replies || [];
      post.replies.push(newReply);
      saveDatabase();
      return newReply;
    }
    return null;
  },

  // Certificates
  getCertificates: () => loadDatabase().certificates,
  createCertificate: (certData) => {
    const data = loadDatabase();
    const newCert = {
      id: 'CERT-' + new Date().getFullYear() + '-' + Math.floor(1000 + Math.random() * 9000),
      issueDate: new Date().toISOString().split('T')[0],
      verificationUrl: '#verify',
      ...certData
    };
    data.certificates.push(newCert);
    saveDatabase();
    return newCert;
  },

  // Leaderboard & Challenges
  getLeaderboard: () => loadDatabase().leaderboard,
  getCodingChallenges: () => loadDatabase().codingChallenges,
  getNotifications: () => loadDatabase().notifications
};

module.exports = db;
