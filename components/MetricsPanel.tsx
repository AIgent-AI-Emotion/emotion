'use client';

import useSWR from 'swr';
import { useState } from 'react';
import { apiGet, apiPost } from '@/lib/api';
import type { Metrics } from '@/lib/types';

export default function MetricsPanel() {
  const { data, mutate, isLoading, error } = useSWR<Metrics>('/api/metrics', apiGet);
  const [key, setKey] = useState('');
  const [value, setValue] = useState('');

  const upsert = async () => {
    if (!key.trim()) return;
    const parsed = tryParse(value);
    await apiPost('/api/metrics', { [key.trim()]: parsed });
    setKey(''); setValue('');
    mutate(); // refresh
  };

  return (
    <div className="rounded-xl bg-slate-900 border border-slate-800 p-4">
      <h2 className="text-lg font-medium mb-3">Metrics</h2>

      <div className="grid grid-cols-1 gap-2">
        {isLoading && <p>Loading…</p>}
        {error && <p className="text-rose-300">Failed to load metrics</p>}
        {data && Object.entries(data).length === 0 && <p className="text-slate-400">No metrics yet.</p>}
        {data && Object.entries(data).map(([k, v]) => (
          <div key={k} className="flex items-center justify-between bg-slate-950/50 rounded-md px-3 py-2">
            <span className="text-slate-300">{k}</span>
            <span className="text-slate-100">{String(v)}</span>
          </div>
        ))}
      </div>

      <div className="mt-4 flex gap-2">
        <input
          className="flex-1 bg-slate-800 rounded-md px-3 py-2 outline-none"
          placeholder="Metric key (e.g., Clarity)"
          value={key} onChange={(e) => setKey(e.target.value)}
        />
        <input
          className="flex-1 bg-slate-800 rounded-md px-3 py-2 outline-none"
          placeholder="Value (auto-typed)"
          value={value} onChange={(e) => setValue(e.target.value)}
        />
        <button onClick={upsert}
          className="px-3 py-2 bg-cyan-500 hover:bg-cyan-400 text-slate-900 rounded-md font-medium">
          Save
        </button>
      </div>
    </div>
  );
}

function tryParse(val: string): number | boolean | string {
  if (val === 'true') return true;
  if (val === 'false') return false;
  const num = Number(val);
  if (!Number.isNaN(num) && val.trim() !== '') return num;
  return val;
}
