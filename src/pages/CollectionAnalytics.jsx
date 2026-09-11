import { useState } from 'react'
import TopBar from '../components/layout/TopBar'
import GlassCard from '../components/cards/GlassCard'
import RiskMemo from '../components/content/RiskMemo'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts'

const agentData = [
  { id: 'Agent-101', recovered: 840 },
  { id: 'Agent-104', recovered: 720 },
  { id: 'Agent-108', recovered: 680 },
  { id: 'Agent-112', recovered: 540 },
  { id: 'Agent-115', recovered: 490 },
  { id: 'Agent-120', recovered: 410 },
]

const stratData = [
  { name: 'SMS / Digital', value: 35 },
  { name: 'Tele-calling', value: 45 },
  { name: 'Field visits', value: 12 },
  { name: 'Legal escalation', value: 8 },
]

const COLORS = ['#3b82f6', '#06b6d4', '#f59e0b', '#ef4444']

const chartStyle = {
  contentStyle: { background: '#1a1a2e', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 12, color: '#f0f0f5', fontSize: 12 }
}

export default function CollectionAnalytics() {
  const [smsPct, setSmsPct] = useState(30)
  const [callPct, setCallPct] = useState(50)
  const legalPct = Math.max(0, 100 - smsPct - callPct)
  const projected = 8.4 * (1 + smsPct / 100 * 0.05 + callPct / 100 * 0.12 + legalPct / 100 * 0.22)

  return (
    <div>
      <TopBar title="Collections efficacy & outreach strategy" />

      <div className="grid grid-chart-table gap-20">
        <RiskMemo
          title="Collections audit memo"
          subtitle="Outreach resolution efficiencies"
          body='SMS/Digital outreach handles high early-stage volume at minimal expense, but <strong style="color:#f0f0f5">legal escalations</strong> deliver highest recovery values on prime defaults.'
          items={[
            'Top 3 collection agents account for 38% of recovered capital.',
            'Tele-calling converts at 14.5% Collections Efficiency Index (CEI).',
          ]}
        />
        <GlassCard>
          <div className="card-title">Collections efficiency by agent ($k recovered)</div>
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={agentData}>
                <XAxis dataKey="id" tick={{ fill: '#a1a1b5', fontSize: 11 }} axisLine={false} />
                <YAxis tick={{ fill: '#5a5a72', fontSize: 10, fontFamily: 'DM Mono' }} axisLine={false} />
                <Tooltip {...chartStyle} />
                <Bar dataKey="recovered" fill="#3b82f6" radius={[6, 6, 0, 0]} animationDuration={800} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
      </div>

      <div className="grid grid-stress gap-20 mt-20">
        <GlassCard>
          <div className="card-title">Recoveries by outreach strategy</div>
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={stratData} cx="50%" cy="50%" innerRadius="45%" outerRadius="80%" dataKey="value" nameKey="name" animationDuration={800} stroke="none">
                  {stratData.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
                </Pie>
                <Legend wrapperStyle={{ fontSize: 11, color: '#a1a1b5' }} />
                <Tooltip {...chartStyle} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
        <GlassCard>
          <div className="card-title">Strategy budget simulator</div>
          <div className="stress-label">SMS/Digital allocation: <span className="font-mono color-violet">{smsPct}%</span></div>
          <input type="range" className="stress-slider" min={0} max={100} step={5} value={smsPct} onChange={e => setSmsPct(+e.target.value)} />
          <div className="stress-label mt-16">Tele-calling allocation: <span className="font-mono color-violet">{callPct}%</span></div>
          <input type="range" className="stress-slider" min={0} max={100} step={5} value={callPct} onChange={e => setCallPct(+e.target.value)} />
          <div className="grid grid-2 gap-20 mt-16">
            <div className="sim-box"><div className="sim-box-label">Legal allocation</div><div className="sim-box-value color-amber">{legalPct}%</div></div>
            <div className="sim-box"><div className="sim-box-label">Projected recoveries</div><div className="sim-box-value color-green">${projected.toFixed(2)}M</div></div>
          </div>
        </GlassCard>
      </div>
    </div>
  )
}
