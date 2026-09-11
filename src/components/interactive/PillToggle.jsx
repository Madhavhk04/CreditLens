import { useState } from 'react'
import { motion } from 'framer-motion'

export default function PillToggle({ options = ['1M', '3M', '6M', '1Y'], value, onChange }) {
  const [active, setActive] = useState(value || options[2])

  const handleClick = (opt) => {
    setActive(opt)
    onChange?.(opt)
  }

  return (
    <div className="pill-toggle">
      {options.map((opt) => (
        <button
          key={opt}
          className={`pill-option ${active === opt ? 'active' : ''}`}
          onClick={() => handleClick(opt)}
        >
          {opt}
          {active === opt && (
            <motion.div
              className="pill-indicator"
              layoutId="pill-indicator"
              style={{ inset: 0, position: 'absolute' }}
              transition={{ type: 'spring', stiffness: 400, damping: 30 }}
            />
          )}
        </button>
      ))}
    </div>
  )
}
