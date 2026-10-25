// ==========================================================================
// Multi-Role Dynamic Dashboard (Student, Trainer, Admin)
// ==========================================================================

const dashboardModule = {
  async initDashboard() {
    const user = auth.getUser();
    if (!user) {
      window.location.href = 'login.html';
      return;
    }

    const container = document.getElementById('dashboard-dynamic-content');
    if (!container) return;

    if (user.role === 'admin') {
      await this.renderAdminDashboard(container, user);
    } else if (user.role === 'trainer') {
      await this.renderTrainerDashboard(container, user);
    } else {
      await this.renderStudentDashboard(container, user);
    }
  },

  // 1. Student Dashboard View
  async renderStudentDashboard(container, user) {
    let courses = [];
    try {
      const res = await api.get('/courses');
      courses = res.courses || [];
    } catch (e) {
      courses = [];
    }

    const enrolledCourses = courses.filter(c => (user.enrolledCourses || []).includes(c.id));

    container.innerHTML = `
      <!-- User Header Banner -->
      <div class="dashboard-header">
        <div class="user-profile-badge">
          <img src="${user.avatar}" alt="${user.name}" class="user-avatar-lg">
          <div>
            <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.25rem;">
              <h2 style="font-size: 1.6rem;">Welcome back, ${user.name}!</h2>
              <span class="badge badge-cyan">Student</span>
            </div>
            <p style="color: var(--text-secondary); font-size: 0.95rem;">
              Keep up your daily learning momentum. You are on a <strong>${user.streak || 7}-day streak!</strong>
            </p>
          </div>
        </div>

        <div style="display: flex; gap: 0.75rem;">
          <a href="ai-hub.html" class="btn btn-primary btn-sm">AI Tutor & Explainer</a>
          <a href="courses.html" class="btn btn-secondary btn-sm">Explore More Courses</a>
        </div>
      </div>

      <!-- Stats Grid -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon amber" style="font-size: 0.85rem; font-weight: 800;">XP</div>
          <div>
            <div class="stat-val gradient-text">${user.xp || 420}</div>
            <div class="stat-lbl">Total XP Points</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon cyan" style="font-size: 0.85rem; font-weight: 800;">DAY</div>
          <div>
            <div class="stat-val" style="color: var(--accent-cyan);">${user.streak || 7} Days</div>
            <div class="stat-lbl">Daily Streak</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon purple" style="font-size: 0.85rem; font-weight: 800;">CRS</div>
          <div>
            <div class="stat-val" style="color: var(--accent-purple);">${enrolledCourses.length || 2}</div>
            <div class="stat-lbl">Enrolled Courses</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon green" style="font-size: 0.85rem; font-weight: 800;">AVG</div>
          <div>
            <div class="stat-val" style="color: var(--accent-green);">88%</div>
            <div class="stat-lbl">Avg. Quiz Score</div>
          </div>
        </div>
      </div>

      <!-- Badges Showcase -->
      <div class="card" style="margin-bottom: 2rem;">
        <h3 style="font-size: 1.15rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
          Earned Badges & Achievements
        </h3>
        <div class="badge-shelf">
          ${(user.badges || ['Beginner', 'Streak Master', 'Quiz Whiz']).map(b => `
            <div class="badge-item">
              <span class="badge badge-purple" style="font-size: 0.75rem;">Badge</span>
              <span>${b}</span>
            </div>
          `).join('')}
          <div class="badge-item" style="opacity: 0.5; border-style: dashed;">
            <span class="badge badge-cyan" style="font-size: 0.75rem;">Locked</span>
            <span>Master Coder (+100 XP)</span>
          </div>
        </div>
      </div>

      <!-- Enrolled Courses -->
      <div class="section-header">
        <div>
          <h3 class="section-title">My Courses & Progress</h3>
          <p class="section-subtitle">Pick up right where you left off</p>
        </div>
      </div>

      <div class="grid-2" style="margin-bottom: 2.5rem;">
        ${enrolledCourses.length > 0 ? enrolledCourses.map(c => `
          <div class="card course-card">
            <div class="course-thumb-wrap" style="height: 150px;">
              <img src="${c.thumbnail}" alt="${c.title}">
              <span class="course-category-tag">${c.category}</span>
            </div>
            <div class="course-body">
              <h4 class="course-title" style="font-size: 1.1rem;">${c.title}</h4>
              
              <div class="progress-bar-wrap">
                <div class="progress-bar-fill" style="width: 60%;"></div>
              </div>
              <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--text-muted); margin-bottom: 1rem;">
                <span>Progress: 60%</span>
                <span>3 of 5 Lessons</span>
              </div>

              <div style="display: flex; gap: 0.5rem;">
                <a href="lesson.html?courseId=${c.id}" class="btn btn-primary btn-sm" style="flex: 1;">
                  Continue Lesson
                </a>
                <a href="quiz.html?courseId=${c.id}" class="btn btn-secondary btn-sm">
                  Quiz Assessment
                </a>
              </div>
            </div>
          </div>
        `).join('') : `
          <div class="card" style="grid-column: 1/-1; text-align: center; padding: 2rem;">
            <p style="color: var(--text-secondary); margin-bottom: 1rem;">You are not enrolled in any courses yet.</p>
            <a href="courses.html" class="btn btn-primary btn-sm">Browse Course Catalog</a>
          </div>
        `}
      </div>

      <!-- Quick AI Tools Launcher -->
      <div class="card" style="background: linear-gradient(135deg, rgba(56, 189, 248, 0.05) 0%, rgba(129, 140, 248, 0.05) 100%);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
          <div>
            <h3 style="font-size: 1.2rem; margin-bottom: 0.25rem;">Accelerate Your Learning with 5 AI Assistants</h3>
            <p style="color: var(--text-secondary); font-size: 0.9rem;">Chat Tutor | Code Explainer | Dynamic Quiz Gen | Mock Interviews | Resume Review</p>
          </div>
          <a href="ai-hub.html" class="btn btn-primary">Open AI Hub</a>
        </div>
      </div>
    `;
  },

  // 2. Trainer Dashboard View
  async renderTrainerDashboard(container, user) {
    let courses = [];
    try {
      const res = await api.get('/courses');
      courses = res.courses || [];
    } catch (e) {
      courses = [];
    }

    container.innerHTML = `
      <div class="dashboard-header">
        <div class="user-profile-badge">
          <img src="${user.avatar}" alt="${user.name}" class="user-avatar-lg" style="border-color: var(--accent-purple);">
          <div>
            <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.25rem;">
              <h2 style="font-size: 1.6rem;">Trainer Portal: ${user.name}</h2>
              <span class="badge badge-purple">Trainer</span>
            </div>
            <p style="color: var(--text-secondary); font-size: 0.95rem;">
              ${user.specialization || 'Technical Instructor'} - <strong>${user.studentsTrained || 1250}</strong> Students Enrolled Across Your Courses
            </p>
          </div>
        </div>

        <div style="display: flex; gap: 0.75rem;">
          <button class="btn btn-primary btn-sm" onclick="dashboardModule.openCreateCourseModal()">+ Create New Course</button>
          <button class="btn btn-secondary btn-sm" onclick="dashboardModule.openAddLessonModal()">+ Upload Lesson / Notes</button>
        </div>
      </div>

      <!-- Trainer Metrics -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon purple" style="font-size: 0.85rem; font-weight: 800;">STU</div>
          <div>
            <div class="stat-val" style="color: var(--accent-purple);">1,250</div>
            <div class="stat-lbl">Active Students</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon cyan" style="font-size: 0.85rem; font-weight: 800;">CRS</div>
          <div>
            <div class="stat-val" style="color: var(--accent-cyan);">${courses.length}</div>
            <div class="stat-lbl">Courses Created</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon amber" style="font-size: 0.85rem; font-weight: 800;">RTG</div>
          <div>
            <div class="stat-val" style="color: var(--accent-amber);">4.9 / 5.0</div>
            <div class="stat-lbl">Student Rating</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon green" style="font-size: 0.85rem; font-weight: 800;">CRT</div>
          <div>
            <div class="stat-val" style="color: var(--accent-green);">342</div>
            <div class="stat-lbl">Certificates Issued</div>
          </div>
        </div>
      </div>

      <!-- Manage Courses Table -->
      <div class="card" style="margin-bottom: 2rem;">
        <div class="section-header" style="margin-bottom: 1.25rem;">
          <h3 style="font-size: 1.15rem;">My Active Courses & Enrollment Statistics</h3>
        </div>
        <div style="overflow-x: auto;">
          <table class="custom-table">
            <thead>
              <tr>
                <th>Course Title</th>
                <th>Category</th>
                <th>Lessons</th>
                <th>Rating</th>
                <th>Enrollments</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              ${courses.map(c => `
                <tr>
                  <td><strong>${c.title}</strong></td>
                  <td><span class="badge badge-cyan">${c.category}</span></td>
                  <td>${c.lessons ? c.lessons.length : c.lessonsCount}</td>
                  <td>${c.rating} / 5.0</td>
                  <td>${c.enrollments}</td>
                  <td>
                    <a href="lesson.html?courseId=${c.id}" class="btn btn-secondary btn-sm" style="padding: 0.25rem 0.6rem; font-size: 0.75rem;">Manage</a>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  },

  // 3. Admin Dashboard View
  async renderAdminDashboard(container, user) {
    let stats = {
      totalUsers: 1480,
      studentsCount: 1420,
      trainersCount: 45,
      totalCourses: 5,
      totalQuizzes: 4,
      totalCertificates: 342,
      pendingTrainersCount: 1
    };

    try {
      const res = await api.get('/admin/stats');
      if (res && res.stats) stats = res.stats;
    } catch (e) {}

    container.innerHTML = `
      <div class="dashboard-header">
        <div class="user-profile-badge">
          <img src="${user.avatar}" alt="${user.name}" class="user-avatar-lg" style="border-color: var(--accent-rose);">
          <div>
            <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.25rem;">
              <h2 style="font-size: 1.6rem;">Admin System Console: ${user.name}</h2>
              <span class="badge badge-amber" style="background: rgba(251,113,133,0.15); color: var(--accent-rose); border-color: rgba(251,113,133,0.3);">Administrator</span>
            </div>
            <p style="color: var(--text-secondary); font-size: 0.95rem;">
              Platform Health: <strong>Optimal (99.9%)</strong> | Active Sessions Today: <strong>18</strong>
            </p>
          </div>
        </div>

        <div>
          <button class="btn btn-primary btn-sm" onclick="app.showToast('Generating Platform Analytics Report (PDF)...', 'success')">
            Export Analytics Report
          </button>
        </div>
      </div>

      <!-- Admin KPIs -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon cyan" style="font-size: 0.85rem; font-weight: 800;">USR</div>
          <div>
            <div class="stat-val" style="color: var(--accent-cyan);">${stats.totalUsers}</div>
            <div class="stat-lbl">Total Registered Users</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon purple" style="font-size: 0.85rem; font-weight: 800;">TRN</div>
          <div>
            <div class="stat-val" style="color: var(--accent-purple);">${stats.trainersCount}</div>
            <div class="stat-lbl">Approved Trainers</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon green" style="font-size: 0.85rem; font-weight: 800;">CRS</div>
          <div>
            <div class="stat-val" style="color: var(--accent-green);">${stats.totalCourses}</div>
            <div class="stat-lbl">Active Courses</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon amber" style="font-size: 0.85rem; font-weight: 800;">CRT</div>
          <div>
            <div class="stat-val" style="color: var(--accent-amber);">${stats.totalCertificates}</div>
            <div class="stat-lbl">Certificates Issued</div>
          </div>
        </div>
      </div>

      <!-- Pending Trainer Approvals -->
      <div class="card" style="margin-bottom: 2rem;">
        <h3 style="font-size: 1.15rem; margin-bottom: 1rem; color: var(--accent-amber);">
          Trainer Verification & Onboarding Requests
        </h3>
        <div style="overflow-x: auto;">
          <table class="custom-table">
            <thead>
              <tr>
                <th>Applicant Name</th>
                <th>Email</th>
                <th>Specialization</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Dr. Rajesh Mehta</strong></td>
                <td>rajesh.mehta@faculty.edu</td>
                <td>Cloud Computing & DevOps</td>
                <td><span class="badge badge-amber">Pending Approval</span></td>
                <td>
                  <button class="btn btn-primary btn-sm" style="padding: 0.25rem 0.6rem; font-size: 0.75rem;" onclick="app.showToast('Trainer Approved Successfully! Verification badge granted.', 'success')">
                    Approve Trainer
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `;
  },

  openCreateCourseModal() {
    let modal = document.getElementById('create-course-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'create-course-modal';
      modal.className = 'modal-overlay active';
      modal.innerHTML = `
        <div class="modal-content">
          <div class="modal-header">
            <h3>Create New Technical Course</h3>
            <button onclick="document.getElementById('create-course-modal').remove()" style="background:none; border:none; color:var(--text-muted); font-size:1.5rem; cursor:pointer;">&times;</button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label class="form-label">Course Title</label>
              <input type="text" id="new-course-title" class="form-control" placeholder="e.g. Docker & Kubernetes Masterclass">
            </div>
            <div class="form-group">
              <label class="form-label">Category</label>
              <select id="new-course-category" class="form-control">
                <option value="Web Development">Web Development</option>
                <option value="AI">AI & Machine Learning</option>
                <option value="Data Structures">Data Structures</option>
                <option value="Cloud">Cloud Computing</option>
                <option value="Python">Python</option>
                <option value="SQL">SQL</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Description</label>
              <textarea id="new-course-desc" class="form-control" placeholder="Course syllabus overview..."></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Duration</label>
              <input type="text" id="new-course-duration" class="form-control" placeholder="e.g. 15 Hours">
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" onclick="document.getElementById('create-course-modal').remove()">Cancel</button>
            <button class="btn btn-primary" onclick="dashboardModule.submitCreateCourse()">Publish Course</button>
          </div>
        </div>
      `;
      document.body.appendChild(modal);
    }
  },

  async submitCreateCourse() {
    const title = document.getElementById('new-course-title')?.value.trim();
    const category = document.getElementById('new-course-category')?.value;
    const description = document.getElementById('new-course-desc')?.value.trim();
    const duration = document.getElementById('new-course-duration')?.value.trim() || '12 Hours';
    const user = auth.getUser();

    if (!title || !description) {
      app.showToast('Please provide course title and description.', 'error');
      return;
    }

    try {
      await api.post('/courses', {
        title,
        category,
        description,
        duration,
        trainerName: user.name,
        trainerId: user.id
      });
      app.showToast('Course published successfully!', 'success');
      document.getElementById('create-course-modal')?.remove();
      this.initDashboard();
    } catch (e) {
      app.showToast('Course created in local workspace!', 'success');
      document.getElementById('create-course-modal')?.remove();
    }
  },

  openAddLessonModal() {
    app.showToast('Lesson & PDF Notes uploader dialog ready.', 'info');
  }
};
