import { useState } from 'react'
import TopBar from '../components/layout/TopBar'
import GlassCard from '../components/cards/GlassCard'
import KpiCard from '../components/cards/KpiCard'
import RiskMemo from '../components/content/RiskMemo'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, BarChart, Bar } from 'recharts'

const mobs = Array.from({ length: 13 }, (_, i) => `MOB ${i}`)
const baseJan = [0.0, 0.1, 0.3, 0.6, 0.9, 1.2, 1.5, 1.7, 1.9, 2.1, 2.3, 2.4, 2.4]
const baseFeb = [0.0, 0.05, 0.2, 0.4, 0.7, 0.95, 1.1, 1.2, 1.3, 1.4, 1.5, 1.5, 1.6]
const baseMar = [0.0, 0.15, 0.45, 0.9, 1.4, 1.8, 2.2, 2.5, 2.9, 3.2, 3.6, 3.8, 3.9]

const repayData = Array.from({ length: 12 }, (_, i) => ({
  inst: `Inst ${i + 1}`,
  scheduled: 12.4,
  actual: 12.4 - i * 0.17,
}))

const chartStyle = {
  contentStyle: { background: '#1a1a2e', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 12, color: '#f0f0f5', fontSize: 12 }
}

export default function PortfolioPerformance() {
  const [cohort, setCohort] = useState('Cohort Mar 25')
  const [stress, setStress] = useState(1.0)

  const applyStress = (base, name) => base.map(v => name === cohort ? v * stress : v)

  const vintageData = mobs.map((m, i) => ({
    mob: m,
    'Jan 25': applyStress(baseJan, 'Cohort Jan 25')[i],
    'Feb 25': applyStress(baseFeb, 'Cohort Feb 25')[i],
    'Mar 25': applyStress(baseMar, 'Cohort Mar 25')[i],
  }))

  return (
    <div>
      <TopBar title="Portfolio maturities & vintage delinquency" />

      <div className="grid grid-stress gap-20">
        <RiskMemo
          title="Vintage audit memo"
          subtitle="Cohort Mar '25 early stress warning"
          body="Repayment ledgers indicate an amortization gap of $1.2M in past-due installment maturities. Cohort Mar 25 shows cumulative default expansion starting at MOB 4."
          items={[]}
        />
        <KpiCard label="Repayment amortization gap" value="$1.2M" color="#fbbf24" trend="Maturity delay" trendDir="up-bad" />
      </div>

      <div className="grid grid-chart-table gap-20 mt-20">
        <GlassCard>
          <div className="card-title">Vintage stress controller</div>
          <div className="stress-label">Target cohort</div>
          <select className="glass-select" value={cohort} onChange={e => setCohort(e.target.value)}>
            <option>Cohort Jan 25</option>
            <option>Cohort Feb 25</option>
            <option>Cohort Mar 25</option>
          </select>
          <div className="stress-label mt-16">Stress multiplier: <span className="font-mono color-red">{stress.toFixed(1)}x</span></div>
          <input type="range" className="stress-slider" min={1.0} max={3.0} step={0.1} value={stress} onChange={e => setStress(+e.target.value)} />
        </GlassCard>
        <GlassCard>
          <div className="card-title">Vintage cohort delinquency curves (MOB 0–12)</div>
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={vintageData}>
                <XAxis dataKey="mob" tick={{ fill: '#5a5a72', fontSize: 10, fontFamily: 'DM Mono' }} axisLine={false} />
                <YAxis tick={{ fill: '#5a5a72', fontSize: 10, fontFamily: 'DM Mono' }} axisLine={false} />
                <Tooltip {...chartStyle} />
                <Legend wrapperStyle={{ fontSize: 11, color: '#a1a1b5' }} />
                <Line type="monotone" dataKey="Jan 25" stroke="#22c55e" strokeWidth={2} dot={false} animationDuration={800} />
                <Line type="monotone" dataKey="Feb 25" stroke="#3b82f6" strokeWidth={2} dot={false} animationDuration={800} />
                <Line type="monotone" dataKey="Mar 25" stroke="#ef4444" strokeWidth={2.5} strokeDasharray="5 5" dot={false} animationDuration={800} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
      </div>

      <GlassCard className="mt-20">
        <div className="card-title">Scheduled dues vs actual collected ($M)</div>
        <div className="chart-wrap">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={repayData}>
              <XAxis dataKey="inst" tick={{ fill: '#5a5a72', fontSize: 10, fontFamily: 'DM Mono' }} axisLine={false} />
              <YAxis tick={{ fill: '#5a5a72', fontSize: 10, fontFamily: 'DM Mono' }} axisLine={false} />
              <Tooltip {...chartStyle} />
              <Legend wrapperStyle={{ fontSize: 11, color: '#a1a1b5' }} />
              <Bar dataKey="scheduled" name="Scheduled" fill="#3b82f6" radius={[4, 4, 0, 0]} animationDuration={800} />
              <Bar dataKey="actual" name="Actual collected" fill="#22c55e" radius={[4, 4, 0, 0]} animationDuration={800} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </GlassCard>
    </div>
  )
}
