import { useState, useCallback } from 'react'
import { motion, useMotionValue, useSpring, useTransform } from 'framer-motion'
import GlassCard from '../cards/GlassCard'

export default function StressTester() {
  const [cutoff, setCutoff] = useState(600)

  const portfolioMotion = useMotionValue(145.2)
  const nplMotion = useMotionValue(1.10)

  const portfolioSpring = useSpring(portfolioMotion, { stiffness: 300, damping: 30 })
  const nplSpring = useSpring(nplMotion, { stiffness: 300, damping: 30 })

  const handleSlide = useCallback((e) => {
    const val = parseInt(e.target.value, 10)
    setCutoff(val)

    const targetPort = Math.max(85.0, 145.2 - ((val - 600) / 250.0) * 45.0)
    let targetNpl = 1.10
    if (val > 600) {
      targetNpl = Math.max(0.15, 1.10 - ((val - 600) / 250.0) * 0.95)
    } else {
      targetNpl = Math.min(4.50, 1.10 + ((600 - val) / 300.0) * 3.4)
    }

    portfolioMotion.set(targetPort)
    nplMotion.set(targetNpl)
  }, [portfolioMotion, nplMotion])

  return (
    <GlassCard variant="violet">
      <div className="card-title">Interactive credit stress tester</div>

      <div className="stress-label">
        Underwriting CIBIL cutoff floor: <span className="font-mono color-violet">{cutoff}</span>
      </div>
      <input
        type="range"
        className="stress-slider"
        min={300}
        max={850}
        step={10}
        value={cutoff}
        onChange={handleSlide}
      />

      <div className="grid grid-2 gap-20 mt-16">
        <div className="sim-box">
          <div className="sim-box-label">Simulated portfolio value</div>
          <motion.div className="sim-box-value color-violet">
            {useTransform(portfolioSpring, v => `$${v.toFixed(1)}M`)}
          </motion.div>
        </div>
        <div className="sim-box">
          <div className="sim-box-label">Simulated NPL rate</div>
          <NplDisplay spring={nplSpring} />
        </div>
      </div>

      <p className="card-note">
        Adjusting the minimum credit score acts as an immediate lever on underwriting conversions. Raising limits cuts high-risk default volumes but restricts outstanding balances.
      </p>
    </GlassCard>
  )
}

function NplDisplay({ spring }) {
  const color = useTransform(spring, v => v > 2.0 ? '#f87171' : '#4ade80')
  const text = useTransform(spring, v => `${v.toFixed(2)}%`)

  return (
    <motion.div className="sim-box-value" style={{ color }}>
      {text}
    </motion.div>
  )
}
