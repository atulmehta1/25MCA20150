import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import TaskModal from './components/TaskModal';
import SubjectModal from './components/SubjectModal';

import Dashboard from './pages/Dashboard';
import Tasks from './pages/Tasks';
import FocusRoom from './pages/FocusRoom';
import Planner from './pages/Planner';
import Analytics from './pages/Analytics';
import Login from './pages/Login';
import Register from './pages/Register';

import { subjectAPI, analyticsAPI } from './services/api';

// Protected Route Guard
function ProtectedLayout({ children }) {
  const { isAuthenticated, loading } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [subjects, setSubjects] = useState([]);
  const [streak, setStreak] = useState(0);

  // Modals state
  const [isTaskModalOpen, setIsTaskModalOpen] = useState(false);
  const [taskToEdit, setTaskToEdit] = useState(null);
  const [taskDefaultDate, setTaskDefaultDate] = useState(null);
  const [isSubjectModalOpen, setIsSubjectModalOpen] = useState(false);

  const [refreshKey, setRefreshKey] = useState(0);

  const fetchGlobalContext = async () => {
    if (!isAuthenticated) return;
    try {
      const [subRes, dashRes] = await Promise.all([
        subjectAPI.getSubjects(),
        analyticsAPI.getDashboardSummary(),
      ]);
      if (subRes.data?.success) setSubjects(subRes.data.data);
      if (dashRes.data?.success) setStreak(dashRes.data.data.streakDays || 0);
    } catch (err) {
      console.warn('Error loading global context:', err.message);
    }
  };

  useEffect(() => {
    fetchGlobalContext();
  }, [isAuthenticated, refreshKey]);

  if (loading) {
    return (
      <div
        style={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: 'var(--bg-main)',
          color: '#818cf8',
          fontSize: '1.1rem',
          fontWeight: 600,
        }}
      >
        Loading FocusForge...
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  const handleOpenNewTask = (defaultDate = null) => {
    setTaskToEdit(null);
    setTaskDefaultDate(defaultDate);
    setIsTaskModalOpen(true);
  };

  const handleOpenEditTask = (task) => {
    setTaskToEdit(task);
    setTaskDefaultDate(null);
    setIsTaskModalOpen(true);
  };

  const handleTaskSaved = () => {
    setRefreshKey((prev) => prev + 1);
  };

  const handleSubjectsUpdated = () => {
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="app-container">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div className="main-content">
        <Navbar
          onOpenSidebar={() => setSidebarOpen(true)}
          streak={streak}
          onOpenTaskModal={() => handleOpenNewTask()}
        />

        {React.cloneElement(children, {
          key: refreshKey,
          subjects,
          onOpenTaskModal: handleOpenNewTask,
          onOpenTaskModalWithDate: handleOpenNewTask,
          onEditTask: handleOpenEditTask,
          onOpenSubjectModal: () => setIsSubjectModalOpen(true),
        })}
      </div>

      {/* Global Modals */}
      <TaskModal
        isOpen={isTaskModalOpen}
        onClose={() => setIsTaskModalOpen(false)}
        taskToEdit={taskToEdit}
        subjects={subjects}
        defaultDate={taskDefaultDate}
        onTaskSaved={handleTaskSaved}
      />

      <SubjectModal
        isOpen={isSubjectModalOpen}
        onClose={() => setIsSubjectModalOpen(false)}
        subjects={subjects}
        onSubjectsUpdated={handleSubjectsUpdated}
      />
    </div>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            <Route
              path="/"
              element={
                <ProtectedLayout>
                  <Dashboard />
                </ProtectedLayout>
              }
            />

            <Route
              path="/tasks"
              element={
                <ProtectedLayout>
                  <Tasks />
                </ProtectedLayout>
              }
            />

            <Route
              path="/focus"
              element={
                <ProtectedLayout>
                  <FocusRoom />
                </ProtectedLayout>
              }
            />

            <Route
              path="/planner"
              element={
                <ProtectedLayout>
                  <Planner />
                </ProtectedLayout>
              }
            />

            <Route
              path="/analytics"
              element={
                <ProtectedLayout>
                  <Analytics />
                </ProtectedLayout>
              }
            />

            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
}
