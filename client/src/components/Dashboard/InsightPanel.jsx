import React from 'react';

export default function InsightPanel({ summary }) {
  return (
    <div className="card">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-xl">✨</span>
        <h3 className="font-semibold text-white">AI Summary</h3>
      </div>
      <p className="text-slate-300 leading-relaxed text-sm">{summary || 'No summary available.'}</p>
    </div>
  );
}
