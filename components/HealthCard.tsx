'use client';

import useSWR from 'swr';
import { apiGet } from '@/lib/api';
import type { Health } from '@/lib/types';

export default function HealthCard() {
  const { data, error, isLoading } = useSWR<Health>('/api/health', apiGet);

  return (
    <div className="rounded-xl bg-slate-900 border border-slate-800 p-4 neon-cyan">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-medium">Service Health</h2>
        <span className={`h-3 w-3 rounded-full ${isLoading ? 'bg-yellow-400' : error ? 'bg-rose-400' : 'bg-emerald-400'}`} />
      </div>
      <div className="mt-3 text-sm">
        {isLoading && <p>Checking…</p>}
        {error && <p className="text-rose-300">Unavailable</p>}
        {data && (
          <ul className="space-y-1 text-slate-300">
            <li>Status: <b className="text-slate-100">{data.status}</b></li>
            <li>Version: {data.version}</li>
            <li>Runtime: {data.runtime}</li>
          </ul>
        )}
      </div>
    </div>
  );
}
