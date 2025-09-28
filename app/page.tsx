'use client';

import { motion } from 'framer-motion';
import HealthCard from '@/components/HealthCard';
import MetricsPanel from '@/components/MetricsPanel';
import KwordPanel from '@/components/KwordPanel';
import TriggersPanel from '@/components/TriggersPanel';
import ReportPanel from '@/components/ReportPanel';

export default function Dashboard() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <motion.h1
          className="text-3xl md:text-4xl font-semibold tracking-tight mb-6"
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
        >
          AIgent K‑WORD Dashboard
        </motion.h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <HealthCard />
          <MetricsPanel />
          <TriggersPanel />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
          <KwordPanel />
          <ReportPanel />
        </div>
      </div>
    </main>
  );
}
 
