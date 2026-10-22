# FocusForge — Smart Study & Productivity Hub

A Full-Stack Study Planner and Productivity Analytics Platform built with the **MERN** stack (MongoDB, Express.js, React, Node.js).

---

## 🚀 Quick Start

### 1. Start the Full Application (Frontend + Backend)
From the project root:
```bash
npm start
```
*(or `npm run dev` or `node start.js` or double-click `run-project.bat`)*

- **Frontend App**: [http://localhost:5173](http://localhost:5173)
- **Backend API**: [http://localhost:5000](http://localhost:5000)

---

## ⚡ Instant Viva Demo Account
When opening the login screen, click **"⚡ One-Click Viva Demo Login"** or sign in manually:
- **Email:** `alex@focusforge.com`
- **Password:** `password123`

To reset or re-seed realistic demo data (subjects, tasks, 7-day study history):
```bash
npm run seed
```

---

## 🌟 Key Features

### A. Personal Dashboard (`/`)
- Dynamic time-of-day greeting & motivational quotes with randomizer
- Daily metrics: **Today's Focus Minutes**, **Tasks Completed Today**, **Active Study Streak**, and **Overdue Task Warnings**
- Interactive **Weekly Study-Time AreaChart** (Recharts)
- Today's agenda & upcoming deadlines list with direct task completion toggles

### B. Smart Task & Academic Subject Manager (`/tasks`)
- Create, edit, toggle completion, and delete tasks
- Filter by Subject, Priority (High, Medium, Low), and Status (Pending, Completed), plus keyword search
- Dedicated **Subject Manager** (`Machine Learning`, `IoT Systems`, `Technical Training`, etc.) with customizable color pills and task counters
- One-click **"Focus"** launcher to instantly open any task inside the Focus Room

### C. Focus Room — Signature Feature (`/focus`)
- Circular SVG Pomodoro timer with animated progress ring
- Preset modes: **Focus (25m)**, **Short Break (5m)**, **Long Break (15m)**
- Task selector: Link focus session to a specific pending task
- Option to auto-mark task completed upon session finish
- **Offline Web Audio API Sound System**:
  - Crystal Bell completion chime
  - Synthesized soothing rainfall/pink noise toggle
- Confetti celebration upon session completion
- Saves completed sessions to MongoDB and displays today's focused time & session log

### D. Study Planner (`/planner`)
- 7-Day interactive agenda strip with task counts per day
- Calendar day selection with direct **"Add for this Day"** action
- Overdue tasks warning panel with direct "Resolve" button

### E. Analytics & Progress (`/analytics`)
- Filter by timeframe (**Last 7 Days**, **Last 30 Days**)
- **Study Time Trend AreaChart** (daily minutes & hours)
- **Task Completion Status Donut Chart** (Completed vs Pending)
- **Subject-Wise Study Distribution BarChart** (time per academic subject)
- **Export Study History as CSV** (one-click download)
- **Gamified Achievements**:
  - *First Step* (First completed session)
  - *Century Club* (100+ study minutes)
  - *Pomodoro Pro* (10+ completed focus sessions)
  - *Task Crusher* (10+ completed study tasks)
  - *Streak Master* (3+ day study streak)
  - *Master Scholar* (500+ study minutes)

### F. Modern Aesthetic & Extras
- **Dark & Light Mode** toggle with persistent storage
- Glassmorphism design system with responsive layouts
- Secure JWT authentication in HTTP-Only cookies + Bearer token support
- Strict user-isolation across all MongoDB queries

---

## 🏗️ Technology Stack

| Layer | Tools |
|---|---|
| **Frontend** | React 18 + Vite |
| **Routing** | React Router v6 |
| **Icons** | Lucide React |
| **Charts** | Recharts |
| **Styling** | Vanilla CSS Design System (Custom Glassmorphism, CSS Variables) |
| **Audio** | Web Audio API Synthesizer (Crystal Chime, Pink Noise) |
| **Celebration** | Canvas Confetti |
| **HTTP Client** | Axios (with token interceptors) |
| **Backend** | Node.js + Express (ES Modules) |
| **Database** | MongoDB + Mongoose |
| **Authentication**| JWT + bcryptjs |

---

## 🗄️ Database Schemas (MongoDB)

1. **`users`**: `name`, `email`, `passwordHash`, `settings`, `createdAt`
2. **`subjects`**: `userId` (ref: User), `name`, `color`, `createdAt`
3. **`tasks`**: `userId`, `subjectId` (ref: Subject), `title`, `description`, `priority` (low/medium/high), `status` (pending/completed), `dueDate`, `estimatedMinutes`, `completedAt`
4. **`focusSessions`**: `userId`, `taskId` (ref: Task), `subjectId` (ref: Subject), `durationMinutes`, `startedAt`, `endedAt`, `status` (completed/cancelled), `notes`
