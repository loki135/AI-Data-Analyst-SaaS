import React, { useState } from 'react';
import api from '../../api';

const CHART_TYPES = ['bar', 'line', 'pie'];

export default function ChartTypeSelector({ columns, datasetId, config, setConfig }) {
  const [suggesting, setSuggesting] = useState(false);
  const [reason, setReason] = useState('');

  const numericCols = columns.filter((c) => c.type === 'numeric').map((c) => c.name);
  const allCols = columns.map((c) => c.name);

  const handleSuggest = async () => {
    setSuggesting(true);
    setReason('');
    try {
      const res = await api.post('/api/ai/suggest-chart', { datasetId });
      const { type, x, y, reason: r } = res.data;
      setConfig({
        type: CHART_TYPES.includes(type) ? type : 'bar',
        x: allCols.includes(x) ? x : allCols[0],
        y: allCols.includes(y) ? y : numericCols[0] || allCols[1],
      });
      setReason(r);
    } catch {
      setReason('Could not get AI suggestion. Check your Gemini API key.');
    } finally {
      setSuggesting(false);
    }
  };

  return (
    <div className="card space-y-4">
      <div className="flex flex-wrap gap-3 items-center justify-between">
        <div className="flex gap-2">
          {CHART_TYPES.map((t) => (
            <button
              key={t}
              onClick={() => setConfig((c) => ({ ...c, type: t }))}
              className={`px-4 py-1.5 rounded-lg text-sm font-medium border transition-colors ${
                config.type === t
                  ? 'bg-brand-500 border-brand-500 text-white'
                  : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-500'
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        <button
          onClick={handleSuggest}
          disabled={suggesting}
          className="btn-secondary text-sm flex items-center gap-2"
        >
          <span>✨</span>
          {suggesting ? 'Thinking...' : 'AI suggest'}
        </button>
      </div>

      <div className="flex flex-wrap gap-4">
        <div className="flex-1 min-w-32">
          <label className="block text-xs text-slate-500 mb-1">X axis</label>
          <select
            className="input text-sm"
            value={config.x}
            onChange={(e) => setConfig((c) => ({ ...c, x: e.target.value }))}
          >
            {allCols.map((col) => (
              <option key={col} value={col}>{col}</option>
            ))}
          </select>
        </div>
        {config.type !== 'pie' && (
          <div className="flex-1 min-w-32">
            <label className="block text-xs text-slate-500 mb-1">Y axis</label>
            <select
              className="input text-sm"
              value={config.y}
              onChange={(e) => setConfig((c) => ({ ...c, y: e.target.value }))}
            >
              {numericCols.map((col) => (
                <option key={col} value={col}>{col}</option>
              ))}
            </select>
          </div>
        )}
      </div>

      {reason && (
        <div className="text-xs text-slate-400 bg-slate-800/50 px-3 py-2 rounded-lg">
          ✨ {reason}
        </div>
      )}
    </div>
  );
}
