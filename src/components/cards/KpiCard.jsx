import Sparkline from '../charts/Sparkline'
import GlassCard from './GlassCard'
import { TrendingUp, TrendingDown } from 'lucide-react'

export default function KpiCard({ label, value, trend, trendDir = 'neutral', color = '#a78bfa', sparkData }) {
  const trendClass =
    trendDir === 'up-bad' ? 'up-bad' :
    trendDir === 'down-good' ? 'down-good' :
    trendDir === 'up-good' ? 'up-good' : 'neutral'

  const TrendIcon = trendDir.startsWith('up') ? TrendingUp : TrendingDown

  return (
    <GlassCard variant="violet">
      <div className="kpi-card">
        <div className="kpi-label">{label}</div>
        <div className="kpi-value" style={{ color }}>{value}</div>
        {trend && (
          <div className={`kpi-trend ${trendClass}`}>
            <TrendIcon size={12} strokeWidth={2} />
            {trend}
          </div>
        )}
        {sparkData && (
          <div className="kpi-sparkline-wrap">
            <Sparkline data={sparkData} color={color} height={32} />
          </div>
        )}
      </div>
    </GlassCard>
  )
}
