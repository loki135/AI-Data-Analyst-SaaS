import React from 'react';

function StatCard({ label, value, icon }) {
  return (
    <div className="card flex items-center gap-4">
      <div className="text-3xl">{icon}</div>
      <div>
        <div className="text-2xl font-bold text-white">{value}</div>
        <div className="text-xs text-slate-500 uppercase tracking-wide">{label}</div>
      </div>
    </div>
  );
}

export default function SummaryCards({ dataset }) {
  const { rowCount, columns } = dataset;
  const numericCols = columns.filter((c) => c.type === 'numeric').length;
  const categoricalCols = columns.filter((c) => c.type === 'categorical').length;
  const nullCols = columns.filter((c) => c.nullCount > 0).length;

  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
      <StatCard label="Total Rows" value={rowCount.toLocaleString()} icon="📋" />
      <StatCard label="Columns" value={columns.length} icon="📐" />
      <StatCard label="Numeric" value={numericCols} icon="🔢" />
      <StatCard label="Categorical" value={categoricalCols} icon="🏷️" />
      <StatCard label="Cols w/ Nulls" value={nullCols} icon="⚠️" />
    </div>
  );
}
