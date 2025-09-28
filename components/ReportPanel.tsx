'use client';

import { useState } from 'react';
import { apiPost } from '@/lib/api';

export default function ReportPanel() {
  const [json, setJson] = useState<string>('Click "Generate" to produce a summary.');

  async function generate() {
    try {
      const res = await apiPost('/api/reports/generate');
      setJson(JSON.stringify(res, null, 2));
    } catch (e: any) {
      setJson(`Error: ${e.message}`);
    }
  }

  return (
    <div className="rounded-xl bg-slate-900 border border-slate-800 p-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-medium">Report</h2>
        <button onClick={generate}
          className="px-3 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-md font-medium">
          Generate
        </button>
      </div>
      <pre className="mt-3 max-h-80 overflow-auto bg-slate-950/50 rounded-md p-3 text-xs text-slate-300">
        {json}
      </pre>
    </div>
  );
}
 
