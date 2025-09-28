 
'use client';

import useSWR from 'swr';
import { useState } from 'react';
import { apiGet, apiPost } from '@/lib/api';
import type { KWord } from '@/lib/types';

type KWordList = { kwords: KWord[] };

export default function KwordPanel() {
  const { data, mutate } = useSWR<KWordList>('/api/matrix/kwords', apiGet);
  const [name, setName] = useState('');
  const [tags, setTags] = useState('+Founder,÷Architect,@AIgent');
  const [attrs, setAttrs] = useState('{"%Metrics":{"Clarity":0.98}}');

  const add = async () => {
    if (!name.trim()) return;
    let attributes: Record<string, unknown> | undefined = undefined;
    try { attributes = JSON.parse(attrs); } catch { /* ignore */ }
    await apiPost('/api/matrix/kwords', {
      name: name.trim(),
      tags: splitTags(tags),
      attributes
    });
    setName(''); // keep tags/attrs as defaults
    mutate();
  };

  return (
    <div className="rounded-xl bg-slate-900 border border-slate-800 p-4">
      <h2 className="text-lg font-medium mb-3">K‑WORD Matrix</h2>

      <div className="space-y-2">
        <input
          className="w-full bg-slate-800 rounded-md px-3 py-2 outline-none"
          placeholder="Name (e.g., ×Kevin Michael Norman)"
          value={name} onChange={(e) => setName(e.target.value)}
        />
        <input
          className="w-full bg-slate-800 rounded-md px-3 py-2 outline-none"
          placeholder="Tags comma-separated (e.g., +Founder,÷Architect,@AIgent)"
          value={tags} onChange={(e) => setTags(e.target.value)}
        />
        <textarea
          className="w-full bg-slate-800 rounded-md px-3 py-2 outline-none"
          rows={3}
          placeholder='Attributes JSON (optional)'
          value={attrs} onChange={(e) => setAttrs(e.target.value)}
        />
        <button onClick={add}
          className="px-3 py-2 bg-pink-500 hover:bg-pink-400 text-slate-900 rounded-md font-medium">
          Add K‑WORD
        </button>
      </div>

      <div className="mt-4 space-y-2 max-h-72 overflow-auto pr-1">
        {!data && <p className="text-slate-400">Loading…</p>}
        {data?.kwords?.length === 0 && <p className="text-slate-400">No entries yet.</p>}
        {data?.kwords?.slice().reverse().map((k) => (
          <div key={k.id || k.name} className="bg-slate-950/50 rounded-md px-3 py-2">
            <div className="text-slate-100 font-medium">{k.name}</div>
            <div className="text-slate-300 text-sm">{k.tags?.join('  ')}</div>
            {k.created_at && <div className="text-slate-500 text-xs mt-1">{k.created_at}</div>}
          </div>
        ))}
      </div>
    </div>
  );
}

function splitTags(s: string) {
  return s.split(',').map((t) => t.trim()).filter(Boolean);
}
 
