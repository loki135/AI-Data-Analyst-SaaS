import React from 'react';
import {
  ResponsiveContainer,
  BarChart, Bar,
  LineChart, Line,
  PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts';

const COLORS = ['#0ea5e9', '#38bdf8', '#7dd3fc', '#bae6fd', '#0369a1', '#075985', '#0284c7', '#0c4a6e'];

export default function ChartRenderer({ rows, config }) {
  const { type, x, y } = config;
  const data = rows.slice(0, 50).map((row) => ({
    [x]: row[x],
    [y]: isNaN(Number(row[y])) ? 0 : Number(row[y]),
  }));

  const commonProps = {
    data,
    margin: { top: 10, right: 20, left: 0, bottom: 40 },
  };

  const tooltipStyle = {
    backgroundColor: '#1e293b',
    border: '1px solid #334155',
    borderRadius: '8px',
    color: '#e2e8f0',
  };

  if (type === 'bar') {
    return (
      <ResponsiveContainer width="100%" height={320}>
        <BarChart {...commonProps}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis dataKey={x} tick={{ fill: '#94a3b8', fontSize: 11 }} angle={-30} textAnchor="end" interval="preserveStartEnd" />
          <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} />
          <Tooltip contentStyle={tooltipStyle} />
          <Bar dataKey={y} fill="#0ea5e9" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    );
  }

  if (type === 'line') {
    return (
      <ResponsiveContainer width="100%" height={320}>
        <LineChart {...commonProps}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis dataKey={x} tick={{ fill: '#94a3b8', fontSize: 11 }} angle={-30} textAnchor="end" interval="preserveStartEnd" />
          <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} />
          <Tooltip contentStyle={tooltipStyle} />
          <Line type="monotone" dataKey={y} stroke="#0ea5e9" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    );
  }

  if (type === 'pie') {
    const pieData = data.slice(0, 8).map((d) => ({ name: String(d[x]), value: d[y] }));
    return (
      <ResponsiveContainer width="100%" height={320}>
        <PieChart>
          <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={120} label={({ name }) => name}>
            {pieData.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip contentStyle={tooltipStyle} />
          <Legend wrapperStyle={{ color: '#94a3b8', fontSize: 12 }} />
        </PieChart>
      </ResponsiveContainer>
    );
  }

  return null;
}
