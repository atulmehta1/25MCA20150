// MongoDB / Mongoose Schema Definition for MCA Project Documentation
// Can be used with active MongoDB or referenced in project viva

const userSchemaDefinition = {
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  role: { type: String, enum: ['student', 'trainer', 'admin'], default: 'student' },
  avatar: { type: String, default: '' },
  xp: { type: Number, default: 0 },
  streak: { type: Number, default: 1 },
  badges: [{ type: String }],
  enrolledCourses: [{ type: String, ref: 'Course' }],
  completedLessons: [{ type: String }],
  isApproved: { type: Boolean, default: true },
  createdAt: { type: Date, default: Date.now }
};

module.exports = userSchemaDefinition;
