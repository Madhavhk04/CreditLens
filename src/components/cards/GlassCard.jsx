import { motion } from 'framer-motion'

export default function GlassCard({ children, className = '', variant = 'neutral', ...props }) {
  const glowClass = variant === 'violet' ? 'glow-violet' : variant === 'red' ? 'glow-red' : ''

  return (
    <motion.div
      className={`glass-card ${glowClass} ${className}`}
      whileHover={{ borderColor: 'rgba(255,255,255,0.12)' }}
      transition={{ duration: 0.2 }}
      {...props}
    >
      {children}
    </motion.div>
  )
}
