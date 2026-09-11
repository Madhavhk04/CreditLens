import Sparkline from '../charts/Sparkline'
import PillToggle from '../interactive/PillToggle'
import { TrendingUp } from 'lucide-react'

export default function HeroRiskCard() {
  const sparkData = [
    { v: 1.8 }, { v: 1.9 }, { v: 2.0 }, { v: 1.95 }, { v: 2.1 },
    { v: 2.15 }, { v: 2.2 }, { v: 2.05 }, { v: 2.3 }, { v: 2.35 }, { v: 2.4 }
  ]

  return (
    <div className="hero-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', position: 'relative', zIndex: 1 }}>
        <div>
          <div className="hero-card-label">Portfolio at risk (PAR 30)</div>
          <div className="hero-card-value">2.40%</div>
          <div className="hero-card-meta">
            <span className="hero-trend-badge">
              <TrendingUp size={12} strokeWidth={2.5} />
              +0.35% MoM
            </span>
            <span className="hero-exposure">$3.48M past-due · vs 2.00% target</span>
          </div>
        </div>
        <PillToggle options={['1M', '3M', '6M', '1Y']} />
      </div>
      <div className="hero-sparkline-wrap" style={{ position: 'relative', zIndex: 1 }}>
        <Sparkline data={sparkData} color="rgba(255,255,255,0.6)" height={48} />
      </div>
    </div>
  )
}
