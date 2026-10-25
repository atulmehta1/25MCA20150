// Certificate Schema Definition

const certificateSchemaDefinition = {
  id: { type: String, unique: true, required: true },
  userId: { type: String, ref: 'User', required: true },
  studentName: { type: String, required: true },
  courseId: { type: String, ref: 'Course', required: true },
  courseTitle: { type: String, required: true },
  score: { type: Number, required: true },
  issueDate: { type: String, required: true },
  instructor: { type: String, default: 'Dr. Priya Nair' },
  verificationUrl: { type: String }
};

module.exports = certificateSchemaDefinition;
