// MongoDB / Mongoose Course Schema Definition for MCA Project

const courseSchemaDefinition = {
  title: { type: String, required: true },
  category: {
    type: String,
    enum: ['Web Development', 'Java', 'Python', 'C++', 'Data Structures', 'SQL', 'AI', 'Cloud', 'Aptitude'],
    required: true
  },
  trainerId: { type: String, ref: 'User', required: true },
  trainerName: { type: String, required: true },
  description: { type: String, required: true },
  level: { type: String, default: 'Beginner to Intermediate' },
  duration: { type: String, default: '12 Hours' },
  thumbnail: { type: String },
  rating: { type: Number, default: 5.0 },
  enrollments: { type: Number, default: 0 },
  lessons: [
    {
      id: String,
      title: String,
      duration: String,
      videoUrl: String,
      pdfTitle: String,
      pdfUrl: String,
      summary: String,
      codePractice: {
        title: String,
        instructions: String,
        starterCode: String,
        solution: String
      }
    }
  ],
  createdAt: { type: Date, default: Date.now }
};

module.exports = courseSchemaDefinition;
