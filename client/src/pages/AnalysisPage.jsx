import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import SummaryCards from '../components/Dashboard/SummaryCards';
import InsightPanel from '../components/Dashboard/InsightPanel';
import DataTable from '../components/Dashboard/DataTable';
import ChartTypeSelector from '../components/Charts/ChartTypeSelector';
import ChartRenderer from '../components/Charts/ChartRenderer';
import AskAI from '../components/Chat/AskAI';

const TABS = ['Overview', 'Chart', 'Data', 'Ask AI'];

export default function AnalysisPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [dataset, setDataset] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('Overview');
  const [chartConfig, setChartConfig] = useState(null);

  useEffect(() => {
    const fetchDataset = async () => {
      try {
        const res = await axios.get(`/api/analysis/${id}`);
        setDataset(res.data);
        const numericCol = res.data.columns.find((c) => c.type === 'numeric');
        const firstCol = res.data.columns[0];
        setChartConfig({
          type: 'bar',
          x: firstCol?.name || '',
          y: numericCol?.name || firstCol?.name || '',
        });
      } catch {
        setError('Failed to load dataset. It may have been deleted.');
      } finally {
        setLoading(false);
      }
    };
    fetchDataset();
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-10 h-10 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <p className="text-slate-400">Loading dataset...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-400 mb-4">{error}</p>
          <Link to="/" className="btn-primary">Go home</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Navbar */}
      <nav className="border-b border-slate-800 px-6 py-4 flex items-center gap-4">
        <button
          onClick={() => navigate('/')}
          className="text-slate-400 hover:text-white transition-colors flex items-center gap-1 text-sm"
        >
          ← Back
        </button>
        <div className="flex items-center gap-2 flex-1 min-w-0">
          <span className="text-xl">📊</span>
          <span className="font-semibold text-white truncate">{dataset.filename}</span>
          <span className="text-slate-600 text-sm hidden sm:block">
            · {dataset.rowCount.toLocaleString()} rows · {dataset.columns.length} cols
          </span>
        </div>
        <Link to="/history" className="btn-secondary text-sm shrink-0">History</Link>
      </nav>

      {/* Tabs */}
      <div className="border-b border-slate-800">
        <div className="max-w-6xl mx-auto px-6 flex gap-1">
          {TABS.map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-3 text-sm font-medium transition-colors border-b-2 -mb-px ${
                activeTab === tab
                  ? 'border-brand-500 text-brand-400'
                  : 'border-transparent text-slate-500 hover:text-slate-300'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto px-6 py-8">
        {activeTab === 'Overview' && (
          <div className="space-y-6">
            <SummaryCards dataset={dataset} />
            <InsightPanel summary={dataset.aiSummary} />
            {/* Column details */}
            <div className="card">
              <h3 className="font-semibold text-white mb-4">Column Details</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-slate-800">
                      {['Column', 'Type', 'Unique', 'Nulls', 'Min', 'Max', 'Mean'].map((h) => (
                        <th key={h} className="px-3 py-2 text-left text-xs text-slate-500 uppercase tracking-wide">{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {dataset.columns.map((col) => (
                      <tr key={col.name} className="border-b border-slate-800/50 hover:bg-slate-800/20">
                        <td className="px-3 py-2 text-white font-medium">{col.name}</td>
                        <td className="px-3 py-2">
                          <span className={`text-xs px-2 py-0.5 rounded-full ${
                            col.type === 'numeric' ? 'bg-blue-900/40 text-blue-300' :
                            col.type === 'date' ? 'bg-purple-900/40 text-purple-300' :
                            'bg-slate-700 text-slate-300'
                          }`}>
                            {col.type}
                          </span>
                        </td>
                        <td className="px-3 py-2 text-slate-400">{col.uniqueCount}</td>
                        <td className="px-3 py-2 text-slate-400">{col.nullCount > 0 ? <span className="text-amber-400">{col.nullCount}</span> : 0}</td>
                        <td className="px-3 py-2 text-slate-400">{col.min ?? '—'}</td>
                        <td className="px-3 py-2 text-slate-400">{col.max ?? '—'}</td>
                        <td className="px-3 py-2 text-slate-400">{col.mean != null ? col.mean : '—'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'Chart' && chartConfig && (
          <div className="space-y-4">
            <ChartTypeSelector
              columns={dataset.columns}
              datasetId={id}
              config={chartConfig}
              setConfig={setChartConfig}
            />
            <div className="card">
              <ChartRenderer rows={dataset.rows} config={chartConfig} />
            </div>
          </div>
        )}

        {activeTab === 'Data' && (
          <DataTable rows={dataset.rows} columns={dataset.columns} />
        )}

        {activeTab === 'Ask AI' && (
          <AskAI datasetId={id} />
        )}
      </div>
    </div>
  );
}
