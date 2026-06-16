import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

export default function HistoryPage() {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(null);
  const { logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    axios.get('/api/analysis')
      .then((res) => setDatasets(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm('Delete this dataset?')) return;
    setDeleting(id);
    try {
      await axios.delete(`/api/analysis/${id}`);
      setDatasets((ds) => ds.filter((d) => d._id !== id));
    } catch {
      alert('Failed to delete dataset');
    } finally {
      setDeleting(null);
    }
  };

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit',
    });
  };

  return (
    <div className="min-h-screen bg-slate-950">
      <nav className="border-b border-slate-800 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button onClick={() => navigate('/')} className="text-slate-400 hover:text-white text-sm transition-colors">
            ← Back
          </button>
          <div className="flex items-center gap-2">
            <span className="text-xl">📊</span>
            <span className="font-bold text-white">DataLens AI</span>
          </div>
        </div>
        <button onClick={logout} className="text-slate-500 hover:text-slate-300 text-sm transition-colors">
          Sign out
        </button>
      </nav>

      <div className="max-w-4xl mx-auto px-6 py-10">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-2xl font-bold text-white">Upload History</h1>
          <Link to="/" className="btn-primary text-sm">+ New upload</Link>
        </div>

        {loading ? (
          <div className="text-center py-20 text-slate-500">Loading...</div>
        ) : datasets.length === 0 ? (
          <div className="text-center py-20">
            <div className="text-5xl mb-4">📂</div>
            <p className="text-slate-400 mb-4">No datasets yet</p>
            <Link to="/" className="btn-primary">Upload your first CSV</Link>
          </div>
        ) : (
          <div className="space-y-3">
            {datasets.map((ds) => (
              <div
                key={ds._id}
                onClick={() => navigate(`/analysis/${ds._id}`)}
                className="card flex items-center justify-between cursor-pointer hover:border-slate-600 transition-all group"
              >
                <div className="flex items-center gap-4 min-w-0">
                  <div className="text-2xl">📄</div>
                  <div className="min-w-0">
                    <div className="font-medium text-white truncate group-hover:text-brand-300 transition-colors">
                      {ds.filename}
                    </div>
                    <div className="text-xs text-slate-500 mt-0.5">
                      {ds.rowCount?.toLocaleString()} rows · {ds.columns?.length} columns · {formatDate(ds.createdAt)}
                    </div>
                  </div>
                </div>
                <button
                  onClick={(e) => handleDelete(ds._id, e)}
                  disabled={deleting === ds._id}
                  className="text-slate-600 hover:text-red-400 transition-colors p-2 shrink-0 ml-4"
                  title="Delete"
                >
                  {deleting === ds._id ? '...' : '🗑️'}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
