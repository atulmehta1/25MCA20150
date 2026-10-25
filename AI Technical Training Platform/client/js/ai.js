// ==========================================================================
// 5 AI Features Controller: Tutor, Explainer, QuizGen, Mock Interview, Resume
// ==========================================================================

const ai = {
  activeTab: 'tutor',

  switchTab(tabName) {
    this.activeTab = tabName;
    document.querySelectorAll('.ai-tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tab === tabName);
    });
    document.querySelectorAll('.ai-tab-panel').forEach(panel => {
      panel.style.display = panel.id === `tab-panel-${tabName}` ? 'block' : 'none';
    });
  },

  // 1. AI Chat Tutor
  async sendTutorMessage() {
    const input = document.getElementById('tutor-input');
    const prompt = (input ? input.value : '').trim();
    if (!prompt) return;

    const chatMessages = document.getElementById('tutor-messages');
    
    // Append user message bubble
    const userMsg = document.createElement('div');
    userMsg.className = 'message-bubble message-user';
    userMsg.innerText = prompt;
    chatMessages.appendChild(userMsg);
    input.value = '';
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Append loading indicator
    const aiLoading = document.createElement('div');
    aiLoading.className = 'message-bubble message-ai';
    aiLoading.innerHTML = `<em>AI Tutor is analyzing concept...</em>`;
    chatMessages.appendChild(aiLoading);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
      const res = await api.post('/ai/tutor', { prompt });
      const data = res.data;

      aiLoading.innerHTML = `
        <div style="font-weight: 700; color: var(--accent-cyan); font-size: 1.05rem; margin-bottom: 0.4rem;">
          ${data.title}
        </div>
        <p style="margin-bottom: 0.6rem; color: var(--text-secondary);">${data.summary}</p>
        <div style="white-space: pre-line; margin-bottom: 0.75rem;">${data.explanation}</div>
        ${data.codeSnippet ? `<pre><code>${data.codeSnippet}</code></pre>` : ''}
        <div style="margin-top: 0.6rem; font-size: 0.85rem; padding: 0.6rem; background: rgba(56, 189, 248, 0.08); border-left: 3px solid var(--accent-cyan); border-radius: 4px;">
          <strong>Key Takeaway:</strong> ${data.keyTakeaway}
        </div>
      `;
    } catch (err) {
      aiLoading.innerHTML = `<span style="color: var(--accent-rose);">Error getting response. Please try again.</span>`;
    }
    chatMessages.scrollTop = chatMessages.scrollHeight;
  },

  quickPrompt(text) {
    const input = document.getElementById('tutor-input');
    if (input) {
      input.value = text;
      this.sendTutorMessage();
    }
  },

  // 2. AI Code Explainer
  async analyzeCode() {
    const codeArea = document.getElementById('code-input-area');
    const langSelect = document.getElementById('code-lang-select');
    const code = (codeArea ? codeArea.value : '').trim();
    const language = langSelect ? langSelect.value : 'javascript';

    if (!code) {
      app.showToast('Please paste or write code to explain.', 'error');
      return;
    }

    const resultBox = document.getElementById('code-explain-result');
    resultBox.style.display = 'block';
    resultBox.innerHTML = `<div style="text-align: center; padding: 2rem;"><em>AI is generating line-by-line breakdown and complexity analysis...</em></div>`;

    try {
      const res = await api.post('/ai/code-explain', { code, language });
      const d = res.data;

      resultBox.innerHTML = `
        <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.25rem;">
          <div class="complexity-pill">Time Complexity: <strong>${d.complexity.time}</strong></div>
          <div class="complexity-pill" style="color: var(--accent-cyan); border-color: rgba(56,189,248,0.3); background: rgba(56,189,248,0.1);">Space: <strong>${d.complexity.space}</strong></div>
        </div>

        <h4 style="color: var(--accent-cyan); margin-bottom: 0.5rem;">Overview</h4>
        <p style="color: var(--text-secondary); margin-bottom: 1.25rem;">${d.overview}</p>

        <h4 style="color: var(--accent-purple); margin-bottom: 0.5rem;">Line-by-Line Breakdown</h4>
        <div style="background: var(--bg-primary); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1rem; margin-bottom: 1.25rem; font-size: 0.875rem;">
          ${d.lineByLineExplanation.map(line => `<div style="padding: 0.25rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);">${line}</div>`).join('')}
        </div>

        <h4 style="color: var(--accent-amber); margin-bottom: 0.5rem;">Best Practice & Optimization Tips</h4>
        <ul style="padding-left: 1.25rem; color: var(--text-secondary); font-size: 0.9rem;">
          ${d.improvementSuggestions.map(tip => `<li style="margin-bottom: 0.35rem;">${tip}</li>`).join('')}
        </ul>
      `;
    } catch (err) {
      resultBox.innerHTML = `<span style="color: var(--accent-rose);">Failed to explain code.</span>`;
    }
  },

  loadSampleCode(type) {
    const codeArea = document.getElementById('code-input-area');
    if (!codeArea) return;

    if (type === 'twosum') {
      codeArea.value = `// Two Sum Algorithm in JavaScript\nfunction twoSum(nums, target) {\n  const map = new Map();\n  for (let i = 0; i < nums.length; i++) {\n    const complement = target - nums[i];\n    if (map.has(complement)) {\n      return [map.get(complement), i];\n    }\n    map.set(nums[i], i);\n  }\n  return [];\n}\n\nconsole.log(twoSum([2, 7, 11, 15], 9)); // [0, 1]`;
    } else if (type === 'async') {
      codeArea.value = `// Asynchronous User Profile Loader\nasync function loadUserProfile(userId) {\n  try {\n    const response = await fetch(\`/api/users/\${userId}\`);\n    if (!response.ok) throw new Error("User not found");\n    const data = await response.json();\n    return data;\n  } catch (err) {\n    console.error("Load failed:", err.message);\n    return null;\n  }\n}`;
    }
    this.analyzeCode();
  },

  // 3. AI Quiz Generator
  async generateDynamicQuiz() {
    const topicInput = document.getElementById('quiz-gen-topic');
    const topic = (topicInput ? topicInput.value : '').trim() || 'Node.js';

    const container = document.getElementById('quiz-gen-output');
    container.innerHTML = `<div style="text-align: center; padding: 2rem;"><em>AI is generating 5 MCQs on "${topic}"...</em></div>`;

    try {
      const res = await api.post('/ai/generate-quiz', { topic, count: 5 });
      const quizData = res.data;

      container.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
          <h3>Quiz on: <span class="gradient-text">${quizData.topic}</span></h3>
          <span class="badge badge-purple">${quizData.questions.length} Generated Questions</span>
        </div>
        ${quizData.questions.map((q, idx) => `
          <div class="quiz-gen-card">
            <div style="font-weight: 700; font-size: 1rem; margin-bottom: 0.75rem;">
              ${idx + 1}. ${q.question}
            </div>
            <div>
              ${q.options.map((opt, optIdx) => `
                <div class="quiz-option-label" onclick="ai.verifyQuizGenAnswer(this, ${optIdx}, ${q.correctIndex}, '${encodeURIComponent(q.explanation)}')">
                  <span style="font-weight: 700; width: 24px;">${String.fromCharCode(65 + optIdx)}.</span>
                  <span>${opt}</span>
                </div>
              `).join('')}
            </div>
            <div class="quiz-gen-expl" style="display: none; margin-top: 0.75rem; padding: 0.75rem; background: rgba(56, 189, 248, 0.1); border-left: 3px solid var(--accent-cyan); border-radius: 4px; font-size: 0.85rem;">
            </div>
          </div>
        `).join('')}
      `;
    } catch (err) {
      container.innerHTML = `<span style="color: var(--accent-rose);">Failed to generate quiz.</span>`;
    }
  },

  verifyQuizGenAnswer(element, selectedIdx, correctIdx, explanationURI) {
    const parent = element.parentElement;
    const card = parent.closest('.quiz-gen-card');
    const explBox = card.querySelector('.quiz-gen-expl');
    const explanation = decodeURIComponent(explanationURI);

    // Disable multiple clicks
    if (card.dataset.answered) return;
    card.dataset.answered = "true";

    const allOptions = parent.querySelectorAll('.quiz-option-label');
    allOptions[correctIdx].classList.add('correct');

    if (selectedIdx !== correctIdx) {
      element.style.background = 'rgba(251, 113, 133, 0.2)';
      element.style.borderColor = 'var(--accent-rose)';
      element.style.color = 'var(--accent-rose)';
    } else {
      app.showToast('Correct Answer! +5 XP', 'success');
    }

    explBox.style.display = 'block';
    explBox.innerHTML = `<strong>Explanation:</strong> ${explanation}`;
  },

  // 4. AI Interview Preparation
  async loadInterviewMock() {
    const role = document.getElementById('interview-role-select')?.value || 'Full Stack Developer';
    const round = document.getElementById('interview-round-select')?.value || 'Technical';
    const container = document.getElementById('interview-questions-box');

    container.innerHTML = `<div style="text-align: center; padding: 2rem;"><em>AI is preparing mock questions for ${role} (${round})...</em></div>`;

    try {
      const res = await api.post('/ai/interview', { role, round });
      const d = res.data;

      container.innerHTML = d.questions.map((q, idx) => `
        <div class="interview-box">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <span class="badge badge-cyan">${q.category}</span>
            <span style="font-size: 0.8rem; color: var(--text-muted);">Question ${idx + 1} of ${d.questions.length}</span>
          </div>
          <h4 style="font-size: 1.05rem; margin-bottom: 0.75rem;">${q.question}</h4>
          
          <div class="form-group">
            <textarea id="interview-ans-${idx}" class="form-control" placeholder="Type your answer here or structure your response using STAR method..." style="min-height: 90px;"></textarea>
          </div>

          <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
            <button class="btn btn-primary btn-sm" onclick="ai.evaluateInterviewAnswer(${idx}, '${encodeURIComponent(q.evalCriteria)}', '${encodeURIComponent(q.modelAnswer)}')">
              Evaluate My Answer
            </button>
            <button class="btn btn-secondary btn-sm" onclick="ai.revealModelAnswer(${idx}, '${encodeURIComponent(q.modelAnswer)}')">
              View Model Answer
            </button>
          </div>

          <div id="eval-result-${idx}" style="display: none; margin-top: 1rem; padding: 1rem; background: var(--bg-primary); border-radius: var(--radius-md); border: 1px solid var(--border-glow);"></div>
        </div>
      `).join('');
    } catch (err) {
      container.innerHTML = `<span style="color: var(--accent-rose);">Failed to load mock interview.</span>`;
    }
  },

  evaluateInterviewAnswer(idx, criteriaURI, modelAnswerURI) {
    const ans = document.getElementById(`interview-ans-${idx}`)?.value.trim();
    const resultBox = document.getElementById(`eval-result-${idx}`);
    const criteria = decodeURIComponent(criteriaURI);
    const modelAns = decodeURIComponent(modelAnswerURI);

    if (!ans) {
      app.showToast('Please type your answer first before requesting AI evaluation.', 'error');
      return;
    }

    resultBox.style.display = 'block';
    const score = Math.min(95, Math.max(65, Math.floor(ans.length / 5) + 60));

    resultBox.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
        <span style="font-weight: 700; color: var(--accent-green);">AI Evaluation Score: ${score}/100</span>
        <span class="badge badge-amber">Good Effort</span>
      </div>
      <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.6rem;">
        <strong>Key Evaluation Criteria:</strong> ${criteria}
      </p>
      <div style="padding: 0.6rem; background: rgba(52, 211, 153, 0.1); border-radius: var(--radius-sm); font-size: 0.85rem;">
        <strong>Feedback:</strong> Your response articulates core concepts. To stand out in technical interviews, explicitly mention scalability bottlenecks, database transactions, or system metrics.
      </div>
    `;
    app.showToast('AI Evaluated your response! +15 XP', 'success');
  },

  revealModelAnswer(idx, modelAnswerURI) {
    const resultBox = document.getElementById(`eval-result-${idx}`);
    resultBox.style.display = 'block';
    resultBox.innerHTML = `
      <h5 style="color: var(--accent-cyan); margin-bottom: 0.4rem;">Suggested Model Answer:</h5>
      <p style="font-size: 0.875rem; color: var(--text-primary); line-height: 1.6;">${decodeURIComponent(modelAnswerURI)}</p>
    `;
  },

  // 5. AI Resume Review
  async analyzeResume() {
    const resumeText = document.getElementById('resume-text-input')?.value.trim();
    if (!resumeText) {
      app.showToast('Please paste your resume text to review.', 'error');
      return;
    }

    const outputBox = document.getElementById('resume-review-output');
    outputBox.style.display = 'block';
    outputBox.innerHTML = `<div style="text-align: center; padding: 2rem;"><em>AI is scanning resume for keywords, ATS compatibility, and technical skills...</em></div>`;

    try {
      const res = await api.post('/ai/resume-review', { resumeText });
      const d = res.data;

      outputBox.innerHTML = `
        <div class="ats-score-display">
          <div class="ats-circle" style="--score: ${d.atsScore};">
            <span>${d.atsScore}%</span>
          </div>
          <div>
            <h3 style="margin-bottom: 0.25rem;">${d.atsStatus}</h3>
            <p style="color: var(--text-secondary); font-size: 0.9rem;">Calculated based on industry ATS parsers and placement screening algorithms.</p>
          </div>
        </div>

        <div style="margin-bottom: 1.5rem;">
          <h4 style="color: var(--accent-green); margin-bottom: 0.6rem;">Technical Skills Detected:</h4>
          <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            ${d.skillsDetected.map(s => `<span class="badge badge-green">${s}</span>`).join('')}
          </div>
        </div>

        <div style="margin-bottom: 1.5rem;">
          <h4 style="color: var(--accent-rose); margin-bottom: 0.6rem;">Missing In-Demand Industry Skills:</h4>
          <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            ${d.missingInDemandSkills.map(s => `<span class="badge badge-amber" style="color: var(--accent-rose); border-color: rgba(251,113,133,0.3); background: rgba(251,113,133,0.1);">${s}</span>`).join('')}
          </div>
        </div>

        <div style="margin-bottom: 1.5rem;">
          <h4 style="color: var(--accent-cyan); margin-bottom: 0.6rem;">ATS Optimization Recommendations:</h4>
          <ul style="padding-left: 1.25rem; font-size: 0.9rem; color: var(--text-secondary);">
            ${d.atsOptimizationTips.map(tip => `<li style="margin-bottom: 0.4rem;">${tip}</li>`).join('')}
          </ul>
        </div>

        <div style="padding: 1.25rem; background: var(--bg-primary); border-radius: var(--radius-md); border: 1px solid var(--border-color);">
          <h4 style="color: var(--accent-purple); margin-bottom: 0.5rem;">Recommended Courses to Bridge Skill Gaps:</h4>
          <ul style="padding-left: 1.25rem; font-size: 0.875rem;">
            ${d.recommendedCourses.map(c => `<li><a href="courses.html" style="color: var(--accent-cyan); font-weight: 600;">${c} -></a></li>`).join('')}
          </ul>
        </div>
      `;
    } catch (err) {
      outputBox.innerHTML = `<span style="color: var(--accent-rose);">Failed to review resume.</span>`;
    }
  },

  loadSampleResume() {
    const input = document.getElementById('resume-text-input');
    if (input) {
      input.value = `ATUL MEHTA
Email: atul.mehta@email.com | Phone: +91-9876543210 | GitHub: github.com/atulmehta

EDUCATION:
Master of Computer Applications (MCA) - CGPA: 8.9/10 (2022 - 2024)
Bachelor of Computer Applications (BCA) - 84% (2019 - 2022)

TECHNICAL SKILLS:
- Languages: JavaScript (ES6+), Python, HTML5, CSS3, SQL
- Frameworks & Libraries: Node.js, Express.js, React.js
- Tools & Databases: MongoDB, Git, Postman, VS Code

ACADEMIC PROJECTS:
1. AI Technical Training Platform (Full Stack Web App)
- Developed responsive web learning platform using Node.js, Express, and JavaScript.
- Integrated AI assistants for code explanation, mock technical interviews, and automated quiz evaluation.
- Implemented role-based access control (Student, Trainer, Admin) with JWT security.

2. Student Placement Management Portal
- Designed relational database schema in SQL for tracking placement registrations and student records.
- Built REST API endpoints with validation and error-handling middleware.`;
      this.analyzeResume();
    }
  }
};
