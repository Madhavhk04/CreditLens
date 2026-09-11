import { useState } from 'react'
import TopBar from '../components/layout/TopBar'
import GlassCard from '../components/cards/GlassCard'
import KpiCard from '../components/cards/KpiCard'
import RiskMemo from '../components/content/RiskMemo'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts'

const queueData = [
  { custId: 'CUST-8821', cibil: 540, loanId: 'LN-9012', inst: '$1,450', dpd: 65, tier: 'Subprime' },
  { custId: 'CUST-7743', cibil: 580, loanId: 'LN-8834', inst: '$2,100', dpd: 45, tier: 'Subprime' },
  { custId: 'CUST-6612', cibil: 610, loanId: 'LN-7721', inst: '$980', dpd: 35, tier: 'Near Prime' },
  { custId: 'CUST-5541', cibil: 520, loanId: 'LN-6643', inst: '$3,400', dpd: 85, tier: 'Subprime' },
  { custId: 'CUST-4439', cibil: 630, loanId: 'LN-5512', inst: '$1,850', dpd: 40, tier: 'Near Prime' },
  { custId: 'CUST-3310', cibil: 590, loanId: 'LN-4489', inst: '$1,200', dpd: 75, tier: 'Subprime' },
]

const heatmapData = [
  { band: 'Subprime (300–599)', low: 6.8, mid: 4.5, high: 2.9 },
  { band: 'Near prime (600–679)', low: 4.2, mid: 2.8, high: 1.5 },
  { band: 'Prime (680–749)', low: 1.8, mid: 1.1, high: 0.5 },
  { band: 'Super prime (750+)', low: 0.4, mid: 0.2, high: 0.1 },
]

const chartStyle = {
  contentStyle: { background: '#1a1a2e', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 12, color: '#f0f0f5', fontSize: 12 }
}

export default function RiskIntelligence() {
  const [minDpd, setMinDpd] = useState(30)
  const filtered = queueData.filter(r => r.dpd >= minDpd)

  return (
    <div>
      <TopBar title="Delinquency segmentation & action queue" />

      <div className="grid grid-stress gap-20">
        <RiskMemo
          title="Risk segmentation findings"
          subtitle="Subprime concentration loss"
          body="Subprime borrowers with monthly income under $35,000 represent 58% of total portfolio default volume. Action queues prioritized by DPD and cover ratios."
          items={[]}
        />
        <KpiCard label="Subprime default share" value="58.0%" color="#f87171" trend="High-risk exposure" trendDir="up-bad" />
      </div>

      <div className="grid grid-chart-table gap-20 mt-20">
        <GlassCard>
          <div className="card-title">Action queue controller</div>
          <div className="stress-label">Minimum DPD: <span className="font-mono color-red">{minDpd}</span></div>
          <input type="range" className="stress-slider" min={30} max={90} step={5} value={minDpd} onChange={e => setMinDpd(+e.target.value)} />
        </GlassCard>
        <GlassCard>
          <div className="card-title">Priority outbound dialer queue</div>
          <div style={{ overflowX: 'auto' }}>
            <table className="data-table">
              <thead><tr><th>Customer</th><th>CIBIL</th><th>Loan</th><th>Installment</th><th>DPD</th><th>Tier</th></tr></thead>
              <tbody>
                {filtered.map(r => (
                  <tr key={r.custId}>
                    <td className="td-label" style={{ fontFamily: 'var(--font-body)' }}>{r.custId}</td>
                    <td>{r.cibil}</td>
                    <td>{r.loanId}</td>
                    <td>{r.inst}</td>
                    <td className="risk-val">{r.dpd} DPD</td>
                    <td><span className={`category-badge ${r.tier === 'Subprime' ? 'badge-red' : 'badge-amber'}`} style={{ borderRadius: 'var(--radius-pill)', padding: '3px 10px', fontSize: 11, fontWeight: 600, width: 'auto', height: 'auto' }}>{r.tier}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassCard>
      </div>

      <GlassCard className="mt-20">
        <div className="card-title">NPL default rate % (CIBIL band vs income decile)</div>
        <div className="chart-wrap">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={heatmapData}>
              <XAxis dataKey="band" tick={{ fill: '#a1a1b5', fontSize: 11 }} axisLine={false} />
              <YAxis tick={{ fill: '#5a5a72', fontSize: 10, fontFamily: 'DM Mono' }} axisLine={false} />
              <Tooltip {...chartStyle} />
              <Legend wrapperStyle={{ fontSize: 11, color: '#a1a1b5' }} />
              <Bar dataKey="low" name="Low income" fill="#ef4444" radius={[4, 4, 0, 0]} animationDuration={800} />
              <Bar dataKey="mid" name="Mid income" fill="#f59e0b" radius={[4, 4, 0, 0]} animationDuration={800} />
              <Bar dataKey="high" name="High income" fill="#3b82f6" radius={[4, 4, 0, 0]} animationDuration={800} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </GlassCard>
    </div>
  )
}
