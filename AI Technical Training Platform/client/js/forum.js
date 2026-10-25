// ==========================================================================
// Discussion Forum & Technical Community Q&A
// ==========================================================================

const forumModule = {
  posts: [],

  async initForum() {
    await this.fetchPosts();
    this.renderForum();
  },

  async fetchPosts() {
    try {
      const res = await api.get('/forum');
      if (res && res.posts) this.posts = res.posts;
    } catch (e) {
      console.warn("Using offline forum posts fallback:", e);
    }

    if (!this.posts || this.posts.length === 0) {
      this.posts = [
        {
          id: "f1",
          title: "How does the Node.js event loop handle asynchronous file I/O versus network requests?",
          category: "Web Development",
          author: "Atul Mehta",
          authorRole: "Student",
          date: "2 hours ago",
          upvotes: 12,
          replies: [
            {
              id: "r1",
              author: "Dr. Priya Nair",
              authorRole: "Trainer",
              isTrainerVerified: true,
              content: "Great question! Network I/O is delegated directly to OS asynchronous system calls (like epoll on Linux, kqueue on macOS, IOCP on Windows). In contrast, standard file system I/O does not have unified async OS interfaces across platforms, so Node.js offloads file system operations to the libuv threadpool (default 4 threads).",
              upvotes: 19
            }
          ]
        },
        {
          id: "f2",
          title: "What is the difference between Array and LinkedList memory allocation in Java?",
          category: "Data Structures",
          author: "Karthik Verma",
          authorRole: "Student",
          date: "1 day ago",
          upvotes: 8,
          replies: [
            {
              id: "r2",
              author: "Dr. Priya Nair",
              authorRole: "Trainer",
              isTrainerVerified: true,
              content: "Arrays allocate contiguous blocks of memory, which provides O(1) random access and excellent CPU cache locality. LinkedList allocates non-contiguous nodes on the heap with pointers (references), which incurs extra memory overhead per node and O(N) access time.",
              upvotes: 14
            }
          ]
        }
      ];
    }
  },

  renderForum() {
    const container = document.getElementById('forum-posts-container');
    if (!container) return;

    container.innerHTML = this.posts.map(p => `
      <div class="card" style="margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
          <div>
            <span class="badge badge-cyan" style="margin-bottom: 0.4rem;">${p.category}</span>
            <h3 style="font-size: 1.2rem; font-weight: 700; margin-top: 0.25rem;">${p.title}</h3>
            <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem;">
              Asked by <strong>${p.author}</strong> (${p.authorRole}) - <span>${p.date}</span>
            </div>
          </div>
          <button class="btn btn-secondary btn-sm" onclick="forumModule.upvotePost('${p.id}')">
            Upvotes: ${p.upvotes || 0}
          </button>
        </div>

        <!-- Replies List -->
        <div style="margin-top: 1.25rem; border-top: 1px solid var(--border-color); padding-top: 1rem;">
          <h4 style="font-size: 0.95rem; color: var(--text-secondary); margin-bottom: 0.75rem;">
            Replies (${p.replies ? p.replies.length : 0})
          </h4>
          
          ${(p.replies || []).map(r => `
            <div style="background: var(--bg-primary); border: 1px solid ${r.isTrainerVerified ? 'var(--accent-purple)' : 'var(--border-color)'}; border-radius: var(--radius-md); padding: 1rem; margin-bottom: 0.75rem;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                  <span style="font-weight: 700; font-size: 0.9rem;">${r.author}</span>
                  ${r.isTrainerVerified ? `<span class="badge badge-purple" style="font-size: 0.7rem;">Trainer Verified</span>` : ''}
                </div>
                <span style="font-size: 0.8rem; color: var(--text-muted);">Votes: ${r.upvotes || 0}</span>
              </div>
              <p style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.5;">${r.content}</p>
            </div>
          `).join('')}

          <!-- Quick Reply Box -->
          <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
            <input type="text" id="reply-input-${p.id}" class="form-control" placeholder="Write a constructive technical reply..." style="font-size: 0.85rem;">
            <button class="btn btn-primary btn-sm" onclick="forumModule.submitReply('${p.id}')">Reply</button>
          </div>
        </div>
      </div>
    `).join('');
  },

  async askQuestion() {
    const title = document.getElementById('new-question-title')?.value.trim();
    const category = document.getElementById('new-question-cat')?.value || 'General';
    const user = auth.getUser();

    if (!title) {
      app.showToast('Please type a question title.', 'error');
      return;
    }

    try {
      await api.post('/forum', {
        title,
        category,
        author: user ? user.name : 'Student',
        authorRole: user ? user.role : 'Student'
      });
    } catch (e) {}

    this.posts.unshift({
      id: 'f' + Date.now(),
      title,
      category,
      author: user ? user.name : 'Student',
      authorRole: user ? user.role : 'Student',
      date: 'Just now',
      upvotes: 1,
      replies: []
    });

    document.getElementById('new-question-title').value = '';
    app.showToast('Question posted to community forum! +5 XP', 'success');
    this.renderForum();
  },

  async submitReply(postId) {
    const input = document.getElementById(`reply-input-${postId}`);
    const content = input ? input.value.trim() : '';
    const user = auth.getUser();

    if (!content) return;

    const post = this.posts.find(p => p.id === postId);
    if (post) {
      const isTrainer = user && user.role === 'trainer';
      post.replies = post.replies || [];
      post.replies.push({
        id: 'r' + Date.now(),
        author: user ? user.name : 'Learner',
        authorRole: user ? user.role : 'Student',
        isTrainerVerified: isTrainer,
        content,
        upvotes: 1
      });
      input.value = '';
      app.showToast(isTrainer ? 'Trainer Verified answer submitted!' : 'Reply posted! +5 XP', 'success');
      this.renderForum();
    }
  },

  upvotePost(postId) {
    const post = this.posts.find(p => p.id === postId);
    if (post) {
      post.upvotes = (post.upvotes || 0) + 1;
      this.renderForum();
      app.showToast('Upvoted successfully', 'info');
    }
  }
};
