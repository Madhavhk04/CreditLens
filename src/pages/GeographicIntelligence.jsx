import { useState } from 'react'
import TopBar from '../components/layout/TopBar'
import GlassCard from '../components/cards/GlassCard'
import KpiCard from '../components/cards/KpiCard'
import RiskMemo from '../components/content/RiskMemo'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'

const defaultData = [
  { state: 'Maharashtra', rate: 1.20 },
  { state: 'Delhi', rate: 0.95 },
  { state: 'Uttar Pradesh', rate: 4.20 },
  { state: 'Karnataka', rate: 0.85 },
  { state: 'Tamil Nadu', rate: 1.10 },
  { state: 'Telangana', rate: 0.70 },
  { state: 'West Bengal', rate: 2.10 },
  { state: 'Bihar', rate: 3.40 },
  { state: 'Madhya Pradesh', rate: 1.80 },
  { state: 'Gujarat', rate: 0.90 },
]

const volumeData = [
  { state: 'Maharashtra', volume: 35.4 },
  { state: 'Delhi', volume: 24.5 },
  { state: 'Karnataka', volume: 21.5 },
  { state: 'Uttar Pradesh', volume: 18.2 },
  { state: 'Tamil Nadu', volume: 16.4 },
  { state: 'Telangana', volume: 12.2 },
  { state: 'Gujarat', volume: 11.5 },
  { state: 'West Bengal', volume: 9.8 },
  { state: 'Madhya Pradesh', volume: 8.4 },
  { state: 'Bihar', volume: 7.2 },
]

const chartStyle = {
  contentStyle: { background: '#1a1a2e', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 12, color: '#f0f0f5', fontSize: 12 }
}

export default function GeographicIntelligence() {
  const [thresh, setThresh] = useState(2.5)

  return (
    <div>
      <TopBar title="Geographic concentration & loss heatmap" />

      <div className="grid grid-stress gap-20">
        <RiskMemo
          title="Geographic risk memo"
          subtitle="State default concentration outliers"
          body='Maharashtra and Delhi hold top funding volumes with healthy defaults (&lt;1.20%). However, <strong style="color:#f87171">Uttar Pradesh (4.20%) and Bihar (3.40%)</strong> exceed risk tolerance limits.'
          items={[]}
        />
        <KpiCard label="Highest state NPL (Uttar Pradesh)" value="4.20%" color="#f87171" trend="Concentration outlier" trendDir="up-bad" />
      </div>

      <div className="grid grid-chart-table gap-20 mt-20">
        <GlassCard>
          <div className="card-title">Exposure threshold controller</div>
          <div className="stress-label">Highlight rates above: <span className="font-mono color-red">{thresh.toFixed(1)}%</span></div>
          <input type="range" className="stress-slider" min={0.5} max={5.0} step={0.1} value={thresh} onChange={e => setThresh(+e.target.value)} />
        </GlassCard>
        <GlassCard>
          <div className="card-title">State default rates (%)</div>
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={defaultData} layout="vertical" margin={{ left: 10 }}>
                <XAxis type="number" tick={{ fill: '#5a5a72', fontSize: 10, fontFamily: 'DM Mono' }} axisLine={false} />
                <YAxis type="category" dataKey="state" tick={{ fill: '#a1a1b5', fontSize: 11 }} axisLine={false} width={120} />
                <Tooltip {...chartStyle} />
                <Bar dataKey="rate" radius={[0, 6, 6, 0]} animationDuration={800}>
                  {defaultData.map((d, i) => (
                    <Cell key={i} fill={d.rate > thresh ? '#ef4444' : '#22c55e'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
      </div>

      <GlassCard className="mt-20">
        <div className="card-title">State-level disbursement volumes ($M)</div>
        <div className="chart-wrap">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={volumeData} layout="vertical" margin={{ left: 10 }}>
              <XAxis type="number" tick={{ fill: '#5a5a72', fontSize: 10, fontFamily: 'DM Mono' }} axisLine={false} />
              <YAxis type="category" dataKey="state" tick={{ fill: '#a1a1b5', fontSize: 11 }} axisLine={false} width={120} />
              <Tooltip {...chartStyle} />
              <Bar dataKey="volume" fill="#8b5cf6" radius={[0, 6, 6, 0]} animationDuration={800} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </GlassCard>
    </div>
  )
}
