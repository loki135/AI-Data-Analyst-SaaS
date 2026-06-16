import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Login from '../components/Auth/Login';
import Register from '../components/Auth/Register';
import FileUpload from '../components/Upload/FileUpload';

const FEATURES = [
  { icon: '📊', title: 'Instant Charts', desc: 'Bar, line, and pie charts generated automatically from your data' },
  { icon: '✨', title: 'AI Insights', desc: 'Gemini AI writes a plain-English summary of your dataset' },
  { icon: '💬', title: 'Ask Questions', desc: 'Chat with your data — get answers in natural language' },
  { icon: '📜', title: 'Full History', desc: 'All your past uploads saved and accessible anytime' },
];

export default function HomePage() {
  const { token, user, logout } = useAuth();
  const [authMode, setAuthMode] = useState('login');

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Navbar */}
      <nav className="border-b border-slate-800 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-2xl">📊</span>
          <span className="font-bold text-white text-lg">DataLens AI</span>
        </div>
        {token && (
          <div className="flex items-center gap-4">
            <span className="text-slate-400 text-sm hidden sm:block">Hi, {user?.name || 'there'}</span>
            <Link to="/history" className="btn-secondary text-sm">History</Link>
            <button onClick={logout} className="text-slate-500 hover:text-slate-300 text-sm transition-colors">
              Sign out
            </button>
          </div>
        )}
      </nav>

      {token ? (
        /* Logged-in: show upload */
        <div className="max-w-4xl mx-auto px-6 py-16">
          <div className="text-center mb-10">
            <h1 className="text-4xl font-bold text-white mb-3">
              Drop your CSV, get instant insights
            </h1>
            <p className="text-slate-400">AI-powered analysis in seconds — charts, stats, and natural language Q&A</p>
          </div>
          <FileUpload />
        </div>
      ) : (
        /* Logged-out: features + auth */
        <div className="max-w-6xl mx-auto px-6 py-16 grid md:grid-cols-2 gap-16 items-center">
          {/* Left: features */}
          <div>
            <h1 className="text-5xl font-bold text-white leading-tight mb-4">
              Your CSV data,<br />
              <span className="text-brand-400">explained by AI</span>
            </h1>
            <p className="text-slate-400 text-lg mb-10">
              Upload any CSV and get charts, statistics, AI summaries, and a natural language Q&A — free, instantly.
            </p>
            <div className="space-y-5">
              {FEATURES.map((f) => (
                <div key={f.title} className="flex items-start gap-4">
                  <div className="text-2xl mt-0.5">{f.icon}</div>
                  <div>
                    <div className="font-semibold text-white">{f.title}</div>
                    <div className="text-slate-400 text-sm">{f.desc}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Right: auth form */}
          <div className="card max-w-md w-full mx-auto">
            {authMode === 'login' ? (
              <Login onSwitch={() => setAuthMode('register')} />
            ) : (
              <Register onSwitch={() => setAuthMode('login')} />
            )}
          </div>
        </div>
      )}
    </div>
  );
}
