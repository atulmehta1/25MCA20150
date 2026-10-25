// MongoDB / Mongoose Quiz Schema Definition

const quizSchemaDefinition = {
  courseId: { type: String, ref: 'Course', required: true },
  title: { type: String, required: true },
  durationMinutes: { type: Number, default: 10 },
  passingScore: { type: Number, default: 70 },
  questions: [
    {
      id: String,
      question: { type: String, required: true },
      options: [{ type: String, required: true }],
      correctIndex: { type: Number, required: true },
      explanation: { type: String }
    }
  ],
  createdAt: { type: Date, default: Date.now }
};

module.exports = quizSchemaDefinition;
