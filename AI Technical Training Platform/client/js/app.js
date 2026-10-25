// ==========================================================================
// Global Application Logic (Theme, Notifications, Toasts, Navbar)
// ==========================================================================

const app = {
  init() {
    this.initTheme();
    this.initNotifications();
    this.highlightActiveNav();
  },

  // 1. Dark / Light Theme Toggle
  initTheme() {
    const savedTheme = localStorage.getItem('app_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    this.updateThemeIcon(savedTheme);
  },

  toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('app_theme', next);
    this.updateThemeIcon(next);
    this.showToast(`Switched to ${next === 'dark' ? 'Dark' : 'Light'} mode`);
  },

  updateThemeIcon(theme) {
    const btn = document.getElementById('theme-toggle-btn');
    if (btn) {
      btn.innerHTML = theme === 'dark' ? 'Theme' : 'Theme';
      btn.setAttribute('title', `Current: ${theme} mode. Click to toggle.`);
    }
  },

  // 2. Notification Center
  initNotifications() {
    const notifBtn = document.getElementById('notif-bell-btn');
    const notifMenu = document.getElementById('notif-dropdown-menu');

    if (notifBtn && notifMenu) {
      notifBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        notifMenu.classList.toggle('active');
      });

      document.addEventListener('click', () => {
        notifMenu.classList.remove('active');
      });
    }
  },

  // 3. Modern Toast System
  showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.style.cssText = `
        position: fixed;
        bottom: 24px;
        right: 24px;
        z-index: 9999;
        display: flex;
        flex-direction: column;
        gap: 10px;
        pointer-events: none;
      `;
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'card';
    toast.style.cssText = `
      pointer-events: auto;
      padding: 0.85rem 1.25rem;
      border-radius: var(--radius-md);
      background: var(--bg-secondary);
      border: 1px solid var(--border-glow);
      box-shadow: 0 10px 25px rgba(0,0,0,0.4);
      display: flex;
      align-items: center;
      gap: 0.75rem;
      font-size: 0.9rem;
      font-weight: 600;
      animation: toastSlideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      max-width: 380px;
    `;

    const tag = type === 'success' ? '[Success]' : type === 'error' ? '[Alert]' : '[Notice]';
    const tagColor = type === 'success' ? 'var(--accent-green)' : type === 'error' ? 'var(--accent-rose)' : 'var(--accent-cyan)';
    toast.innerHTML = `<span style="font-size:0.8rem; font-weight:700; color:${tagColor};">${tag}</span> <span>${message}</span>`;

    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  },

  // 4. Highlight active page link in navigation
  highlightActiveNav() {
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll('.nav-link');
    links.forEach(link => {
      const href = link.getAttribute('href');
      if (href && currentPath.endsWith(href)) {
        link.classList.add('active');
      }
    });
  }
};

// Keyframe animation for toast
const styleSheet = document.createElement("style");
styleSheet.innerText = `
  @keyframes toastSlideIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }
`;
document.head.appendChild(styleSheet);

document.addEventListener('DOMContentLoaded', () => {
  app.init();
});
