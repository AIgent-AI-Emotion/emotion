'use client';

import { useState } from 'react';
import { apiPost } from '@/lib/api';

const TRIGGERS = [
  '/rememberEverything',
  '/viewEverything',
  '/autoHealEverything',
  '/getUpdatedMetrics',
  '/viewMetrics',
];

export default function TriggersPanel() {
  const [output, setOutput] = useState<string>('Run a trigger to see output.');

  async function run(trigger: string) {
    try {
      const res = await apiPost('/api/triggers/run', { trigger });
      setOutput(JSON.stringify(res, null, 2));
    } catch (e: any) {
      setOutput(`Error: ${e.message}`);
    }
  }

  return (
    <div className="rounded-xl bg-slate-900 border border-slate-800 p-4">
      <h2 className="text-lg font-medium mb-3">Triggers</h2>
      <div className="flex flex-wrap gap-2">
        {TRIGGERS.map((t) => (
          <button key={t}
            onClick={() => run(t)}
            className="px-3 py-2 bg-slate-800 hover:bg-slate-700 rounded-md text-sm">
            {t}
          </button>
        ))}
      </div>
      <pre className="mt-3 max-h-56 overflow-auto bg-slate-950/50 rounded-md p-3 text-xs text-slate-300">
        {output}
      </pre>
    </div>
  );
}
