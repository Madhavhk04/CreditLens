import { motion } from 'framer-motion'
import TopBar from '../components/layout/TopBar'
import HeroRiskCard from '../components/cards/HeroRiskCard'
import KpiCard from '../components/cards/KpiCard'
import RadialGauge from '../components/charts/RadialGauge'
import StressTester from '../components/interactive/StressTester'
import RiskMemo from '../components/content/RiskMemo'
import ChannelDonut from '../components/charts/ChannelDonut'
import ProductMatrix from '../components/content/ProductMatrix'
import GlassCard from '../components/cards/GlassCard'

const containerVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.08 } }
}

const itemVariants = {
  hidden: { opacity: 0, y: 12 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4, ease: 'easeOut' } }
}

const nplSpark = [{ v: 0.9 }, { v: 0.92 }, { v: 0.95 }, { v: 1.0 }, { v: 0.98 }, { v: 1.02 }, { v: 1.05 }, { v: 1.08 }, { v: 1.1 }]
const aumSpark = [{ v: 128 }, { v: 130 }, { v: 133 }, { v: 136 }, { v: 138 }, { v: 140 }, { v: 142 }, { v: 144 }, { v: 145.2 }]
const nimSpark = [{ v: 8.2 }, { v: 8.3 }, { v: 8.4 }, { v: 8.5 }, { v: 8.55 }, { v: 8.6 }, { v: 8.65 }, { v: 8.7 }]
const approvSpark = [{ v: 40 }, { v: 41 }, { v: 41.5 }, { v: 42 }, { v: 42.2 }, { v: 42.5 }]

const channelData = [
  { name: 'Organic search', value: 4200 },
  { name: 'Direct branch', value: 3100 },
  { name: 'Partner digital', value: 2400 },
  { name: 'Referral', value: 1800 },
]

export default function ExecutiveOverview() {
  return (
    <div>
      <TopBar title="Executive portfolio overview" />

      <motion.div variants={containerVariants} initial="hidden" animate="visible">
        {/* Row 1: Hero + Gauge */}
        <motion.div variants={itemVariants} className="grid grid-hero gap-20">
          <HeroRiskCard />
          <GlassCard>
            <RadialGauge score={68} size={170} />
          </GlassCard>
        </motion.div>

        {/* Row 2: KPI Cards */}
        <motion.div variants={itemVariants} className="grid grid-4 gap-20 mt-20">
          <KpiCard
            label="Non-performing loans (NPL 90+)"
            value="1.10%"
            trend="+0.12% MoM"
            trendDir="up-bad"
            color="#f87171"
            sparkData={nplSpark}
          />
          <KpiCard
            label="Active portfolio value"
            value="$145.2M"
            trend="+$3.8M QoQ"
            trendDir="up-good"
            color="#60a5fa"
            sparkData={aumSpark}
          />
          <KpiCard
            label="Net interest margin"
            value="8.70%"
            trend="Stable"
            trendDir="neutral"
            color="#4ade80"
            sparkData={nimSpark}
          />
          <KpiCard
            label="Approval conversion"
            value="42.5%"
            trend="+1.2% MoM"
            trendDir="up-good"
            color="#a78bfa"
            sparkData={approvSpark}
          />
        </motion.div>

        {/* Row 3: Stress Tester + Risk Memo */}
        <motion.div variants={itemVariants} className="grid grid-stress gap-20 mt-20">
          <StressTester />
          <RiskMemo
            title="Risk committee memorandum"
            subtitle="Executive risk findings & stress warning"
            body='Overall portfolio defaults remain bounded (NPL at 1.10%), but <strong style="color:#f87171">Cohort Mar 25 shows 2.4x accelerated delinquency migration</strong> at Month on Book (MOB) 6.'
            items={[
              '<strong style="color:#f0f0f5">Subprime segment (CIBIL &lt;650):</strong> PAR 30 expanded to 3.90%.',
              '<strong style="color:#f0f0f5">Geographic concentration:</strong> Uttar Pradesh NPL outlier at 4.20%.',
              '<strong style="color:#f0f0f5">Channel quality:</strong> Partner Digital affiliates driving 58% of defaults.',
            ]}
          />
        </motion.div>

        {/* Row 4: Channel Donut + Product Matrix */}
        <motion.div variants={itemVariants} className="grid grid-chart-table gap-20 mt-20">
          <GlassCard>
            <div className="card-title">Disbursed loans by channel</div>
            <div className="chart-wrap">
              <ChannelDonut data={channelData} />
            </div>
          </GlassCard>
          <ProductMatrix />
        </motion.div>
      </motion.div>
    </div>
  )
}
