import { useState } from 'react'
import { motion } from 'framer-motion'
import TopBar from '../components/layout/TopBar'
import GlassCard from '../components/cards/GlassCard'
import KpiCard from '../components/cards/KpiCard'
import RiskMemo from '../components/content/RiskMemo'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, FunnelChart } from 'recharts'

const funnelData = [
  { name: '1. Applied', value: 250000, fill: '#8b5cf6' },
  { name: '2. KYC passed', value: 212500, fill: '#06b6d4' },
  { name: '3. Verified', value: 150000, fill: '#22c55e' },
  { name: '4. Approved', value: 106250, fill: '#f59e0b' },
  { name: '5. Disbursed', value: 100000, fill: '#64748b' },
]

const rejectData = [
  { reason: 'CIBIL below threshold', count: 60500 },
  { reason: 'High debt-cover ratio', count: 38200 },
  { reason: 'Unverified income', count: 24100 },
  { reason: 'Employer verification fail', count: 14200 },
  { reason: 'Document mismatch', count: 6750 },
]

const chartStyle = {
  contentStyle: { background: '#1a1a2e', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 12, color: '#f0f0f5', fontSize: 12 }
}

export default function UnderwritingFunnel() {
  const [simIncome, setSimIncome] = useState(30000)
  const [simCibil, setSimCibil] = useState(650)

  const incRatio = (simIncome - 10000) / 90000
  const cibilRatio = (simCibil - 300) / 600
  const appRate = Math.max(5, Math.min(95, 42.5 * (1 - cibilRatio * 0.45 - incRatio * 0.15)))
  const declines = Math.round(250000 * (1 - appRate / 100))

  return (
    <div>
      <TopBar title="Underwriting funnel & pipeline" />

      <div className="grid grid-3 gap-20">
        <RiskMemo
          title="Underwriting audit memo"
          subtitle="Verification stage bottleneck"
          body="Significant attrition between <strong style='color:#f0f0f5'>KYC Passed</strong> and <strong style='color:#f0f0f5'>Verified</strong>, driving total TAT to 18.5 hours."
          items={[
            'CIBIL threshold breaches cause 42% of total declines.',
            'Income verification holds 12.5 hours of processing latency.',
            'Auto loan throughput is 1.8x faster than housing loans.',
          ]}
        />
        <KpiCard label="Total applications" value="250,000" color="#a78bfa" sparkData={[{v:230},{v:235},{v:240},{v:245},{v:248},{v:250}]} />
        <div className="grid" style={{ gap: 16 }}>
          <KpiCard label="Approval rate" value="42.50%" trend="Passed underwriting" trendDir="neutral" color="#4ade80" />
          <KpiCard label="Avg pipeline TAT" value="18.5 hrs" color="#60a5fa" />
        </div>
      </div>

      <div className="grid grid-stress gap-20 mt-20">
        <GlassCard>
          <div className="card-title">Underwriting funnel milestones</div>
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={funnelData} layout="vertical" margin={{ left: 20 }}>
                <XAxis type="number" tick={{ fill: '#5a5a72', fontSize: 11, fontFamily: 'DM Mono' }} axisLine={false} />
                <YAxis type="category" dataKey="name" tick={{ fill: '#a1a1b5', fontSize: 12 }} axisLine={false} width={110} />
                <Tooltip {...chartStyle} />
                <Bar dataKey="value" radius={[0, 6, 6, 0]} animationDuration={800}>
                  {funnelData.map((e, i) => (
                    <motion.rect key={i} fill={e.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>

        <GlassCard>
          <div className="card-title">Underwriting simulator</div>
          <div className="stress-label">Min monthly income ($): <span className="font-mono color-violet">{simIncome.toLocaleString()}</span></div>
          <input type="range" className="stress-slider" min={10000} max={100000} step={5000} value={simIncome} onChange={e => setSimIncome(+e.target.value)} />
          <div className="stress-label mt-16">Min CIBIL score: <span className="font-mono color-violet">{simCibil}</span></div>
          <input type="range" className="stress-slider" min={300} max={900} step={10} value={simCibil} onChange={e => setSimCibil(+e.target.value)} />
          <div className="grid grid-2 gap-20 mt-16">
            <div className="sim-box"><div className="sim-box-label">Projected approval rate</div><div className="sim-box-value color-green">{appRate.toFixed(1)}%</div></div>
            <div className="sim-box"><div className="sim-box-label">Estimated declines</div><div className="sim-box-value color-red">{declines.toLocaleString()}</div></div>
          </div>
        </GlassCard>
      </div>

      <GlassCard className="mt-20">
        <div className="card-title">Top underwriting rejection reasons</div>
        <div className="chart-wrap">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={rejectData} layout="vertical" margin={{ left: 30 }}>
              <XAxis type="number" tick={{ fill: '#5a5a72', fontSize: 11, fontFamily: 'DM Mono' }} axisLine={false} />
              <YAxis type="category" dataKey="reason" tick={{ fill: '#a1a1b5', fontSize: 11 }} axisLine={false} width={180} />
              <Tooltip {...chartStyle} />
              <Bar dataKey="count" fill="#ef4444" radius={[0, 6, 6, 0]} animationDuration={800} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </GlassCard>
    </div>
  )
}
