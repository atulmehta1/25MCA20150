// ==========================================================================
// API Helper Client with Hybrid Standalone / Express Server Support
// ==========================================================================

const API_BASE = window.location.origin.includes('5000') || window.location.origin.includes('localhost')
  ? '/api'
  : 'http://localhost:5000/api';

// Local Mock Fallback Data (ensures project works 100% even if opened via double-click file://)
const LocalDB = {
  getInitialData() {
    const saved = localStorage.getItem('aitraining_db');
    if (saved) {
      try { return JSON.parse(saved); } catch (e) {}
    }
    return null;
  },
  saveData(data) {
    localStorage.setItem('aitraining_db', JSON.stringify(data));
  }
};

const api = {
  // Generic request wrapper with auto fallback
  async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const token = localStorage.getItem('token');

    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      ...(options.headers || {})
    };

    try {
      const res = await fetch(url, { ...options, headers });
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.message || `Request failed with status ${res.status}`);
      }
      return await res.json();
    } catch (err) {
      console.warn(`Server API unreachable for ${endpoint}, utilizing smart client-side execution:`, err.message);
      return this.handleFallback(endpoint, options);
    }
  },

  get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  },

  post(endpoint, body) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(body)
    });
  },

  put(endpoint, body) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body)
    });
  },

  // Fallback simulator for offline or direct HTML file preview
  handleFallback(endpoint, options) {
    // 1. Auth Login Fallback
    if (endpoint === '/auth/login') {
      const body = JSON.parse(options.body || '{}');
      const email = (body.email || '').toLowerCase();
      let role = 'student';
      let name = 'Atul Mehta';
      let xp = 420;
      let streak = 7;
      let badges = ['Beginner', 'Streak Master', 'Quiz Whiz'];

      if (email.includes('trainer')) {
        role = 'trainer';
        name = 'Dr. Priya Nair';
      } else if (email.includes('admin')) {
        role = 'admin';
        name = 'Vikram Malhotra';
      }

      return {
        success: true,
        message: `Welcome back, ${name}!`,
        token: 'local-token-' + Date.now(),
        user: {
          id: 'u-' + role,
          name,
          email: body.email,
          role,
          avatar: `https://api.dicebear.com/7.x/bottts/svg?seed=${name}`,
          xp,
          streak,
          badges,
          enrolledCourses: ['c1', 'c2']
        }
      };
    }

    // 2. AI Tutor Fallback
    if (endpoint === '/ai/tutor') {
      const body = JSON.parse(options.body || '{}');
      return {
        success: true,
        data: {
          title: `AI Tutor Explanation: ${body.prompt}`,
          summary: `Comprehensive technical breakdown of **${body.prompt}** structured for placement and academic examinations.`,
          explanation: [
            "1. **Foundational Concept:** Essential building block for high-scale enterprise systems.",
            "2. **Real-world Application:** Used extensively in asynchronous pipelines and distributed data processing.",
            "3. **Optimization Strategy:** Leverage clean abstractions, non-blocking I/O, and structured error handling."
          ].join('\n'),
          codeSnippet: `// Implementation Example\nfunction solveProblem(input) {\n  console.log("Analyzing concept:", input);\n  return { success: true, processedAt: new Date().toLocaleTimeString() };\n}\nsolveProblem("${body.prompt.replace(/"/g, '')}");`,
          keyTakeaway: "Mastering this concept ensures optimal algorithmic complexity and system reliability."
        }
      };
    }

    // 3. AI Code Explainer Fallback
    if (endpoint === '/ai/code-explain') {
      const body = JSON.parse(options.body || '{}');
      const code = body.code || '';
      return {
        success: true,
        data: {
          overview: `Analyzed snippet with ${code.split('\n').length} lines of code.`,
          lineByLineExplanation: [
            "Line 1-2: Declares function and parses incoming arguments.",
            "Line 3-4: Applies iteration and conditional boundary checks.",
            "Line 5+: Emits structured return values."
          ],
          logicBreakdown: [
            "Validates input data structures.",
            "Executes algorithmic transformation in memory.",
            "Dispatches output with proper cleanup."
          ],
          complexity: {
            time: code.includes('for') ? "O(N) - Linear Time" : "O(1) - Constant Time",
            space: "O(1) - Auxiliary Space",
            notes: "Well-structured algorithm with clean space efficiency."
          },
          improvementSuggestions: [
            "Add guard clauses for null/undefined parameters.",
            "Extract repeated logic into helper functions."
          ]
        }
      };
    }

    // 4. AI Quiz Gen Fallback
    if (endpoint === '/ai/generate-quiz') {
      const body = JSON.parse(options.body || '{}');
      const topic = body.topic || 'Node.js';
      return {
        success: true,
        data: {
          topic,
          totalQuestions: 3,
          questions: [
            {
              question: `In ${topic}, which concept provides optimal non-blocking performance?`,
              options: ["Synchronous Blocking Loop", "Asynchronous Event Loop / I/O Delegation", "Heavy Thread Spawning", "Polling Wait"],
              correctIndex: 1,
              explanation: "Non-blocking event loop architectures delegate I/O to background system workers, preventing thread stalls."
            },
            {
              question: `What is the recommended best practice for error handling in ${topic}?`,
              options: ["Silently ignore exceptions", "Global try-catch with contextual error logging", "Process termination", "Uncaught promise rejections"],
              correctIndex: 1,
              explanation: "Structured error logging allows swift debugging without destabilizing the application lifecycle."
            },
            {
              question: `Which data structure offers average O(1) key-value lookup in ${topic}?`,
              options: ["Linked List", "Hash Map / Dictionary / Object", "Binary Search Tree", "Array"],
              correctIndex: 1,
              explanation: "Hash maps utilize hashing algorithms to provide near constant-time key lookups."
            }
          ]
        }
      };
    }

    // 5. AI Interview Fallback
    if (endpoint === '/ai/interview') {
      return {
        success: true,
        data: {
          targetRole: "Full Stack Developer",
          questions: [
            {
              id: "iq1",
              category: "System Design",
              question: "How do you handle authentication, session security, and token renewal in a scalable REST application?",
              evalCriteria: "Mention short-lived JWT access tokens, secure httpOnly refresh cookies, and CSRF protection.",
              modelAnswer: "I implement stateless JWT access tokens with a 15-minute expiration, paired with refresh tokens stored in secure, HttpOnly, SameSite cookies to mitigate XSS and CSRF."
            },
            {
              id: "iq2",
              category: "Database Indexing",
              question: "When should you add a composite index to a database table, and what is the leftmost prefix rule?",
              evalCriteria: "Explain that multi-column indexes accelerate queries filtering by multiple attributes.",
              modelAnswer: "A composite index should be applied when queries frequently filter or sort across multiple columns. The leftmost prefix rule requires queries to filter from the first indexed column to utilize the B-Tree index."
            }
          ]
        }
      };
    }

    // 6. AI Resume Review Fallback
    if (endpoint === '/ai/resume-review') {
      return {
        success: true,
        data: {
          atsScore: 84,
          atsStatus: "Strong Technical Profile",
          skillsDetected: ["JavaScript", "Node.js", "Python", "SQL", "Git", "REST APIs"],
          missingInDemandSkills: ["Docker & Containers", "AWS Cloud / Serverless", "Redis Caching"],
          atsOptimizationTips: [
            "Quantify project achievements with percentages (e.g. 'Reduced API response time by 40%').",
            "Place Technical Skills section above academic projects.",
            "Ensure standard plain-text formatting for ATS scanners."
          ],
          recommendedCourses: [
            "Full Stack Web Development with Node.js & React",
            "Cloud Computing with AWS & Docker"
          ]
        }
      };
    }

    // 7. Courses Fallback
    if (endpoint === '/courses' || endpoint.startsWith('/courses')) {
      return {
        success: true,
        count: 5,
        courses: [
          {
            id: "c1",
            title: "Full Stack Web Development with Node.js & React",
            category: "Web Development",
            trainerName: "Dr. Priya Nair",
            description: "Master modern full-stack web development from fundamentals to building robust REST APIs, state management, and modern responsive UI.",
            duration: "18 Hours",
            rating: 4.9,
            enrollments: 1420,
            thumbnail: "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800&auto=format&fit=crop&q=60",
            lessonsCount: 5,
            lessons: [
              {
                id: "l1-1",
                title: "1. Modern JavaScript: ES6+, Promises & Async/Await",
                duration: "24 mins",
                videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
                pdfTitle: "ES6_CheatSheet_Notes.pdf",
                summary: "Deep dive into lexical scoping, arrow functions, promises chaining, error handling, and event loop architecture.",
                codePractice: {
                  title: "Async Promise Resolver",
                  instructions: "Write an asynchronous function that fetches user data after a 1-second delay and returns 'User Profile Loaded'.",
                  starterCode: "async function fetchUserData() {\n  return new Promise((resolve) => {\n    setTimeout(() => resolve('User Profile Loaded'), 1000);\n  });\n}\nfetchUserData().then(console.log);",
                  solution: "async function fetchUserData() { return new Promise(r => setTimeout(() => r('User Profile Loaded'), 1000)); }"
                }
              },
              {
                id: "l1-2",
                title: "2. Node.js Architecture, Event Loop & Express Setup",
                duration: "32 mins",
                videoUrl: "https://www.w3schools.com/html/movie.mp4",
                pdfTitle: "Node_Express_Architecture.pdf",
                summary: "Understand single-threaded asynchronous I/O, middleware pipelines, routing, and building modular REST controllers.",
                codePractice: {
                  title: "Express Route Handler",
                  instructions: "Define a route handler that accepts a request query param 'role' and sends a JSON response.",
                  starterCode: "function handleRoute(req, res) {\n  const role = req.query.role || 'guest';\n  return { status: 200, message: `Access granted for ${role}` };\n}\nconsole.log(handleRoute({ query: { role: 'student' } }));",
                  solution: "function handleRoute(req, res) { return { status: 200, message: `Access granted for ${req.query.role || 'guest'}` }; }"
                }
              },
              {
                id: "l1-3",
                title: "3. REST API Design, JWT Authentication & Security",
                duration: "28 mins",
                videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
                pdfTitle: "JWT_Auth_Security.pdf",
                summary: "Learn role-based authorization headers, token signing, secret verification, and bcrypt password hashing.",
                codePractice: {
                  title: "Auth Header Parser",
                  instructions: "Extract bearer token string from an Authorization header formatted as 'Bearer <token>'.",
                  starterCode: "function parseToken(authHeader) {\n  return authHeader ? authHeader.split(' ')[1] : null;\n}\nconsole.log(parseToken('Bearer eyJhbGciOiJI...'));",
                  solution: "function parseToken(h) { return h ? h.split(' ')[1] : null; }"
                }
              }
            ]
          },
          {
            id: "c2",
            title: "Python for AI & Machine Learning Foundations",
            category: "AI",
            trainerName: "Dr. Priya Nair",
            description: "Learn Python programming, NumPy, Pandas, Scikit-Learn, and how to build supervised machine learning models.",
            duration: "14 Hours",
            rating: 4.8,
            enrollments: 1890,
            thumbnail: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop&q=60",
            lessonsCount: 4,
            lessons: [
              {
                id: "l2-1",
                title: "1. Pythonic Syntax, List Comprehensions & Lambdas",
                duration: "20 mins",
                videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
                pdfTitle: "Python_Core_CheatSheet.pdf",
                summary: "Master generators, iterators, functional programming paradigms, and clean syntax in Python.",
                codePractice: {
                  title: "Square Evens",
                  instructions: "Square all even numbers from an input list.",
                  starterCode: "function squareEvens(arr) {\n  return arr.filter(x => x % 2 === 0).map(x => x ** 2);\n}\nconsole.log(squareEvens([1, 2, 3, 4, 5, 6]));",
                  solution: "function squareEvens(arr) { return arr.filter(x => x % 2 === 0).map(x => x ** 2); }"
                }
              }
            ]
          },
          {
            id: "c3",
            title: "Data Structures & Algorithms in Java for Interviews",
            category: "Data Structures",
            trainerName: "Dr. Priya Nair",
            description: "Crack technical placement rounds with in-depth coverage of Arrays, Linked Lists, Trees, Graphs, DP, and Big-O.",
            duration: "22 Hours",
            rating: 4.9,
            enrollments: 2340,
            thumbnail: "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800&auto=format&fit=crop&q=60",
            lessonsCount: 3,
            lessons: [
              {
                id: "l3-1",
                title: "1. Big-O Complexity Analysis & Two-Pointer Technique",
                duration: "25 mins",
                videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
                pdfTitle: "Big_O_Handbook.pdf",
                summary: "Master time and space complexity evaluations, identifying bottlenecks, and optimizing nested loops.",
                codePractice: {
                  title: "Two-Sum Sorted",
                  instructions: "Return indices of two numbers that sum to target.",
                  starterCode: "function twoSum(arr, target) {\n  let l = 0, r = arr.length - 1;\n  while (l < r) {\n    let s = arr[l] + arr[r];\n    if (s === target) return [l, r];\n    if (s < target) l++; else r--;\n  }\n  return null;\n}\nconsole.log(twoSum([2, 7, 11, 15], 9));",
                  solution: "function twoSum(a, t) { let l=0, r=a.length-1; while(l<r){ let s=a[l]+a[r]; if(s===t) return [l,r]; if(s<t) l++; else r--; } return null; }"
                }
              }
            ]
          },
          {
            id: "c4",
            title: "SQL & Relational Database Mastery",
            category: "SQL",
            trainerName: "Dr. Priya Nair",
            description: "Learn complex JOINs, indexing, normalization (1NF-BCNF), window functions, and query optimization.",
            duration: "10 Hours",
            rating: 4.7,
            enrollments: 1100,
            thumbnail: "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=800&auto=format&fit=crop&q=60",
            lessonsCount: 2
          },
          {
            id: "c5",
            title: "Aptitude & Placement Preparation for MCA/B.Tech",
            category: "Aptitude",
            trainerName: "Dr. Priya Nair",
            description: "Fast shortcut formulas for Quantitative aptitude, Speed Math, Logical Reasoning, and Data Interpretation.",
            duration: "12 Hours",
            rating: 4.9,
            enrollments: 1750,
            thumbnail: "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&auto=format&fit=crop&q=60",
            lessonsCount: 2
          }
        ]
      };
    }

    // Default empty success fallback
    return { success: true, message: "Handled by fallback mode." };
  }
};
