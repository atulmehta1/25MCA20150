// ==========================================================================
// Course Catalog, Video Player Classroom & Coding Practice
// ==========================================================================

const courseModule = {
  courses: [],
  activeCategory: 'All',
  currentCourse: null,
  currentLessonIdx: 0,

  async initCatalog() {
    await this.fetchCourses();
    this.renderCategoryChips();
    this.renderCoursesGrid();
  },

  async fetchCourses() {
    try {
      const res = await api.get('/courses');
      if (res && res.courses) {
        this.courses = res.courses;
      }
    } catch (e) {
      console.warn("Using local courses fallback:", e);
    }
  },

  renderCategoryChips() {
    const bar = document.getElementById('category-filter-chips');
    if (!bar) return;

    const categories = ['All', 'Web Development', 'AI', 'Data Structures', 'SQL', 'Aptitude'];
    bar.innerHTML = categories.map(cat => `
      <button class="category-chip ${this.activeCategory === cat ? 'active' : ''}" onclick="courseModule.filterByCategory('${cat}')">
        ${cat}
      </button>
    `).join('');
  },

  filterByCategory(cat) {
    this.activeCategory = cat;
    this.renderCategoryChips();
    this.renderCoursesGrid();
  },

  searchCourses(query) {
    const q = query.toLowerCase().trim();
    const filtered = this.courses.filter(c =>
      (this.activeCategory === 'All' || c.category === this.activeCategory) &&
      (c.title.toLowerCase().includes(q) || c.description.toLowerCase().includes(q) || c.trainerName.toLowerCase().includes(q))
    );
    this.renderCoursesList(filtered);
  },

  renderCoursesGrid() {
    let list = this.courses;
    if (this.activeCategory !== 'All') {
      list = list.filter(c => c.category.toLowerCase() === this.activeCategory.toLowerCase());
    }
    this.renderCoursesList(list);
  },

  renderCoursesList(list) {
    const container = document.getElementById('courses-grid-container');
    if (!container) return;

    if (!list || list.length === 0) {
      container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-secondary);">No courses found matching this criteria.</div>`;
      return;
    }

    const user = auth.getUser();
    const enrolledIds = user ? (user.enrolledCourses || []) : [];

    container.innerHTML = list.map(c => {
      const isEnrolled = enrolledIds.includes(c.id);
      return `
        <div class="card course-card">
          <div class="course-thumb-wrap">
            <img src="${c.thumbnail}" alt="${c.title}" loading="lazy">
            <span class="course-category-tag">${c.category}</span>
          </div>
          <div class="course-body">
            <h3 class="course-title">${c.title}</h3>
            <p class="course-desc">${c.description}</p>
            
            <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.75rem;">
              Instructor: <strong>${c.trainerName}</strong>
            </div>

            <div class="course-meta">
              <span>Duration: ${c.duration}</span>
              <span>Rating: ${c.rating} (${c.enrollments})</span>
              <span>${c.lessons ? c.lessons.length : c.lessonsCount} Lessons</span>
            </div>

            <div style="margin-top: 1rem; display: flex; gap: 0.5rem;">
              ${isEnrolled ? `
                <a href="lesson.html?courseId=${c.id}" class="btn btn-primary btn-sm" style="flex: 1;">
                  Continue Learning
                </a>
              ` : `
                <button class="btn btn-primary btn-sm" style="flex: 1;" onclick="courseModule.enrollCourse('${c.id}')">
                  Enroll Free
                </button>
              `}
              <a href="lesson.html?courseId=${c.id}" class="btn btn-secondary btn-sm" title="Preview Syllabus">
                View
              </a>
            </div>
          </div>
        </div>
      `;
    }).join('');
  },

  async enrollCourse(courseId) {
    const user = auth.getUser();
    if (!user) {
      window.location.href = 'login.html';
      return;
    }

    try {
      await api.post(`/courses/enroll/${courseId}`, { userId: user.id });
      user.enrolledCourses = user.enrolledCourses || [];
      if (!user.enrolledCourses.includes(courseId)) {
        user.enrolledCourses.push(courseId);
        auth.setUser(user);
      }
      app.showToast('Enrolled successfully! +50 XP Welcome Bonus', 'success');
      this.renderCoursesGrid();
    } catch (e) {
      app.showToast('Enrollment processed!', 'success');
      user.enrolledCourses = user.enrolledCourses || [];
      user.enrolledCourses.push(courseId);
      auth.setUser(user);
      this.renderCoursesGrid();
    }
  },

  // ----------------------------------------------------
  // Classroom & Lesson Player Page Logic
  // ----------------------------------------------------
  async initClassroom() {
    const params = new URLSearchParams(window.location.search);
    const courseId = params.get('courseId') || 'c1';

    await this.fetchCourses();
    this.currentCourse = this.courses.find(c => c.id === courseId) || this.courses[0];
    if (!this.currentCourse) return;

    this.renderClassroomUI();
  },

  renderClassroomUI() {
    const c = this.currentCourse;
    const lesson = c.lessons && c.lessons[this.currentLessonIdx] ? c.lessons[this.currentLessonIdx] : null;

    document.getElementById('course-header-title').innerText = c.title;
    document.getElementById('course-header-category').innerText = c.category;

    if (lesson) {
      document.getElementById('current-lesson-title').innerText = lesson.title;
      document.getElementById('current-lesson-summary').innerText = lesson.summary;

      // Update video source
      const videoEl = document.getElementById('lesson-video-player');
      if (videoEl && lesson.videoUrl) {
        videoEl.src = lesson.videoUrl;
      }

      // Update PDF download link
      const pdfBtn = document.getElementById('pdf-download-btn');
      if (pdfBtn) {
        pdfBtn.innerText = `Download Notes (${lesson.pdfTitle})`;
      }

      // Update Coding practice box
      if (lesson.codePractice) {
        document.getElementById('practice-title').innerText = lesson.codePractice.title;
        document.getElementById('practice-instruction').innerText = lesson.codePractice.instructions;
        document.getElementById('practice-code-area').value = lesson.codePractice.starterCode;
        document.getElementById('practice-solution-box').innerText = lesson.codePractice.solution;
        document.getElementById('practice-solution-box').style.display = 'none';
      }
    }

    this.renderPlaylist();
    this.updateProgressBar();
  },

  renderPlaylist() {
    const container = document.getElementById('playlist-items-container');
    if (!container || !this.currentCourse.lessons) return;

    const user = auth.getUser();
    const completed = user ? (user.completedLessons || []) : [];

    container.innerHTML = this.currentCourse.lessons.map((l, idx) => {
      const isDone = completed.includes(l.id);
      const isActive = idx === this.currentLessonIdx;

      return `
        <div class="playlist-item ${isActive ? 'active' : ''} ${isDone ? 'completed' : ''}" onclick="courseModule.switchLesson(${idx})">
          <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div class="lesson-check-icon">
              ${isDone ? 'Done' : (idx + 1)}
            </div>
            <div>
              <div style="font-size: 0.9rem; font-weight: 600; line-height: 1.2;">${l.title}</div>
              <span style="font-size: 0.75rem; color: var(--text-muted);">${l.duration}</span>
            </div>
          </div>
          ${isDone ? `<span class="badge badge-green" style="font-size: 0.65rem;">Done</span>` : ''}
        </div>
      `;
    }).join('');
  },

  switchLesson(idx) {
    this.currentLessonIdx = idx;
    this.renderClassroomUI();
  },

  async markCurrentLessonComplete() {
    const lesson = this.currentCourse.lessons[this.currentLessonIdx];
    const user = auth.getUser();
    if (!lesson || !user) return;

    try {
      const res = await api.post('/courses/complete-lesson', {
        userId: user.id,
        lessonId: lesson.id,
        courseId: this.currentCourse.id
      });

      user.completedLessons = user.completedLessons || [];
      if (!user.completedLessons.includes(lesson.id)) {
        user.completedLessons.push(lesson.id);
        user.xp = (user.xp || 420) + 10;
        auth.setUser(user);
      }

      app.showToast('Lesson Completed! Earned +10 XP', 'success');
      this.renderPlaylist();
      this.updateProgressBar();

      // Check if all lessons are completed -> suggest Quiz
      const allDone = this.currentCourse.lessons.every(l => user.completedLessons.includes(l.id));
      if (allDone) {
        app.showToast('Course completed! Ready to take final Quiz for Certificate', 'success');
      }
    } catch (e) {
      user.completedLessons = user.completedLessons || [];
      user.completedLessons.push(lesson.id);
      auth.setUser(user);
      this.renderPlaylist();
      this.updateProgressBar();
    }
  },

  updateProgressBar() {
    const user = auth.getUser();
    const completed = user ? (user.completedLessons || []) : [];
    const total = this.currentCourse.lessons ? this.currentCourse.lessons.length : 1;
    const courseDoneCount = this.currentCourse.lessons ? this.currentCourse.lessons.filter(l => completed.includes(l.id)).length : 0;
    const percent = Math.round((courseDoneCount / total) * 100);

    const barFill = document.getElementById('classroom-progress-fill');
    const label = document.getElementById('classroom-progress-label');
    if (barFill) barFill.style.width = `${percent}%`;
    if (label) label.innerText = `${percent}% Completed (${courseDoneCount}/${total} Lessons)`;
  },

  runCodePractice() {
    const code = document.getElementById('practice-code-area')?.value || '';
    const outputBox = document.getElementById('practice-console-output');
    outputBox.style.display = 'block';

    const logs = [];
    const originalLog = console.log;
    console.log = function(...args) {
      logs.push(args.map(a => typeof a === 'object' ? JSON.stringify(a) : a).join(' '));
      originalLog.apply(console, args);
    };

    try {
      const result = eval(code);
      console.log = originalLog;
      outputBox.innerHTML = `
        <span style="color: var(--accent-green);">Execution Successful:</span>\n${logs.join('\n') || (result !== undefined ? String(result) : 'Execution finished with code 0.')}
      `;
      app.showToast('Code executed successfully! +5 XP', 'success');
    } catch (err) {
      console.log = originalLog;
      outputBox.innerHTML = `<span style="color: var(--accent-rose);">Syntax/Runtime Error: ${err.message}</span>`;
    }
  },

  toggleSolution() {
    const box = document.getElementById('practice-solution-box');
    if (box) {
      box.style.display = box.style.display === 'none' ? 'block' : 'none';
    }
  }
};
