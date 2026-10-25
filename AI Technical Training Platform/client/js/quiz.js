// ==========================================================================
// Quiz Assessment Runner, Timer, Auto-Grading & Certificate Trigger
// ==========================================================================

const quizModule = {
  currentQuiz: null,
  userAnswers: {},
  timerSeconds: 600, // 10 minutes
  timerInterval: null,

  async initQuiz() {
    const params = new URLSearchParams(window.location.search);
    const courseId = params.get('courseId') || 'c1';

    try {
      const res = await api.get(`/quizzes/course/${courseId}`);
      if (res && res.quiz) {
        this.currentQuiz = res.quiz;
      }
    } catch (e) {
      console.warn("Quiz API unreachable, using default quiz fallback:", e);
    }

    if (!this.currentQuiz) {
      // Local fallback quiz
      this.currentQuiz = {
        id: "q1",
        courseId: "c1",
        title: "Full Stack & JavaScript Architecture Assessment",
        durationMinutes: 10,
        passingScore: 70,
        questions: [
          {
            id: "q1-1",
            question: "What will be the output of `console.log(typeof NaN)` in JavaScript?",
            options: ["'undefined'", "'number'", "'object'", "'NaN'"],
            correctIndex: 1,
            explanation: "In JavaScript, NaN is a numeric value representing 'Not-a-Number', so `typeof NaN` returns 'number'."
          },
          {
            id: "q1-2",
            question: "Which HTTP method is idempotent and used to replace an entire resource in REST?",
            options: ["POST", "PATCH", "PUT", "DELETE"],
            correctIndex: 2,
            explanation: "PUT is idempotent and replaces the target resource entirely. PATCH is for partial updates."
          },
          {
            id: "q1-3",
            question: "What is the purpose of the `next()` function in Express.js middleware?",
            options: [
              "Terminate the HTTP request immediately",
              "Pass control to the next middleware function in stack",
              "Restart the server process",
              "Send an HTTP 200 OK response"
            ],
            correctIndex: 1,
            explanation: "The `next()` callback tells Express to pass execution to the next middleware function."
          },
          {
            id: "q1-4",
            question: "Which part of a JWT (JSON Web Token) contains the user payload and role information?",
            options: ["Header", "Payload", "Signature", "Footer"],
            correctIndex: 1,
            explanation: "The payload (middle segment) contains the JSON claims such as user ID, role, and expiration."
          },
          {
            id: "q1-5",
            question: "In the Node.js event loop, which phase handles expired `setTimeout` callbacks?",
            options: ["Poll phase", "Check phase", "Timers phase", "Close callbacks phase"],
            correctIndex: 2,
            explanation: "The Timers phase executes callbacks scheduled by `setTimeout()` and `setInterval()`."
          }
        ]
      };
    }

    this.renderQuizUI();
    this.startTimer();
  },

  renderQuizUI() {
    const q = this.currentQuiz;
    document.getElementById('quiz-title').innerText = q.title;
    document.getElementById('quiz-total-badge').innerText = `${q.questions.length} Questions`;
    document.getElementById('quiz-pass-badge').innerText = `Passing Score: ${q.passingScore}%`;

    const container = document.getElementById('quiz-questions-list');
    container.innerHTML = q.questions.map((item, idx) => `
      <div class="question-block" id="q-block-${item.id}">
        <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 1rem;">
          <span style="color: var(--accent-cyan);">${idx + 1}.</span> ${item.question}
        </div>
        <div>
          ${item.options.map((opt, optIdx) => `
            <label class="quiz-choice" id="label-${item.id}-${optIdx}">
              <input type="radio" name="answer_${item.id}" value="${optIdx}" onchange="quizModule.selectAnswer('${item.id}', ${optIdx})">
              <span>${opt}</span>
            </label>
          `).join('')}
        </div>
        <div id="expl-${item.id}" style="display: none; margin-top: 1rem; padding: 0.85rem; border-radius: var(--radius-sm); font-size: 0.875rem;"></div>
      </div>
    `).join('');
  },

  selectAnswer(questionId, optionIdx) {
    this.userAnswers[questionId] = optionIdx;
  },

  startTimer() {
    this.timerSeconds = (this.currentQuiz.durationMinutes || 10) * 60;
    const timerEl = document.getElementById('quiz-countdown-timer');

    if (this.timerInterval) clearInterval(this.timerInterval);

    this.timerInterval = setInterval(() => {
      this.timerSeconds--;
      if (this.timerSeconds <= 0) {
        clearInterval(this.timerInterval);
        app.showToast('Time is up! Auto-submitting quiz...', 'error');
        this.submitQuiz();
        return;
      }

      const mins = Math.floor(this.timerSeconds / 60);
      const secs = this.timerSeconds % 60;
      if (timerEl) {
        timerEl.innerText = `Time Remaining: ${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
      }
    }, 1000);
  },

  async submitQuiz() {
    if (this.timerInterval) clearInterval(this.timerInterval);

    const user = auth.getUser();
    let res = null;

    try {
      res = await api.post('/quizzes/submit', {
        quizId: this.currentQuiz.id,
        userId: user ? user.id : 'u1',
        answers: this.userAnswers
      });
    } catch (e) {
      console.warn("Using offline evaluation fallback:", e);
    }

    // Local evaluation if offline
    if (!res || !res.review) {
      let correct = 0;
      const review = this.currentQuiz.questions.map(q => {
        const selected = this.userAnswers[q.id];
        const isCorrect = selected === q.correctIndex;
        if (isCorrect) correct++;
        return {
          questionId: q.id,
          question: q.question,
          options: q.options,
          selectedIndex: selected,
          correctIndex: q.correctIndex,
          isCorrect,
          explanation: q.explanation
        };
      });

      const score = Math.round((correct / this.currentQuiz.questions.length) * 100);
      const passed = score >= (this.currentQuiz.passingScore || 70);

      res = {
        success: true,
        score,
        correctCount: correct,
        totalQuestions: this.currentQuiz.questions.length,
        passed,
        xpAwarded: passed ? 20 : 0,
        certificate: passed ? {
          id: 'CERT-2024-' + Math.floor(1000 + Math.random() * 9000),
          studentName: user ? user.name : 'Atul Mehta',
          courseTitle: 'Full Stack Web Development with Node.js & React',
          score,
          issueDate: new Date().toISOString().split('T')[0]
        } : null,
        review
      };
    }

    this.displayQuizResults(res);
  },

  displayQuizResults(data) {
    // Reveal explanations on all questions
    data.review.forEach(item => {
      const explEl = document.getElementById(`expl-${item.questionId}`);
      if (explEl) {
        explEl.style.display = 'block';
        if (item.isCorrect) {
          explEl.style.background = 'rgba(52, 211, 153, 0.15)';
          explEl.style.borderLeft = '4px solid var(--accent-green)';
          explEl.innerHTML = `<strong>Correct:</strong> ${item.explanation}`;
        } else {
          explEl.style.background = 'rgba(251, 113, 133, 0.15)';
          explEl.style.borderLeft = '4px solid var(--accent-rose)';
          explEl.innerHTML = `<strong>Incorrect.</strong> Correct answer: <em>"${item.options[item.correctIndex]}"</em>.<br>${item.explanation}`;
        }
      }

      // Highlight selected labels
      if (item.correctIndex !== undefined) {
        const correctLabel = document.getElementById(`label-${item.questionId}-${item.correctIndex}`);
        if (correctLabel) correctLabel.style.borderColor = 'var(--accent-green)';
      }
    });

    // Update user stats
    const user = auth.getUser();
    if (user && data.passed) {
      user.xp = (user.xp || 420) + (data.xpAwarded || 20);
      auth.setUser(user);
    }

    // Show Result Modal
    const modal = document.getElementById('quiz-result-modal');
    modal.classList.add('active');

    document.getElementById('modal-score-percent').innerText = `${data.score}%`;
    document.getElementById('modal-correct-count').innerText = `${data.correctCount} / ${data.totalQuestions} Questions Correct`;

    const statusBadge = document.getElementById('modal-pass-status');
    const certActionArea = document.getElementById('modal-cert-action');

    if (data.passed) {
      statusBadge.className = 'badge badge-green';
      statusBadge.innerText = 'PASSED Assessment';
      
      certActionArea.innerHTML = `
        <div style="background: rgba(52, 211, 153, 0.1); border: 1px solid var(--accent-green); border-radius: var(--radius-md); padding: 1.25rem; margin-top: 1rem; text-align: center;">
          <h4 style="color: var(--accent-green); margin-bottom: 0.25rem;">Congratulations! You Earned a Certificate</h4>
          <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1rem;">
            Certificate ID: <strong>${data.certificate ? data.certificate.id : 'CERT-2024-8841'}</strong>
          </p>
          <a href="certificate.html?certId=${data.certificate ? data.certificate.id : 'CERT-2024-8841'}&name=${encodeURIComponent(user ? user.name : 'Atul Mehta')}" class="btn btn-primary btn-sm">
            View & Download Certificate
          </a>
        </div>
      `;
      app.showToast('Quiz Passed! +20 XP Awarded', 'success');
    } else {
      statusBadge.className = 'badge badge-amber';
      statusBadge.innerText = 'NEEDS RETAKE (Passing: 70%)';
      certActionArea.innerHTML = `
        <div style="text-align: center; margin-top: 1rem;">
          <p style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.75rem;">
            Review the question explanations below and retake the quiz to qualify for your certificate.
          </p>
          <button class="btn btn-secondary btn-sm" onclick="window.location.reload()">Retake Quiz</button>
        </div>
      `;
    }
  }
};
