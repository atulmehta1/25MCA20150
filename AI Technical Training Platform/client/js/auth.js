// ==========================================================================
// Authentication & Role Management (Student, Trainer, Admin)
// ==========================================================================

const DEFAULT_USERS = {
  student: {
    id: "u1",
    name: "Atul Mehta",
    email: "student@demo.com",
    role: "student",
    avatar: "https://api.dicebear.com/7.x/bottts/svg?seed=Atul",
    xp: 420,
    streak: 7,
    badges: ["Beginner", "Streak Master", "Quiz Whiz"],
    enrolledCourses: ["c1", "c2"],
    completedLessons: ["l1-1", "l1-2", "l1-3", "l2-1"]
  },
  trainer: {
    id: "u2",
    name: "Dr. Priya Nair",
    email: "trainer@demo.com",
    role: "trainer",
    avatar: "https://api.dicebear.com/7.x/bottts/svg?seed=Priya",
    specialization: "Full Stack & AI Systems",
    bio: "Senior Technical Architect and Corporate Trainer with 10+ years experience.",
    isApproved: true,
    coursesCount: 3,
    studentsTrained: 1250
  },
  admin: {
    id: "u3",
    name: "Vikram Malhotra",
    email: "admin@demo.com",
    role: "admin",
    avatar: "https://api.dicebear.com/7.x/bottts/svg?seed=Admin"
  }
};

const auth = {
  getUser() {
    const raw = localStorage.getItem('currentUser');
    if (raw) {
      try {
        const parsed = JSON.parse(raw);
        if (parsed.name === "Rahul Sharma") {
          parsed.name = "Atul Mehta";
          parsed.avatar = "https://api.dicebear.com/7.x/bottts/svg?seed=Atul";
          localStorage.setItem('currentUser', JSON.stringify(parsed));
        }
        return parsed;
      } catch (e) {}
    }
    // Default to Student for instant preview
    const defaultStudent = DEFAULT_USERS.student;
    this.setUser(defaultStudent);
    return defaultStudent;
  },

  setUser(user) {
    if (user && user.name === "Rahul Sharma") {
      user.name = "Atul Mehta";
      user.avatar = "https://api.dicebear.com/7.x/bottts/svg?seed=Atul";
    }
    localStorage.setItem('currentUser', JSON.stringify(user));
    this.updateNavbarUI();
  },

  getToken() {
    return localStorage.getItem('token') || 'demo-token';
  },

  setToken(token) {
    localStorage.setItem('token', token);
  },

  isLoggedIn() {
    return Boolean(this.getUser());
  },

  logout() {
    localStorage.removeItem('currentUser');
    localStorage.removeItem('token');
    window.location.reload();
  },

  // One-click quick role switcher (Student, Trainer, Admin)
  switchRole(roleName) {
    if (DEFAULT_USERS[roleName]) {
      const selected = DEFAULT_USERS[roleName];
      this.setUser(selected);
      this.setToken('token-' + roleName);
      
      // Show toast alert without emoji
      if (typeof app !== 'undefined' && app.showToast) {
        app.showToast(`Switched active role to: ${selected.name} (${selected.role.toUpperCase()})`);
      } else {
        alert(`Switched active role to: ${selected.name} (${selected.role.toUpperCase()})`);
      }

      // If on dashboard, reload to show role-specific dashboard
      if (window.location.pathname.includes('dashboard')) {
        setTimeout(() => window.location.reload(), 400);
      } else {
        this.updateNavbarUI();
      }
    }
  },

  async login(email, password) {
    const res = await api.post('/auth/login', { email, password });
    if (res.success && res.user) {
      this.setUser(res.user);
      this.setToken(res.token);
      return res;
    }
    throw new Error(res.message || 'Login failed.');
  },

  async register(name, email, password, role = 'student') {
    const res = await api.post('/auth/register', { name, email, password, role });
    if (res.success && res.user) {
      this.setUser(res.user);
      this.setToken(res.token);
      return res;
    }
    throw new Error(res.message || 'Registration failed.');
  },

  updateNavbarUI() {
    const user = this.getUser();
    const navUserSlot = document.getElementById('nav-user-slot');
    if (!navUserSlot) return;

    if (!user) {
      navUserSlot.innerHTML = `
        <a href="pages/login.html" class="btn btn-secondary btn-sm">Sign In</a>
        <a href="pages/login.html?tab=register" class="btn btn-primary btn-sm">Register</a>
      `;
      return;
    }

    const roleBadgeClass = user.role === 'admin' ? 'badge-rose' : user.role === 'trainer' ? 'badge-purple' : 'badge-cyan';
    
    navUserSlot.innerHTML = `
      <div style="display: flex; align-items: center; gap: 0.75rem;">
        <!-- Role quick switch dropdown without emojis -->
        <select id="role-selector-dropdown" class="form-control" style="width: auto; padding: 0.35rem 0.6rem; font-size: 0.8rem;" onchange="auth.switchRole(this.value)">
          <option value="student" ${user.role === 'student' ? 'selected' : ''}>Student</option>
          <option value="trainer" ${user.role === 'trainer' ? 'selected' : ''}>Trainer</option>
          <option value="admin" ${user.role === 'admin' ? 'selected' : ''}>Admin</option>
        </select>

        ${user.role === 'student' ? `<span class="badge badge-amber" title="XP Points">${user.xp || 420} XP</span>` : ''}
        ${user.role === 'student' ? `<span class="badge badge-cyan" title="Daily Streak">${user.streak || 7}d Streak</span>` : ''}

        <a href="${window.location.pathname.includes('/pages/') ? 'dashboard.html' : 'pages/dashboard.html'}" style="display: flex; align-items: center; gap: 0.5rem; text-decoration: none;">
          <img src="${user.avatar}" alt="${user.name}" style="width: 36px; height: 36px; border-radius: 50%; border: 2px solid var(--accent-cyan); background: var(--bg-secondary);">
          <div style="display: none; @media(min-width: 768px){ display: block; }">
            <div style="font-size: 0.85rem; font-weight: 700; color: var(--text-primary); line-height: 1.1;">${user.name}</div>
            <span class="badge ${roleBadgeClass}" style="font-size: 0.65rem; padding: 0.1rem 0.4rem;">${user.role}</span>
          </div>
        </a>

        <button onclick="auth.logout()" class="btn-icon" title="Logout" style="width: 32px; height: 32px; font-size: 0.75rem; font-weight: 700;">Exit</button>
      </div>
    `;
  }
};

// Initialize navbar state on DOM load
document.addEventListener('DOMContentLoaded', () => {
  auth.updateNavbarUI();
});
