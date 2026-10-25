# AI Technical Training Platform (Enhanced Version)
> **Master of Computer Applications (MCA) Mini Project**  
> A Next-Generation, Role-Based E-Learning & Assessment Platform Powered by 5 Technical AI Learning Assistants.

---

## 1. Project Abstract & Objectives
Technical recruitment and university computer science curricula demand practical problem-solving skills, conceptual clarity in algorithms, and placement interview readiness.

The **AI Technical Training Platform** is a full-stack, modular web application designed to bridge the gap between classroom theory and industry demands. It features:
- **3 User Roles**: Student (Atul Mehta), Trainer (Dr. Priya Nair), and Administrator (Vikram Malhotra).
- **5 Core AI Features**: AI Chat Tutor, AI Code Explainer, AI Quiz Generator, AI Mock Technical & HR Interview, and AI Resume Review & ATS Optimizer.
- **Interactive Learning Features**: Curated video lessons, in-browser coding practice with execution engine, downloadable study notes, and category filters.
- **Gamification Arena**: XP Points (+10 XP per lesson, +20 XP per quiz, +100 XP per course), Daily Streak Tracker, Badges (Beginner to Expert), and Global Leaderboard.
- **Automated Assessments & Verified Certificates**: Timed assessments, instant auto-grading, answer reviews with explanations, and Canvas-based verifiable completion certificates.

---

## 2. User Roles & Capabilities

| Feature / Capability | Student | Trainer | Admin |
|---|:---:|:---:|:---:|
| **Authentication & Profile** | Register / Login / Profile | Register / Await Approval | Full Access |
| **Course Enrollment** | Enroll & Track Progress | Manage Own Courses | Manage All Courses |
| **Classroom Experience** | Video Lessons & Progress | Upload Video/PDF Notes | Monitor Quality |
| **In-Browser Code Practice** | Run Code & View Solutions | Add Code Exercises | System Audit |
| **Assessment & Quizzes** | Take Timed MCQ Tests | Create Custom Quizzes | Review Attempts |
| **Verified Certificates** | Auto-Earn & Download PNG | Issue on 70%+ score | Verify & Invalidate |
| **AI Hub Assistants** | Full Access to 5 AI Tools | Course AI Generation | System AI Monitoring |
| **Community Forum** | Ask Questions & Reply | Official Verified Badges | Moderate Content |
| **Platform Governance** | View Personal Dashboard | View Student Analytics | Approve Trainers & KPIs |

---

## 3. The 5 Core AI Learning Assistants

### 1. AI Chat Tutor
- Instant conceptual breakdowns for complex topics (e.g. JavaScript Promises, Closures, Event Loop, Binary Search, SQL Joins).
- Emits structured explanations, runnable code snippets, and key takeaways.
- Preset one-click quick prompt chips for common exam doubts.

### 2. AI Code Explainer
- Analyzes pasted code in JavaScript, Python, Java, and C++.
- Generates line-by-line explanations of variable scope, conditionals, and loops.
- Computes Time Complexity (e.g. O(1), O(log N), O(N), O(N^2)) and Space Complexity.
- Suggests boundary validation and defensive coding improvements.

### 3. AI Quiz Generator
- Generates 5 dynamic MCQs on any selected topic (Node.js, Python, React, SQL, DSA).
- Instant clickable option verification with explanation reveal and +5 XP rewards.

### 4. AI Mock Interview Preparation
- Simulates real company placement rounds (Technical Architecture & HR Behavioral).
- Allows candidate to draft responses using the STAR Method (Situation, Task, Action, Result).
- Evaluates student response with an AI Score (0-100), grading criteria, and reveals high-scoring model answers.

### 5. AI Resume Review & ATS Optimizer
- Scans resume text against industry developer job descriptions.
- Calculates an ATS Compatibility Gauge (0-100%).
- Highlights Detected Technical Skills and flags Missing In-Demand Skills (e.g., Docker, AWS, Redis).
- Recommends tailored courses on the platform to bridge skill gaps.

---

## 4. Gamification System

- **XP Points Progression:**
  - Complete a Video Lesson: **+10 XP**
  - Pass an Assessment Quiz: **+20 XP**
  - Finish Entire Course: **+100 XP**
  - Daily Streak Bonus: **+10 XP**
- **Achievement Badges:**
  - **Tier 1 (Beginner)**: Enrolled in first course.
  - **Tier 2 (Intermediate)**: Earned 300+ XP points.
  - **Tier 3 (Advanced)**: Scored 80%+ on 3 assessments.
  - **Tier 4 (Expert)**: 1000+ XP points.
- **Global Leaderboard:**
  - Real-time learner rankings filtered by Overall, Weekly, and Monthly points.

---

## 5. Clean Project Structure (MCA Standard)

```text
AI-Technical-Training-Platform/
│
├── .gitignore                   # Prevents heavy node_modules from uploading to GitHub
├── package.json                 # Minimal lightweight dependencies (Express & CORS)
├── README.md                    # Project documentation & Viva guide
├── server.js                    # Root server forwarder
│
├── server/                      # Backend REST API Server
│   ├── server.js                # Main Express server (Serves API + Frontend client)
│   ├── db.js                    # Lightweight database with persistence & CRUD
│   │
│   ├── routes/
│   │   ├── authRoutes.js        # Login, registration, role switcher
│   │   ├── courseRoutes.js      # Courses, enrollment, lesson progress
│   │   ├── quizRoutes.js        # Quizzes, auto-grading, scoring
│   │   ├── aiRoutes.js          # The 5 AI Assistant endpoints
│   │   ├── forumRoutes.js       # Q&A community threads & upvotes
│   │   └── adminRoutes.js       # KPIs, stats, trainer approvals
│   │
│   ├── models/                  # Mongoose/MongoDB Schemas for Viva defense
│   │   ├── User.js
│   │   ├── Course.js
│   │   ├── Quiz.js
│   │   └── Certificate.js
│   │
│   ├── utils/
│   │   └── aiEngine.js          # AI knowledge engine & prompt analyzer
│   │
│   └── data/
│       └── initialData.json     # Pre-seeded database (users, courses, quizzes, forum)
│
└── client/                      # Modern Frontend Application (Vanilla HTML/CSS/JS)
    ├── index.html               # Main landing page & feature showcases
    │
    ├── css/
    │   ├── style.css            # Dark/light design system
    │   ├── dashboard.css        # Multi-role dashboard widgets & KPI cards
    │   ├── ai-tools.css         # Specialized styling for the 5 AI modules
    │   └── course.css           # Classroom player, quiz timer, and certificate styles
    │
    ├── js/
    │   ├── api.js               # Hybrid API client with auto offline fallback
    │   ├── auth.js              # Auth state & 1-click role switcher
    │   ├── app.js               # Dark/Light theme, toasts, notifications
    │   ├── ai.js                # Interactive controllers for all 5 AI tools
    │   ├── course.js            # Video player, playlist tracker, code runner
    │   ├── quiz.js              # Assessment timer, auto-grading, certificate trigger
    │   ├── certificate.js       # Canvas certificate rendering & PNG export
    │   ├── dashboard.js         # Student, Trainer, Admin dynamic dashboards
    │   └── forum.js             # Community forum interactions
    │
    └── pages/
        ├── login.html           # Sign In / Register with 1-click demo accounts
        ├── dashboard.html       # Dynamic Multi-Role Dashboard
        ├── courses.html         # Catalog with live filters & search
        ├── lesson.html          # Interactive Classroom & live coding runner
        ├── quiz.html            # Assessment Arena with countdown timer
        ├── ai-hub.html          # All 5 AI Tools in one unified workspace
        ├── leaderboard.html     # Gamification, Streaks, Badges, Ranks
        ├── certificate.html     # Certificate Viewer & Verification tool
        └── forum.html           # Discussion Forum
```

---

## 6. How to Run Locally in 2 Minutes

### Option A: Standard Full-Stack Mode (Express Server)
1. Make sure you have **Node.js** installed ([Download Node.js](https://nodejs.org/)).
2. Open terminal in the project root folder:
   ```bash
   npm install
   npm start
   ```
3. Open your browser at:
   ```text
   http://localhost:5000
   ```

### Option B: Zero-Install Standalone Mode (Direct Browser Click)
- Even without installing Node.js or when presenting offline, simply double-click:
  ```text
  client/index.html
  ```
- The built-in client simulation engine automatically handles all data, role switching, quizzes, and AI tools directly in your browser!

---

## 7. Pre-Configured Demo Accounts (For Viva & Presentation)

You can switch between any role with **1-click** from the Navbar dropdown, or log in manually:

| Role | Email | Password | What to Showcase |
|---|---|---|---|
| **Student** (Atul Mehta) | `student@demo.com` | `password123` | Enrolled courses, 7-day streak, 420 XP, video player, code practice, certificate download |
| **Trainer** (Dr. Priya Nair) | `trainer@demo.com` | `password123` | Course creation modal, lesson uploader, student enrollment statistics, verified forum replies |
| **Admin** (Vikram Malhotra) | `admin@demo.com` | `password123` | Platform KPIs (1,480 users), approve pending trainers, certificate verification |

---

## 8. How to Upload to GitHub (Step-by-Step for MCA Students)

Because we included a configured `.gitignore` that prevents heavy `node_modules` folders from being tracked, your repository is ultra-lightweight (< 2 MB) and will push in seconds:

1. Open Git Bash or Terminal in this folder:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: AI Technical Training Platform MCA Project"
   ```
2. Create a new repository on your GitHub account (e.g., `ai-technical-training-platform`).
3. Link and push:
   ```bash
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ai-technical-training-platform.git
   git push -u origin main
   ```

---

## 9. MCA Viva & Defense Q&A Cheatsheet

### Q1: What is the primary architecture of this application?
> **Answer:** The project follows a decoupled **Client-Server RESTful Architecture**. The frontend is built using standard Vanilla HTML5, CSS3, and ES6 JavaScript with a modern design system. The backend is powered by Node.js and Express.js, providing modular REST API endpoints for authentication, course curriculum, quizzes, discussion forums, and AI services.

### Q2: How does the AI Assistant suite function?
> **Answer:** The platform includes an extensible AI Engine (`server/utils/aiEngine.js`) that provides intelligent heuristic and NLP evaluations for:
> 1. Code explanation and Big-O complexity calculation.
> 2. On-demand MCQ generation for chosen technical topics.
> 3. Behavioral and technical interview preparation using the STAR evaluation rubric.
> 4. ATS keyword scanning and resume skill-gap analysis.
> It can also seamlessly connect to Google Gemini API for live generative responses.

### Q3: How is user authorization and role-based access handled?
> **Answer:** Each user record includes a `role` attribute (`student`, `trainer`, `admin`). Endpoints and dashboards dynamically adapt: Students can only view and enroll; Trainers can publish courses and lessons; Admins possess elevated governance privileges to approve instructors and audit metrics.

### Q4: How are certificates generated and verified?
> **Answer:** When a student achieves 80%+ completion and passes the quiz with 70%+, an official certificate is generated with a unique ID (e.g. `CERT-2024-8841`). The certificate is rendered using the **HTML5 Canvas API** (`client/js/certificate.js`) with custom calligraphy, borders, and verification seals, allowing instant high-resolution PNG export or verification by ID.

### Q5: How is data persisted?
> **Answer:** Data is managed through `server/db.js` which maintains an in-memory data store synchronized to `server/data/initialData.json`. For academic defense, formal Mongoose/MongoDB schemas are provided under `server/models/` demonstrating standard database normalization.

---

## License
This project is open-source under the **MIT License**. Created for MCA Mini Project & Educational Demonstration.
